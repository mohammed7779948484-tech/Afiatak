from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.component_diagram_layouts import InterfacePlacement, Rect, layout_for
from engine.core.models import SemanticModel, ViewSpec


SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


FORBIDDEN_VISIBLE = (
    "Doctor Application",
    "Reception Application",
    "Facility Administrator Application",
    "Authentication Service",
    "Booking Service",
    "Queue Service",
    "Payment Service",
    "Notification Microservice",
    "API Gateway",
    "SMS Provider",
    "HIS",
    "EHR",
)


def tag(name: str) -> str:
    return f"{{{SVG}}}{name}"


def _bounds(rect: Rect) -> str:
    return f"{rect.x:.2f},{rect.y:.2f},{rect.width:.2f},{rect.height:.2f}"


def _wrap(text: str, maximum: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if current and len(candidate) > maximum:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def _multiline(parent, lines: list[str], x: float, y: float, css: str, line_height: float, anchor: str) -> None:
    node = ET.SubElement(
        parent,
        tag("text"),
        {"x": f"{x:.2f}", "y": f"{y:.2f}", "class": css, "text-anchor": anchor},
    )
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag("tspan"), {"x": f"{x:.2f}", **({"dy": f"{line_height:.2f}"} if index else {})})
        span.text = line


def _component(parent, item, box: Rect) -> None:
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": item.id,
            "data-kind": "component",
            "data-semantic-id": item.id,
            "data-component-name": item.name,
            "data-bounds": _bounds(box),
            "aria-label": item.name,
        },
    )
    ET.SubElement(
        group,
        tag("rect"),
        {"x": f"{box.x:.2f}", "y": f"{box.y:.2f}", "width": f"{box.width:.2f}", "height": f"{box.height:.2f}", "class": "component-box"},
    )
    glyph_x, glyph_y = box.right - 285, box.y + 82
    ET.SubElement(group, tag("rect"), {"x": f"{glyph_x:.2f}", "y": f"{glyph_y:.2f}", "width": "145", "height": "74", "class": "component-glyph"})
    ET.SubElement(group, tag("rect"), {"x": f"{glyph_x:.2f}", "y": f"{glyph_y + 100:.2f}", "width": "145", "height": "74", "class": "component-glyph"})
    lines = _wrap(item.name, 29)
    baseline = box.center_y - (len(lines) - 1) * 40 + 28
    _multiline(group, lines, box.center_x, baseline, "component-name", 80, "middle")


def _interface_label(parent, item, placement: InterfacePlacement) -> Rect:
    lines = _wrap(item.name, max(16, int(placement.label_width / 38)))
    line_height = 46.0
    if placement.label_anchor == "middle":
        x = placement.label_x
        left = x - placement.label_width / 2
    elif placement.label_anchor == "end":
        x = placement.label_x
        left = x - placement.label_width
    else:
        x = placement.label_x
        left = x
    top = placement.label_y - 38
    height = 46 * len(lines) + 12
    _multiline(parent, lines, x, placement.label_y, "interface-label", line_height, placement.label_anchor)
    return Rect(left, top, placement.label_width, height)


def _provided_interface(parent, item, placement: InterfacePlacement) -> None:
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": item.id,
            "data-kind": "provided-interface",
            "data-semantic-id": item.id,
            "data-interface-name": item.name,
            "data-owner-component": item.metadata.get("providerComponent", ""),
            "data-glyph": "lollipop",
            "data-center": f"{placement.x:.2f},{placement.y:.2f}",
            "aria-label": f"Provided interface {item.name}",
        },
    )
    radius = 55.0
    if placement.side == "left":
        ET.SubElement(group, tag("line"), {"x1": f"{placement.x + radius:.2f}", "y1": f"{placement.y:.2f}", "x2": f"{placement.x + 200:.2f}", "y2": f"{placement.y:.2f}", "class": "interface-stem"})
    elif placement.side == "top":
        ET.SubElement(group, tag("line"), {"x1": f"{placement.x:.2f}", "y1": f"{placement.y + radius:.2f}", "x2": f"{placement.x:.2f}", "y2": f"{placement.y + 200:.2f}", "class": "interface-stem"})
    ET.SubElement(group, tag("circle"), {"cx": f"{placement.x:.2f}", "cy": f"{placement.y:.2f}", "r": f"{radius:.2f}", "class": "provided-interface"})
    label_bounds = _interface_label(group, item, placement)
    group.attrib["data-label-bounds"] = _bounds(label_bounds)


def _required_socket_path(placement: InterfacePlacement) -> str:
    radius = 62.0
    if placement.side == "right":
        return f"M {placement.x + 64:.2f} {placement.y - radius:.2f} A {radius:.2f} {radius:.2f} 0 0 0 {placement.x + 64:.2f} {placement.y + radius:.2f}"
    if placement.side == "bottom":
        return f"M {placement.x - radius:.2f} {placement.y + 64:.2f} A {radius:.2f} {radius:.2f} 0 0 0 {placement.x + radius:.2f} {placement.y + 64:.2f}"
    raise ValueError(f"Unsupported required interface side: {placement.side}")


def _required_interface(parent, item, placement: InterfacePlacement) -> None:
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": item.id,
            "data-kind": "required-interface",
            "data-semantic-id": item.id,
            "data-interface-name": item.name,
            "data-owner-component": item.metadata.get("ownerComponent", ""),
            "data-matching-provided-interface": item.metadata.get("matchingProvidedInterface", ""),
            "data-glyph": "socket",
            "data-center": f"{placement.x:.2f},{placement.y:.2f}",
            "aria-label": f"Required interface {item.name}",
        },
    )
    if placement.side == "right":
        ET.SubElement(group, tag("line"), {"x1": f"{placement.x - 200:.2f}", "y1": f"{placement.y:.2f}", "x2": f"{placement.x - 58:.2f}", "y2": f"{placement.y:.2f}", "class": "interface-stem"})
    else:
        ET.SubElement(group, tag("line"), {"x1": f"{placement.x:.2f}", "y1": f"{placement.y - 200:.2f}", "x2": f"{placement.x:.2f}", "y2": f"{placement.y - 58:.2f}", "class": "interface-stem"})
    ET.SubElement(group, tag("path"), {"d": _required_socket_path(placement), "class": "required-interface"})
    label_bounds = _interface_label(group, item, placement)
    group.attrib["data-label-bounds"] = _bounds(label_bounds)


def _connector(parent, relation, points: tuple[tuple[float, float], ...]) -> None:
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": relation.id,
            "data-kind": "assembly-connector",
            "data-semantic-id": relation.id,
            "data-required-interface": relation.source,
            "data-provided-interface": relation.target,
            "data-points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
            "aria-label": "Assembly connector",
        },
    )
    ET.SubElement(group, tag("polyline"), {"points": group.attrib["data-points"], "class": "assembly-connector"})


def _style() -> str:
    return """
      .page { fill:#FFFFFF; }
      .page-heading { font-family:"DejaVu Serif","Times New Roman",serif; font-size:78px; font-weight:700; fill:#222222; }
      .component-box { fill:#FFFFFF; stroke:#242424; stroke-width:4; }
      .component-glyph { fill:#FFFFFF; stroke:#242424; stroke-width:3; }
      .component-name { font-family:Arial,sans-serif; font-size:62px; font-weight:600; fill:#202020; }
      .interface-stem { fill:none; stroke:#303030; stroke-width:3.2; stroke-linecap:round; }
      .provided-interface { fill:#FFFFFF; stroke:#202020; stroke-width:4; }
      .required-interface { fill:none; stroke:#202020; stroke-width:4; stroke-linecap:round; }
      .assembly-connector { fill:none; stroke:#353535; stroke-width:3.2; stroke-linecap:round; stroke-linejoin:round; }
      .interface-label { font-family:Arial,sans-serif; font-size:40px; font-weight:500; fill:#282828; }
    """


def render_component_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout = layout_for(view.id)
    selected = {item.id: item for item in model.elements if item.id in view.include}
    relation_by_id = {item.id: item for item in model.relations}
    relations = [relation_by_id[item_id] for item_id in view.relations]
    scale = min(1.0, 8192 / max(layout.width, layout.height))
    root = ET.Element(
        tag("svg"),
        {
            "width": str(round(layout.width * scale)),
            "height": str(round(layout.height * scale)),
            "viewBox": f"0 0 {layout.width} {layout.height}",
            "role": "img",
            "aria-labelledby": "diagram-title diagram-description",
            "data-kind": "component-diagram",
            "data-diagram-id": str(view.options.get("diagramId", "")),
            "data-page-bounds": f"0.00,0.00,{layout.width:.2f},{layout.height:.2f}",
        },
    )
    title = ET.SubElement(root, tag("title"), {"id": "diagram-title"})
    title.text = view.title
    description = ET.SubElement(root, tag("desc"), {"id": "diagram-description"})
    description.text = "Lecturer-style UML Component Diagram with standard components, provided-interface lollipops, required-interface sockets, and assembly connectors."
    definitions = ET.SubElement(root, tag("defs"))
    style = ET.SubElement(definitions, tag("style"))
    style.text = _style()
    ET.SubElement(root, tag("rect"), {"x": "0", "y": "0", "width": str(layout.width), "height": str(layout.height), "class": "page"})
    _multiline(root, [view.title], layout.width / 2, layout.title_y, "page-heading", 0, "middle")

    connector_layer = ET.SubElement(root, tag("g"), {"aria-label": "Assembly connectors"})
    for relation in relations:
        if relation.type == "connector":
            _connector(connector_layer, relation, layout.connector_paths[relation.id])

    component_layer = ET.SubElement(root, tag("g"), {"aria-label": "UML components"})
    for item in selected.values():
        if item.type == "component":
            _component(component_layer, item, layout.component_boxes[item.id])

    interface_layer = ET.SubElement(root, tag("g"), {"aria-label": "Provided and required interfaces"})
    for item in selected.values():
        placement = layout.interfaces.get(item.id)
        if item.type == "provided_interface" and placement:
            _provided_interface(interface_layer, item, placement)
        elif item.type == "required_interface" and placement:
            _required_interface(interface_layer, item, placement)

    source = ET.tostring(root, encoding="unicode")
    for forbidden in FORBIDDEN_VISIBLE:
        if forbidden in source:
            raise ValueError(f"Forbidden Component-Diagram content: {forbidden}")
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
