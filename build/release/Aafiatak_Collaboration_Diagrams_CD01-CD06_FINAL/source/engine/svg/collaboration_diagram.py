from __future__ import annotations

import math
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.collaboration_diagram_layouts import layout_for
from engine.core.models import SemanticModel, ViewSpec

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def tag(name: str) -> str:
    return f"{{{SVG}}}{name}"


def wrap(text: str, maximum: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if line and len(candidate) > maximum:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or [""]


def add_text(parent, text: str, x: float, y: float, css: str, anchor: str = "start"):
    node = ET.SubElement(
        parent,
        tag("text"),
        {"x": f"{x:g}", "y": f"{y:g}", "class": css, "text-anchor": anchor},
    )
    node.text = text
    return node


def add_wrapped_text(parent, lines: list[str], x: float, y: float, css: str, line_height: float, anchor: str = "start"):
    node = ET.SubElement(
        parent,
        tag("text"),
        {"x": f"{x:g}", "y": f"{y:g}", "class": css, "text-anchor": anchor},
    )
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag("tspan"), {"x": f"{x:g}", **({"dy": f"{line_height:g}"} if index else {})})
        span.text = line
    return node


def rect_edge_point(centre: tuple[float, float], other: tuple[float, float], half_width: float, half_height: float) -> tuple[float, float]:
    cx, cy = centre
    dx, dy = other[0] - cx, other[1] - cy
    if dx == 0 and dy == 0:
        return centre
    scale = min(half_width / abs(dx) if dx else float("inf"), half_height / abs(dy) if dy else float("inf"))
    return cx + dx * scale, cy + dy * scale


def point_on_segment(start: tuple[float, float], end: tuple[float, float], fraction: float) -> tuple[float, float]:
    return start[0] + (end[0] - start[0]) * fraction, start[1] + (end[1] - start[1]) * fraction


def nearest_point_on_box(x: float, y: float, width: float, height: float, point: tuple[float, float]) -> tuple[float, float]:
    px, py = point
    candidates = [
        (x, min(max(py, y), y + height)),
        (x + width, min(max(py, y), y + height)),
        (min(max(px, x), x + width), y),
        (min(max(px, x), x + width), y + height),
    ]
    return min(candidates, key=lambda item: (item[0] - px) ** 2 + (item[1] - py) ** 2)


def draw_participant(parent, item, centre: tuple[float, float], layout) -> None:
    cx, cy = centre
    x, y = cx - layout.participant_width / 2, cy - layout.participant_height / 2
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": item.id,
            "data-kind": "participant",
            "data-semantic-id": item.id,
            "data-participant-name": item.name,
            "aria-label": item.name,
        },
    )
    ET.SubElement(
        group,
        tag("rect"),
        {"x": f"{x:g}", "y": f"{y:g}", "width": str(layout.participant_width), "height": str(layout.participant_height), "class": "participant-box"},
    )
    name_lines = wrap(item.name, 24)
    text_y = cy - (len(name_lines) - 1) * 38 + 24
    add_wrapped_text(group, name_lines, cx, text_y, "participant-name", 76, "middle")


def draw_structural_link(parent, link: dict, positions: dict[str, tuple[float, float]], layout) -> tuple[tuple[float, float], tuple[float, float]]:
    source_id, target_id = link["participants"]
    source_centre, target_centre = positions[source_id], positions[target_id]
    start = rect_edge_point(source_centre, target_centre, layout.participant_width / 2, layout.participant_height / 2)
    end = rect_edge_point(target_centre, source_centre, layout.participant_width / 2, layout.participant_height / 2)
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": f"structural-link-{link['id']}",
            "data-kind": "structural-link",
            "data-semantic-id": link["id"],
            "data-source": source_id,
            "data-target": target_id,
            "data-message-sequences": ",".join(map(str, link["messageSequences"])),
            "aria-label": f"Structural communication link {link['id']}",
        },
    )
    ET.SubElement(
        group,
        tag("line"),
        {"x1": f"{start[0]:g}", "y1": f"{start[1]:g}", "x2": f"{end[0]:g}", "y2": f"{end[1]:g}", "class": "structural-link-line"},
    )
    return start, end


def draw_message(parent, relation, start: tuple[float, float], end: tuple[float, float], index: int, count: int, label_box: tuple[float, float, float], cursor_y: float, layout) -> float:
    sequence = relation.metadata["sequence"]
    label = relation.name
    x, _, width = label_box
    max_chars = max(22, int((width - 100) / 31))
    lines = wrap(label, max_chars)
    line_height = 72
    row_height = max(112, 24 + len(lines) * line_height)
    y = cursor_y
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": relation.id,
            "data-kind": "message",
            "data-semantic-id": relation.id,
            "data-sequence": str(sequence),
            "data-source": relation.source,
            "data-target": relation.target,
            "data-direction": f"{relation.source}->{relation.target}",
            "data-exact-label": label,
            "data-structural-link": str(relation.metadata.get("structuralLink", "")),
            "data-style": "solid-directional-message",
            "aria-label": f"{sequence}. {label}",
        },
    )
    # A short solid arrow lies on the reusable link. Its orientation encodes the
    # sender-to-receiver direction independently of the adjacent stacked label.
    distance = math.dist(start, end)
    base = 0.18 if count == 1 else 0.14 + 0.72 * index / (count - 1)
    if relation.source == relation.target:
        base = 0.5
    direct_start, direct_end = (start, end) if relation.source == relation.metadata.get("linkSource", relation.source) else (end, start)
    if relation.source != relation.metadata.get("linkSource", relation.source):
        direct_start, direct_end = end, start
    arrow_centre = point_on_segment(direct_start, direct_end, base)
    ux, uy = direct_end[0] - direct_start[0], direct_end[1] - direct_start[1]
    magnitude = math.hypot(ux, uy) or 1
    ux, uy = ux / magnitude, uy / magnitude
    arrow_length = min(340, max(190, distance * 0.14))
    arrow_start = (arrow_centre[0] - ux * arrow_length / 2, arrow_centre[1] - uy * arrow_length / 2)
    arrow_end = (arrow_centre[0] + ux * arrow_length / 2, arrow_centre[1] + uy * arrow_length / 2)
    ET.SubElement(
        group,
        tag("line"),
        {"x1": f"{arrow_start[0]:g}", "y1": f"{arrow_start[1]:g}", "x2": f"{arrow_end[0]:g}", "y2": f"{arrow_end[1]:g}", "class": "message-arrow", "marker-end": "url(#message-arrowhead)"},
    )
    # Lecturer reference: message text floats beside its reusable link; it is not a card or a panel.
    add_text(group, f"{sequence}.", x, y + 58, "message-number")
    add_wrapped_text(group, lines, x + 122, y + 54, "message-label", line_height)
    return y + row_height + 18


def draw_self_message(parent, relation, item, centre: tuple[float, float], definition: dict, layout) -> None:
    sequence = relation.metadata["sequence"]
    label = relation.name
    box_x, box_y, box_width = definition["box"]
    label_lines = wrap(label, max(22, int((box_width - 100) / 31)))
    line_height = 72
    cx, cy = centre
    box_top = cy - layout.participant_height / 2
    loop_left = cx - 180
    loop_right = cx + 180
    loop_peak = box_top - 520
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": relation.id,
            "data-kind": "message",
            "data-semantic-id": relation.id,
            "data-sequence": str(sequence),
            "data-source": relation.source,
            "data-target": relation.target,
            "data-direction": f"{relation.source}->{relation.target}",
            "data-exact-label": label,
            "data-structural-link": "SELF",
            "data-self-message": "true",
            "data-style": "solid-self-message-loop",
            "aria-label": f"{sequence}. {label}",
        },
    )
    # The lecturer reference draws a small loop immediately above the object box.
    ET.SubElement(group, tag("path"), {"d": f"M {loop_left:g} {box_top:g} C {cx - 390:g} {loop_peak:g}, {cx + 390:g} {loop_peak:g}, {loop_right:g} {box_top:g}", "class": "self-message-self", "marker-end": "url(#message-arrowhead)"})
    add_text(group, f"{sequence}.", box_x, box_y + 58, "message-number")
    add_wrapped_text(group, label_lines, box_x + 122, box_y + 54, "message-label", line_height)


def render_collaboration_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout, composition = layout_for(view.id)
    visible = {item.id: item for item in model.elements if item.id in view.include}
    relation_map = {relation.id: relation for relation in model.relations}
    relations = sorted((relation_map[relation_id] for relation_id in view.relations), key=lambda item: item.metadata["sequence"])
    positions = composition["participants"]
    if set(visible) != set(positions):
        raise ValueError("Collaboration composition and visible participant set do not match")

    max_dimension = 8192
    scale = min(1.0, max_dimension / max(layout.width, layout.height))
    root = ET.Element(
        tag("svg"),
        {
            "width": str(round(layout.width * scale)),
            "height": str(round(layout.height * scale)),
            "viewBox": f"0 0 {layout.width} {layout.height}",
            "role": "img",
            "aria-labelledby": "diagram-title diagram-description",
        },
    )
    title = ET.SubElement(root, tag("title"), {"id": "diagram-title"})
    title.text = view.title
    description = ET.SubElement(root, tag("desc"), {"id": "diagram-description"})
    description.text = "Academic UML Collaboration/Communication Diagram with participant boxes, reusable structural links, directional numbered messages, and no lifelines or activation bars."
    defs = ET.SubElement(root, tag("defs"))
    style = ET.SubElement(defs, tag("style"))
    style.text = """
      .page { fill:#FFFFFF; }
      .participant-box { fill:#FFFFFF; stroke:#222222; stroke-width:3.5; }
      .participant-name { font-family:"Times New Roman",serif; font-size:64px; font-weight:400; text-decoration:underline; fill:#222222; }
      .structural-link-line { stroke:#777777; stroke-width:2.5; fill:none; stroke-linecap:round; }
      .message-arrow { stroke:#777777; stroke-width:2.5; fill:none; stroke-linecap:round; }
      .self-message-self { stroke:#777777; stroke-width:2.5; fill:none; stroke-linejoin:round; }
      .message-number { font-family:"Times New Roman",serif; font-size:62px; font-weight:400; fill:#333333; }
      .message-label { font-family:"Times New Roman",serif; font-size:62px; font-weight:400; fill:#333333; }
    """
    marker = ET.SubElement(defs, tag("marker"), {"id": "message-arrowhead", "viewBox": "0 0 14 12", "markerWidth": "18", "markerHeight": "16", "refX": "12", "refY": "6", "orient": "auto", "markerUnits": "strokeWidth"})
    ET.SubElement(marker, tag("path"), {"d": "M 0 0 L 13 6 L 0 12 Z", "fill": "#777777"})
    ET.SubElement(root, tag("rect"), {"x": "0", "y": "0", "width": str(layout.width), "height": str(layout.height), "class": "page"})

    link_layer = ET.SubElement(root, tag("g"), {"aria-label": "Reusable structural communication links"})
    link_geometries: dict[str, tuple[tuple[float, float], tuple[float, float]]] = {}
    for link in view.options["structuralLinks"]:
        link_geometries[link["id"]] = draw_structural_link(link_layer, link, positions, layout)

    participant_layer = ET.SubElement(root, tag("g"), {"aria-label": "Collaboration participants"})
    for item_id, item in visible.items():
        draw_participant(participant_layer, item, positions[item_id], layout)

    message_layer = ET.SubElement(root, tag("g"), {"aria-label": "Globally numbered directional messages"})
    messages_by_link: dict[str, list] = {}
    self_messages: list = []
    for relation in relations:
        if relation.source == relation.target:
            self_messages.append(relation)
        else:
            messages_by_link.setdefault(relation.metadata["structuralLink"], []).append(relation)
    for link in view.options["structuralLinks"]:
        link_id = link["id"]
        messages = sorted(messages_by_link.get(link_id, []), key=lambda item: item.metadata["sequence"])
        if not messages:
            continue
        label_box = composition["links"][link_id]["labelBox"]
        cursor_y = label_box[1]
        start, end = link_geometries[link_id]
        for index, relation in enumerate(messages):
            # The renderer needs this direction key only to orient the short
            # arrow on a bidirectional structural link; it is not a semantic mutation.
            relation.metadata["linkSource"] = link["participants"][0]
            cursor_y = draw_message(message_layer, relation, start, end, index, len(messages), label_box, cursor_y, layout)
    for relation in self_messages:
        definition = composition["selfMessages"][relation.id]
        draw_self_message(message_layer, relation, visible[relation.source], positions[relation.source], definition, layout)

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
