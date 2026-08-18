"""SVG renderer for collision-aware UML Collaboration/Communication diagrams."""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.collaboration_geometry import (
    CollaborationRenderPlan,
    MessageLabelGeometry,
    ParticipantGeometry,
    TextBlock,
    arrow_data,
    build_collaboration_render_plan,
    label_data,
    layout_metadata,
    link_data,
    loop_data,
)
from engine.core.models import SemanticModel, ViewSpec

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def tag(name: str) -> str:
    return f"{{{SVG}}}{name}"


def _text(parent, text: str, x: float, y: float, css: str, anchor: str = "start"):
    node = ET.SubElement(parent, tag("text"), {"x": f"{x:.2f}", "y": f"{y:.2f}", "class": css, "text-anchor": anchor})
    node.text = text
    return node


def _wrapped_text(parent, text: TextBlock, css: str, anchor: str = "start"):
    node = ET.SubElement(parent, tag("text"), {"x": f"{text.text_x:.2f}", "y": f"{text.first_baseline:.2f}", "class": css, "text-anchor": anchor})
    for index, line in enumerate(text.lines):
        span = ET.SubElement(node, tag("tspan"), {"x": f"{text.text_x:.2f}", **({"dy": f"{text.line_height:.2f}"} if index else {})})
        span.text = line
    return node


def _heading(parent, heading: TextBlock) -> None:
    _wrapped_text(parent, heading, "page-heading")


def _participant(parent, geometry: ParticipantGeometry) -> None:
    element = geometry.element
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": element.id,
            "data-kind": "participant",
            "data-semantic-id": element.id,
            "data-participant-name": element.name,
            "data-participant-bounds": geometry.bounds.data(),
            "aria-label": element.name,
        },
    )
    bounds = geometry.bounds
    ET.SubElement(group, tag("rect"), {"x": f"{bounds.x:.2f}", "y": f"{bounds.y:.2f}", "width": f"{bounds.width:.2f}", "height": f"{bounds.height:.2f}", "class": "participant-box"})
    line_height = 76.0
    first_baseline = bounds.center.y - (len(geometry.name_lines) - 1) * line_height / 2 + 24.0
    node = ET.SubElement(group, tag("text"), {"x": f"{bounds.center.x:.2f}", "y": f"{first_baseline:.2f}", "class": "participant-name", "text-anchor": "middle"})
    for index, line in enumerate(geometry.name_lines):
        span = ET.SubElement(node, tag("tspan"), {"x": f"{bounds.center.x:.2f}", **({"dy": f"{line_height:.2f}"} if index else {})})
        span.text = line


def _structural_link(parent, geometry, message_sequences: tuple[int, ...]) -> None:
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": f"structural-link-{geometry.link_id}",
            "data-kind": "structural-link",
            "data-semantic-id": geometry.link_id,
            "data-source": geometry.source_id,
            "data-target": geometry.target_id,
            "data-message-sequences": ",".join(str(sequence) for sequence in message_sequences),
            **link_data(geometry),
            "aria-label": f"Structural communication link {geometry.link_id}",
        },
    )
    ET.SubElement(group, tag("polyline"), {"points": geometry.polyline.data(), "class": "structural-link-line"})


def _message(parent, label: MessageLabelGeometry, arrow, side: str) -> None:
    relation = label.relation
    attributes = {
        "id": relation.id,
        "data-kind": "message",
        "data-semantic-id": relation.id,
        "data-sequence": str(relation.metadata["sequence"]),
        "data-source": relation.source,
        "data-target": relation.target,
        "data-direction": f"{relation.source}->{relation.target}",
        "data-exact-label": relation.name,
        "data-structural-link": label.link_id,
        "data-style": "solid-directional-message",
        "data-run-side": side,
        **label_data(label),
        **arrow_data(arrow),
        "aria-label": f"{relation.metadata['sequence']}. {relation.name}",
    }
    group = ET.SubElement(parent, tag("g"), attributes)
    ET.SubElement(group, tag("line"), {"x1": f"{arrow.segment.start.x:.2f}", "y1": f"{arrow.segment.start.y:.2f}", "x2": f"{arrow.segment.end.x:.2f}", "y2": f"{arrow.segment.end.y:.2f}", "class": "message-arrow", "marker-end": "url(#message-arrowhead)"})
    _text(group, label.text.number, label.text.number_x, label.text.first_baseline, "message-number")
    _wrapped_text(group, label.text, "message-label")


def _self_loop(parent, loop) -> None:
    relation = loop.relation
    label = loop.label
    group = ET.SubElement(
        parent,
        tag("g"),
        {
            "id": relation.id,
            "data-kind": "message",
            "data-semantic-id": relation.id,
            "data-sequence": str(relation.metadata["sequence"]),
            "data-source": relation.source,
            "data-target": relation.target,
            "data-direction": f"{relation.source}->{relation.target}",
            "data-exact-label": relation.name,
            "data-structural-link": "SELF",
            "data-self-message": "true",
            "data-style": "solid-self-message-loop",
            **label_data(label),
            **loop_data(loop),
            "aria-label": f"{relation.metadata['sequence']}. {relation.name}",
        },
    )
    start, control_one, control_two, end = loop.path.points
    curve = f"M {start.x:.2f} {start.y:.2f} C {control_one.x:.2f} {control_one.y:.2f}, {control_two.x:.2f} {control_two.y:.2f}, {end.x:.2f} {end.y:.2f}"
    ET.SubElement(group, tag("path"), {"d": curve, "class": "self-message-self", "marker-end": "url(#message-arrowhead)"})
    _text(group, label.text.number, label.text.number_x, label.text.first_baseline, "message-number")
    _wrapped_text(group, label.text, "message-label")


def _style() -> str:
    return """
      .page { fill:#FFFFFF; }
      .page-heading { font-family:"DejaVu Serif","Times New Roman",serif; font-size:72px; font-weight:700; fill:#8B1E1E; }
      .participant-box { fill:#FFFFFF; stroke:#222222; stroke-width:3.2; }
      .participant-name { font-family:"DejaVu Serif","Times New Roman",serif; font-size:64px; font-weight:400; text-decoration:underline; fill:#222222; }
      .structural-link-line { stroke:#777777; stroke-width:2.4; fill:none; stroke-linecap:round; stroke-linejoin:round; }
      .message-arrow { stroke:#555555; stroke-width:2.8; fill:none; stroke-linecap:round; }
      .self-message-self { stroke:#555555; stroke-width:2.8; fill:none; stroke-linecap:round; stroke-linejoin:round; }
      .message-number { font-family:"DejaVu Serif","Times New Roman",serif; font-size:62px; font-weight:700; fill:#333333; }
      .message-label { font-family:"DejaVu Serif","Times New Roman",serif; font-size:62px; font-weight:400; fill:#333333; }
    """


def render_collaboration_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> CollaborationRenderPlan:
    plan = build_collaboration_render_plan(model, view)
    scale = min(1.0, 8192 / max(plan.canvas.width, plan.canvas.height))
    root = ET.Element(
        tag("svg"),
        {
            "width": str(round(plan.canvas.width * scale)),
            "height": str(round(plan.canvas.height * scale)),
            "viewBox": f"0 0 {plan.canvas.width:.2f} {plan.canvas.height:.2f}",
            "role": "img",
            "aria-labelledby": "diagram-title diagram-description",
            **layout_metadata(plan),
        },
    )
    title = ET.SubElement(root, tag("title"), {"id": "diagram-title"})
    title.text = view.title
    description = ET.SubElement(root, tag("desc"), {"id": "diagram-description"})
    description.text = "Academic UML Collaboration/Communication Diagram with object boxes, reusable communication links, numbered directional messages, collision-aware label placement, and no sequence-diagram constructs."
    definitions = ET.SubElement(root, tag("defs"))
    style = ET.SubElement(definitions, tag("style"))
    style.text = _style()
    marker = ET.SubElement(definitions, tag("marker"), {"id": "message-arrowhead", "viewBox": "0 0 14 12", "markerWidth": "15", "markerHeight": "14", "refX": "12", "refY": "6", "orient": "auto", "markerUnits": "strokeWidth"})
    ET.SubElement(marker, tag("path"), {"d": "M 0 0 L 13 6 L 0 12 Z", "fill": "#555555"})
    ET.SubElement(root, tag("rect"), {"x": "0", "y": "0", "width": f"{plan.canvas.width:.2f}", "height": f"{plan.canvas.height:.2f}", "class": "page"})
    _heading(root, plan.heading)

    link_layer = ET.SubElement(root, tag("g"), {"aria-label": "Reusable structural communication links"})
    link_sequences = {item["id"]: tuple(item["messageSequences"]) for item in view.options["structuralLinks"]}
    for link in plan.links.values():
        _structural_link(link_layer, link, link_sequences[link.link_id])
    participant_layer = ET.SubElement(root, tag("g"), {"aria-label": "Collaboration participants"})
    for participant in plan.participants.values():
        _participant(participant_layer, participant)
    message_layer = ET.SubElement(root, tag("g"), {"aria-label": "Globally numbered directional messages"})
    for run in plan.runs.values():
        arrows = {arrow.relation.id: arrow for arrow in run.arrows}
        for label in run.labels:
            _message(message_layer, label, arrows[label.relation.id], run.side)
    for loop in plan.loops:
        _self_loop(message_layer, loop)

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
    return plan
