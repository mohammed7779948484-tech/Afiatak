from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.component_diagram_layouts import (
    TOKENS,
    InterfacePlacement,
    Rect,
    layout_for,
)
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
    node = ET.SubElement(parent, tag("text"), {"x": f"{x:.2f}", "y": f"{y:.2f}", "class": css, "text-anchor": anchor})
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag("tspan"), {"x": f"{x:.2f}", **({"dy": f"{line_height:.2f}"} if index else {})})
        span.text = line


def _module_glyph_bounds(box: Rect) -> Rect:
    return Rect(box.x - 2, box.y + 92, TOKENS.module_tab_width + 4, TOKENS.module_tab_height * 2 + TOKENS.module_tab_gap)


def _component(parent, item, box: Rect) -> None:
    glyph_bounds = _module_glyph_bounds(box)
    lines = _wrap(item.name, 29)
    name_width = box.width - 380
    name_height = TOKENS.component_name_line_height * len(lines)
    name_left = box.x + 250
    name_top = box.center_y - name_height / 2 - 8
    name_bounds = Rect(name_left, name_top, name_width, name_height)
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": item.id,
            "data-kind": "component",
            "data-semantic-id": item.id,
            "data-component-name": item.name,
            "data-component-symbol": "uml-module",
            "data-bounds": _bounds(box),
            "data-module-glyph-bounds": _bounds(glyph_bounds),
            "data-name-bounds": _bounds(name_bounds),
            "aria-label": item.name,
        },
    )
    ET.SubElement(group, tag("rect"), {"x": f"{box.x:.2f}", "y": f"{box.y:.2f}", "width": f"{box.width:.2f}", "height": f"{box.height:.2f}", "class": "component-box"})
    # A classic UML Component marker: two open tabs share the Component's left
    # boundary rather than floating as unrelated rectangles inside the body.
    tab_x = box.x
    tab_y = glyph_bounds.y
    for offset in (0.0, TOKENS.module_tab_height + TOKENS.module_tab_gap):
        ET.SubElement(
            group,
            tag("path"),
            {"d": f"M {tab_x:.2f} {tab_y + offset:.2f} H {tab_x + TOKENS.module_tab_width:.2f} V {tab_y + offset + TOKENS.module_tab_height:.2f} H {tab_x:.2f}", "class": "component-module-tab"},
        )
    baseline = name_top + TOKENS.component_name_font_size
    _multiline(group, lines, name_bounds.x + name_bounds.width / 2, baseline, "component-name", TOKENS.component_name_line_height, "middle")


def _interface_label(parent, item, placement: InterfacePlacement) -> Rect:
    lines = _wrap(item.name, max(15, int(placement.label_width / 34)))
    if placement.label_anchor == "middle":
        x = placement.label_x
        left = x - placement.label_width / 2
    elif placement.label_anchor == "end":
        x = placement.label_x
        left = x - placement.label_width
    else:
        x = placement.label_x
        left = x
    top = placement.label_y - TOKENS.interface_label_font_size
    height = TOKENS.interface_label_line_height * len(lines) + 10
    _multiline(parent, lines, x, placement.label_y, "interface-label", TOKENS.interface_label_line_height, placement.label_anchor)
    return Rect(left, top, placement.label_width, height)


def _boundary_point(owner: Rect, placement: InterfacePlacement) -> tuple[float, float]:
    if placement.side == "left":
        return owner.x, placement.y
    if placement.side == "right":
        return owner.right, placement.y
    if placement.side == "top":
        return placement.x, owner.y
    if placement.side == "bottom":
        return placement.x, owner.bottom
    raise ValueError(f"Unsupported component side: {placement.side}")


def _provided_interface(parent, item, placement: InterfacePlacement, owner: Rect) -> None:
    boundary = _boundary_point(owner, placement)
    radius = TOKENS.provided_radius
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
            "data-glyph-bounds": _bounds(Rect(placement.x - radius, placement.y - radius, radius * 2, radius * 2)),
            "data-stem-boundary-point": f"{boundary[0]:.2f},{boundary[1]:.2f}",
            "aria-label": f"Provided interface {item.name}",
        },
    )
    if placement.side == "left":
        ET.SubElement(group, tag("line"), {"x1": f"{placement.x + radius:.2f}", "y1": f"{placement.y:.2f}", "x2": f"{boundary[0]:.2f}", "y2": f"{boundary[1]:.2f}", "class": "interface-stem"})
    elif placement.side == "top":
        ET.SubElement(group, tag("line"), {"x1": f"{placement.x:.2f}", "y1": f"{placement.y + radius:.2f}", "x2": f"{boundary[0]:.2f}", "y2": f"{boundary[1]:.2f}", "class": "interface-stem"})
    else:
        raise ValueError(f"Unsupported provided interface side: {placement.side}")
    ET.SubElement(group, tag("circle"), {"cx": f"{placement.x:.2f}", "cy": f"{placement.y:.2f}", "r": f"{radius:.2f}", "class": "provided-interface"})
    label_bounds = _interface_label(group, item, placement)
    group.attrib["data-label-bounds"] = _bounds(label_bounds)


def _required_socket_path(placement: InterfacePlacement) -> str:
    radius = TOKENS.required_radius
    terminal = radius + 16.0
    if placement.side == "right":
        return f"M {placement.x + terminal:.2f} {placement.y - radius:.2f} A {radius:.2f} {radius:.2f} 0 0 0 {placement.x + terminal:.2f} {placement.y + radius:.2f}"
    if placement.side == "bottom":
        return f"M {placement.x - radius:.2f} {placement.y + terminal:.2f} A {radius:.2f} {radius:.2f} 0 0 0 {placement.x + radius:.2f} {placement.y + terminal:.2f}"
    raise ValueError(f"Unsupported required interface side: {placement.side}")


def _required_interface(parent, item, placement: InterfacePlacement, owner: Rect) -> None:
    boundary = _boundary_point(owner, placement)
    radius = TOKENS.required_radius
    terminal = radius + 16.0
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
            "data-glyph-bounds": _bounds(Rect(placement.x + 16 - radius, placement.y - radius, radius * 2, radius * 2) if placement.side == "right" else Rect(placement.x - radius, placement.y + 16, radius * 2, radius * 2)),
            "data-stem-boundary-point": f"{boundary[0]:.2f},{boundary[1]:.2f}",
            "aria-label": f"Required interface {item.name}",
        },
    )
    if placement.side == "right":
        ET.SubElement(group, tag("line"), {"x1": f"{boundary[0]:.2f}", "y1": f"{boundary[1]:.2f}", "x2": f"{placement.x + 16:.2f}", "y2": f"{placement.y:.2f}", "class": "interface-stem"})
    elif placement.side == "bottom":
        ET.SubElement(group, tag("line"), {"x1": f"{boundary[0]:.2f}", "y1": f"{boundary[1]:.2f}", "x2": f"{placement.x:.2f}", "y2": f"{placement.y + terminal:.2f}", "class": "interface-stem"})
    else:
        raise ValueError(f"Unsupported required interface side: {placement.side}")
    ET.SubElement(group, tag("path"), {"d": _required_socket_path(placement), "class": "required-interface"})
    label_bounds = _interface_label(group, item, placement)
    group.attrib["data-label-bounds"] = _bounds(label_bounds)


def _connector(parent, relation, points: tuple[tuple[float, float], ...]) -> None:
    group = ET.SubElement(parent, tag("g"), {"id": relation.id, "data-kind": "assembly-connector", "data-semantic-id": relation.id, "data-required-interface": relation.source, "data-provided-interface": relation.target, "data-points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points), "aria-label": "Assembly connector"})
    ET.SubElement(group, tag("polyline"), {"points": group.attrib["data-points"], "class": "assembly-connector"})


def _style() -> str:
    return f"""
      .page {{ fill:#FFFFFF; }}
      .page-heading {{ font-family:"DejaVu Serif","Times New Roman",serif; font-size:{TOKENS.title_font_size}px; font-weight:700; fill:#1F1F1F; }}
      .component-box {{ fill:#FFFFFF; stroke:#262626; stroke-width:{TOKENS.component_stroke_width}; }}
      .component-module-tab {{ fill:none; stroke:#262626; stroke-width:{TOKENS.glyph_stroke_width}; stroke-linecap:square; stroke-linejoin:miter; }}
      .component-name {{ font-family:Arial,Helvetica,sans-serif; font-size:{TOKENS.component_name_font_size}px; font-weight:700; fill:#1F1F1F; }}
      .interface-stem {{ fill:none; stroke:#303030; stroke-width:{TOKENS.glyph_stroke_width}; stroke-linecap:round; }}
      .provided-interface {{ fill:#FFFFFF; stroke:#202020; stroke-width:{TOKENS.glyph_stroke_width}; }}
      .required-interface {{ fill:none; stroke:#202020; stroke-width:{TOKENS.glyph_stroke_width}; stroke-linecap:round; }}
      .assembly-connector {{ fill:none; stroke:#353535; stroke-width:{TOKENS.connector_stroke_width}; stroke-linecap:round; stroke-linejoin:round; }}
      .interface-label {{ font-family:Arial,Helvetica,sans-serif; font-size:{TOKENS.interface_label_font_size}px; font-weight:500; fill:#303030; }}
    """


def render_component_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout = layout_for(view.id)
    selected = {item.id: item for item in model.elements if item.id in view.include}
    relation_by_id = {item.id: item for item in model.relations}
    relations = [relation_by_id[item_id] for item_id in view.relations]
    scale = min(1.0, 8192 / max(layout.width, layout.height))
    root = ET.Element(tag("svg"), {"width": str(round(layout.width * scale)), "height": str(round(layout.height * scale)), "viewBox": f"0 0 {layout.width} {layout.height}", "role": "img", "aria-labelledby": "diagram-title diagram-description", "data-kind": "component-diagram", "data-diagram-id": str(view.options.get("diagramId", "")), "data-page-bounds": f"0.00,0.00,{layout.width:.2f},{layout.height:.2f}"})
    title = ET.SubElement(root, tag("title"), {"id": "diagram-title"})
    title.text = view.title
    description = ET.SubElement(root, tag("desc"), {"id": "diagram-description"})
    description.text = "Lecturer-style UML Component Diagram with standard module Components, provided-interface lollipops, required-interface sockets, and assembly connectors."
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
            _provided_interface(interface_layer, item, placement, layout.component_boxes[placement.component_id])
        elif item.type == "required_interface" and placement:
            _required_interface(interface_layer, item, placement, layout.component_boxes[placement.component_id])

    source = ET.tostring(root, encoding="unicode")
    for forbidden in FORBIDDEN_VISIBLE:
        if forbidden in source:
            raise ValueError(f"Forbidden Component-Diagram content: {forbidden}")
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
