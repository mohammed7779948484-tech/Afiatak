from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.deployment_diagram_layouts import DeploymentLayout, NodeLayout, Rect, TOKENS, layout_for
from engine.core.models import SemanticModel, ViewSpec


SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

FORBIDDEN_VISIBLE = (
    "AWS", "Azure", "GCP", "Vercel", "Railway", "VPS", "Docker", "Kubernetes",
    "Load Balancer", "CDN", "Reverse Proxy", "Nginx", "Caddy", "Apache", "API Gateway",
    "Redis", "Cache Server", "Queue Worker", "Message Broker", "Kafka", "RabbitMQ",
    "Object Storage", "File Server", "SMS Gateway", "SMS Provider", "HIS", "EHR",
    "Internal Scheduling Server", "Cashier", "Accounting Server", "Cloud",
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


def _multiline(parent, lines: list[str], x: float, y: float, css: str, line_height: float, anchor: str = "middle") -> None:
    node = ET.SubElement(parent, tag("text"), {"x": f"{x:.2f}", "y": f"{y:.2f}", "class": css, "text-anchor": anchor})
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag("tspan"), {"x": f"{x:.2f}", **({"dy": f"{line_height:.2f}"} if index else {})})
        span.text = line


def _shape_bounds(box: Rect) -> Rect:
    return Rect(box.x, box.y - TOKENS.perspective_y, box.width + TOKENS.perspective_x, box.height + TOKENS.perspective_y)


def _stereotype(value: str) -> str:
    return f"«{value}»"


def _node(parent, item, layout: NodeLayout) -> None:
    box = layout.box
    shape_bounds = _shape_bounds(box)
    title_lines = _wrap(item.name, 30)
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": item.id,
            "data-kind": "deployment-node",
            "data-semantic-id": item.id,
            "data-node-name": item.name,
            "data-node-symbol": "uml-deployment-node-3d",
            "data-node-stereotype": layout.node_stereotype or "",
            "data-bounds": _bounds(box),
            "data-shape-bounds": _bounds(shape_bounds),
            "data-name-bounds": _bounds(layout.title_bounds),
            "data-node-kind": str(item.metadata.get("nodeKind", "")),
            "aria-label": item.name,
        },
    )
    # Classic UML deployment node: front face with shallow top and right perspective faces.
    ET.SubElement(group, tag("path"), {"d": f"M {box.x:.2f} {box.y:.2f} H {box.right:.2f} V {box.bottom:.2f} H {box.x:.2f} Z", "class": "deployment-node-front"})
    ET.SubElement(group, tag("path"), {"d": f"M {box.x:.2f} {box.y:.2f} H {box.right:.2f} L {box.right + TOKENS.perspective_x:.2f} {box.y - TOKENS.perspective_y:.2f} H {box.x + TOKENS.perspective_x:.2f} {box.y - TOKENS.perspective_y:.2f} Z", "class": "deployment-node-top"})
    ET.SubElement(group, tag("path"), {"d": f"M {box.right:.2f} {box.y:.2f} L {box.right + TOKENS.perspective_x:.2f} {box.y - TOKENS.perspective_y:.2f} V {box.bottom - TOKENS.perspective_y:.2f} L {box.right:.2f} {box.bottom:.2f} Z", "class": "deployment-node-side"})
    title_x = layout.title_bounds.center_x
    if layout.node_stereotype:
        _multiline(group, [_stereotype(layout.node_stereotype)], title_x, layout.title_bounds.y + TOKENS.node_stereotype_font_size, "node-stereotype", TOKENS.node_stereotype_line_height)
        title_y = layout.title_bounds.y + TOKENS.node_stereotype_line_height + TOKENS.node_name_font_size
    else:
        title_y = layout.title_bounds.y + TOKENS.node_name_font_size
    _multiline(group, title_lines, title_x, title_y, "node-name", TOKENS.node_name_line_height)

    for index, contained_item in enumerate(layout.contained):
        label, bounds = contained_item.label, contained_item.bounds
        contained = ET.SubElement(
            group,
            tag("g"),
            {
                "id": f"{item.id}-contained-{index + 1}",
                "data-kind": contained_item.visual_kind,
                "data-owner-node": item.id,
                "data-item-name": label,
                "data-uml-kind": contained_item.uml_kind,
                "data-stereotype": contained_item.stereotype,
                "data-bounds": _bounds(bounds),
                "aria-label": f"{contained_item.uml_kind} {label}",
            },
        )
        if contained_item.visual_kind == "execution-environment":
            depth_x, depth_y = 18.0, 14.0
            ET.SubElement(contained, tag("path"), {"d": f"M {bounds.x:.2f} {bounds.y:.2f} H {bounds.right:.2f} V {bounds.bottom:.2f} H {bounds.x:.2f} Z", "class": "execution-environment-front"})
            ET.SubElement(contained, tag("path"), {"d": f"M {bounds.x:.2f} {bounds.y:.2f} H {bounds.right:.2f} L {bounds.right + depth_x:.2f} {bounds.y - depth_y:.2f} H {bounds.x + depth_x:.2f} {bounds.y - depth_y:.2f} Z", "class": "execution-environment-top"})
            ET.SubElement(contained, tag("path"), {"d": f"M {bounds.right:.2f} {bounds.y:.2f} L {bounds.right + depth_x:.2f} {bounds.y - depth_y:.2f} V {bounds.bottom - depth_y:.2f} L {bounds.right:.2f} {bounds.bottom:.2f} Z", "class": "execution-environment-side"})
        elif contained_item.visual_kind == "deployed-artifact":
            fold = min(54.0, max(32.0, bounds.height * 0.24))
            ET.SubElement(contained, tag("path"), {"d": f"M {bounds.x:.2f} {bounds.y:.2f} H {bounds.right - fold:.2f} L {bounds.right:.2f} {bounds.y + fold:.2f} V {bounds.bottom:.2f} H {bounds.x:.2f} Z", "class": "deployed-artifact"})
            ET.SubElement(contained, tag("path"), {"d": f"M {bounds.right - fold:.2f} {bounds.y:.2f} V {bounds.y + fold:.2f} H {bounds.right:.2f}", "class": "deployed-artifact-fold"})
        else:
            ET.SubElement(contained, tag("rect"), {"x": f"{bounds.x:.2f}", "y": f"{bounds.y:.2f}", "width": f"{bounds.width:.2f}", "height": f"{bounds.height:.2f}", "class": "device-context"})

        label_lines = _wrap(label, max(18, int(bounds.width / 32)))
        total_height = TOKENS.contained_stereotype_line_height + TOKENS.contained_line_height * len(label_lines)
        top = bounds.y + (bounds.height - total_height) / 2
        _multiline(contained, [_stereotype(contained_item.stereotype)], bounds.center_x, top + TOKENS.contained_stereotype_font_size, "contained-stereotype", TOKENS.contained_stereotype_line_height)
        _multiline(contained, label_lines, bounds.center_x, top + TOKENS.contained_stereotype_line_height + TOKENS.contained_font_size, "contained-item-name", TOKENS.contained_line_height)

    if layout.subtitle:
        subtitle, bounds = layout.subtitle
        subtitle_group = ET.SubElement(group, tag("g"), {"data-kind": "node-subtitle", "data-owner-node": item.id, "data-bounds": _bounds(bounds)})
        _multiline(subtitle_group, _wrap(subtitle, 52), bounds.center_x, bounds.y + TOKENS.subtitle_font_size, "node-subtitle", TOKENS.subtitle_font_size + 8)


def _communication_path(parent, relation, points: tuple[tuple[float, float], ...]) -> None:
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": relation.id,
            "data-kind": "communication-path",
            "data-semantic-id": relation.id,
            "data-source-id": relation.source,
            "data-target-id": relation.target,
            "data-points": " ".join(f"{x:.2f},{y:.2f}" for x, y in points),
            "data-arrowheads": "none",
            "aria-label": "Communication path",
        },
    )
    ET.SubElement(group, tag("polyline"), {"points": group.attrib["data-points"], "class": "communication-path"})


def _style() -> str:
    return f"""
      .page {{ fill:#FFFFFF; }}
      .page-heading {{ font-family:"DejaVu Serif","Times New Roman",serif; font-size:{TOKENS.title_font_size}px; font-weight:700; fill:#1F1F1F; }}
      .deployment-node-front {{ fill:#FFFFFF; stroke:#262626; stroke-width:{TOKENS.node_stroke_width}; stroke-linejoin:miter; }}
      .deployment-node-top, .deployment-node-side {{ fill:#F6F6F6; stroke:#262626; stroke-width:{TOKENS.node_stroke_width}; stroke-linejoin:miter; }}
      .node-name {{ font-family:Arial,Helvetica,sans-serif; font-size:{TOKENS.node_name_font_size}px; font-weight:700; fill:#1F1F1F; }}
      .node-stereotype {{ font-family:Arial,Helvetica,sans-serif; font-size:{TOKENS.node_stereotype_font_size}px; font-style:italic; fill:#454545; }}
      .execution-environment-front {{ fill:#FFFFFF; stroke:#3D3D3D; stroke-width:{TOKENS.contained_stroke_width}; stroke-linejoin:miter; }}
      .execution-environment-top, .execution-environment-side {{ fill:#F7F7F7; stroke:#3D3D3D; stroke-width:{TOKENS.contained_stroke_width}; stroke-linejoin:miter; }}
      .deployed-artifact {{ fill:#FFFFFF; stroke:#343434; stroke-width:{TOKENS.contained_stroke_width}; stroke-linejoin:miter; }}
      .deployed-artifact-fold {{ fill:none; stroke:#343434; stroke-width:{TOKENS.contained_stroke_width}; stroke-linejoin:miter; }}
      .device-context {{ fill:#FCFCFC; stroke:#5A5A5A; stroke-width:{TOKENS.contained_stroke_width}; stroke-dasharray:9 7; }}
      .contained-stereotype {{ font-family:Arial,Helvetica,sans-serif; font-size:{TOKENS.contained_stereotype_font_size}px; font-style:italic; fill:#4A4A4A; }}
      .contained-item-name {{ font-family:Arial,Helvetica,sans-serif; font-size:{TOKENS.contained_font_size}px; font-weight:500; fill:#242424; }}
      .node-subtitle {{ font-family:Arial,Helvetica,sans-serif; font-size:{TOKENS.subtitle_font_size}px; font-style:italic; fill:#454545; }}
      .communication-path {{ fill:none; stroke:#303030; stroke-width:{TOKENS.connector_stroke_width}; stroke-linecap:round; stroke-linejoin:round; }}
    """


def render_deployment_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout: DeploymentLayout = layout_for(view.id)
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
            "data-kind": "deployment-diagram",
            "data-diagram-id": str(view.options.get("diagramId", "")),
            "data-page-bounds": f"0.00,0.00,{layout.width:.2f},{layout.height:.2f}",
            "data-title-bounds": _bounds(Rect(750, 80, layout.width - 1500, 220)),
        },
    )
    title = ET.SubElement(root, tag("title"), {"id": "diagram-title"})
    title.text = view.title
    description = ET.SubElement(root, tag("desc"), {"id": "diagram-description"})
    description.text = "Lecturer-style UML Deployment Diagram with logical deployment nodes, contained execution environments or deployed artifacts, and solid unarrowed communication paths."
    definitions = ET.SubElement(root, tag("defs"))
    style = ET.SubElement(definitions, tag("style"))
    style.text = _style()
    ET.SubElement(root, tag("rect"), {"x": "0", "y": "0", "width": str(layout.width), "height": str(layout.height), "class": "page"})
    _multiline(root, [view.title], layout.width / 2, layout.title_y, "page-heading", 0)

    path_layer = ET.SubElement(root, tag("g"), {"aria-label": "Communication paths"})
    for relation in relations:
        if relation.type == "communication_path":
            _communication_path(path_layer, relation, layout.communication_paths[relation.id])

    node_layer = ET.SubElement(root, tag("g"), {"aria-label": "UML deployment nodes"})
    for item_id, node_layout in layout.nodes.items():
        _node(node_layer, selected[item_id], node_layout)

    source = ET.tostring(root, encoding="unicode")
    for forbidden in FORBIDDEN_VISIBLE:
        if forbidden in source:
            raise ValueError(f"Forbidden Deployment-Diagram content: {forbidden}")
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
