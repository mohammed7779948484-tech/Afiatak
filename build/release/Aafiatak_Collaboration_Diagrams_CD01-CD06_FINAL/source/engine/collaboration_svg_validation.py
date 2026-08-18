from __future__ import annotations

from itertools import combinations
from math import hypot
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.collaboration_geometry import Rect, parse_polyline, parse_rect, parse_segment, segment_intersects_rect
from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic

FORBIDDEN_KINDS = {
    "lifeline",
    "activation",
    "alt-fragment",
    "opt-fragment",
    "loop-fragment",
    "break-fragment",
    "par-fragment",
    "critical-fragment",
    "ref-fragment",
}
FORBIDDEN_VISIBLE = (
    "Patient Service",
    "Patient Repository",
    "Booking Service",
    "Payment Service",
    "Queue Service",
    "API Gateway",
    "OTP Validator",
    "SMS Provider",
    "Password Service",
    "Repository",
    "Controller",
    "Microservice",
    "Event Bus",
    "CQRS Handler",
    "ORM",
    "<<system participant>>",
    "<<external system>>",
    "alt ",
    "opt ",
    "break ",
    "par ",
    "critical ",
    "ref ",
    "Alternative Flow",
    "Failure Flow",
    "Exception Flow",
)


def _nodes(root, kind: str):
    return [node for node in root.iter() if node.attrib.get("data-kind") == kind]


def _geometry_diagnostics(root, participants, structural_links, messages) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if "data-page-bounds" not in root.attrib:
        return [Diagnostic("Q5", "geometry-metadata-missing", "Collaboration SVG must expose page and object geometry metadata")]
    canvas = parse_rect(root.attrib["data-page-bounds"])
    if int(root.attrib.get("data-layout-issue-count", "0")):
        diagnostics.append(Diagnostic("Q5", "layout-candidate-unresolved", root.attrib.get("data-layout-issues", "Renderer reported unresolved layout candidates")))

    participant_bounds: dict[str, Rect] = {}
    for node in participants:
        identifier = node.attrib.get("data-semantic-id", "unknown")
        try:
            bounds = parse_rect(node.attrib["data-participant-bounds"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "participant-geometry-missing", "Participant has no parseable geometry bounds", subject=identifier))
            continue
        participant_bounds[identifier] = bounds
        if not bounds.within(canvas, 40):
            diagnostics.append(Diagnostic("Q5", "participant-page-bounds", "Participant extends outside safe page bounds", subject=identifier))

    label_bounds: dict[str, Rect] = {}
    for node in messages:
        identifier = node.attrib.get("data-semantic-id", "unknown")
        try:
            bounds = parse_rect(node.attrib["data-label-bounds"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "label-geometry-missing", "Message has no parseable label geometry", subject=identifier))
            continue
        label_bounds[identifier] = bounds
        if not bounds.within(canvas, 60):
            diagnostics.append(Diagnostic("Q5", "label-page-bounds", "Message label extends outside safe page bounds", subject=identifier))
        for participant_id, participant_bounds_value in participant_bounds.items():
            if bounds.expanded(20).intersects(participant_bounds_value):
                diagnostics.append(Diagnostic("Q5", "label-participant-intersection", "Message label intersects a participant box", subject=f"{identifier}->{participant_id}"))

    for (first_id, first), (second_id, second) in combinations(label_bounds.items(), 2):
        if first.expanded(10).intersects(second.expanded(10)):
            diagnostics.append(Diagnostic("Q5", "label-label-intersection", "Message labels overlap or violate minimum safe spacing", subject=f"{first_id}<->{second_id}"))

    link_geometry: dict[str, tuple[object, set[str]]] = {}
    for node in structural_links:
        identifier = node.attrib.get("data-semantic-id", "unknown")
        try:
            polyline = parse_polyline(node.attrib["data-points"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "link-geometry-missing", "Structural link has no parseable route geometry", subject=identifier))
            continue
        endpoints = {node.attrib.get("data-source", ""), node.attrib.get("data-target", "")}
        link_geometry[identifier] = (polyline, endpoints)
        if not polyline.bounds.within(canvas, 30):
            diagnostics.append(Diagnostic("Q5", "link-page-bounds", "Structural link extends outside page bounds", subject=identifier))
        for participant_id, bounds in participant_bounds.items():
            if participant_id not in endpoints and polyline.intersects(bounds.expanded(16)):
                diagnostics.append(Diagnostic("Q5", "link-unrelated-participant-intersection", "Structural link crosses an unrelated participant", subject=f"{identifier}->{participant_id}"))
        for message_id, bounds in label_bounds.items():
            message_node = next((item for item in messages if item.attrib.get("data-semantic-id") == message_id), None)
            if message_node is not None and message_node.attrib.get("data-structural-link") != identifier and polyline.intersects(bounds.expanded(18)):
                diagnostics.append(Diagnostic("Q5", "link-unrelated-label-intersection", "Structural link crosses an unrelated message label", subject=f"{identifier}->{message_id}"))

    arrow_by_lane: dict[tuple[str, str], list[tuple[float, float, str]]] = {}
    for node in messages:
        identifier = node.attrib.get("data-semantic-id", "unknown")
        if node.attrib.get("data-self-message") == "true":
            continue
        try:
            arrow = parse_segment(node.attrib["data-arrow-segment"])
            start_distance = float(node.attrib["data-arrow-start-distance"])
            end_distance = float(node.attrib["data-arrow-end-distance"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "arrow-geometry-missing", "Directional message arrow has no parseable geometry", subject=identifier))
            continue
        for other_id, bounds in label_bounds.items():
            if other_id != identifier and any(segment_intersects_rect(segment, bounds.expanded(14)) for segment in (arrow,)):
                diagnostics.append(Diagnostic("Q5", "arrow-unrelated-label-intersection", "Directional arrow crosses an unrelated message label", subject=f"{identifier}->{other_id}"))
        key = (node.attrib.get("data-structural-link", ""), node.attrib.get("data-arrow-lane", ""))
        arrow_by_lane.setdefault(key, []).append((start_distance, end_distance, identifier))
    for (link_id, lane), intervals in arrow_by_lane.items():
        previous_end = float("-inf")
        for start, end, identifier in sorted(intervals):
            if start < previous_end + 40.0:
                diagnostics.append(Diagnostic("Q5", "arrow-density-overlap", "Directional arrows overlap or violate the minimum lane separation", subject=f"{link_id}/lane-{lane}/{identifier}"))
            previous_end = max(previous_end, end)

    loops = [node for node in messages if node.attrib.get("data-self-message") == "true"]
    loop_bounds: list[tuple[str, Rect]] = []
    for node in loops:
        identifier = node.attrib.get("data-semantic-id", "unknown")
        owner = node.attrib.get("data-source", "")
        try:
            bounds = parse_rect(node.attrib["data-loop-bounds"])
            path = parse_polyline(node.attrib["data-loop-points"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "self-loop-geometry-missing", "Self message has no parseable loop geometry", subject=identifier))
            continue
        loop_bounds.append((identifier, bounds))
        if not bounds.within(canvas, 60):
            diagnostics.append(Diagnostic("Q5", "self-loop-page-bounds", "Self loop extends outside safe page bounds", subject=identifier))
        label = label_bounds.get(identifier)
        if label is not None:
            horizontal_gap = max(0.0, max(bounds.left - label.right, label.left - bounds.right))
            vertical_gap = max(0.0, max(bounds.top - label.bottom, label.top - bounds.bottom))
            if hypot(horizontal_gap, vertical_gap) > 240.0:
                diagnostics.append(Diagnostic("Q5", "self-loop-detached-label", "Self-message label is not adjacent to its loop", subject=identifier))
        for participant_id, participant_bounds_value in participant_bounds.items():
            if participant_id != owner and path.intersects(participant_bounds_value.expanded(18)):
                diagnostics.append(Diagnostic("Q5", "self-loop-participant-intersection", "Self loop intersects an unrelated participant", subject=f"{identifier}->{participant_id}"))
        for link_id, (polyline, _) in link_geometry.items():
            if polyline.intersects(bounds.expanded(18)):
                diagnostics.append(Diagnostic("Q5", "self-loop-link-intersection", "Self loop intersects a structural communication link", subject=f"{identifier}->{link_id}"))
    for (first_id, first), (second_id, second) in combinations(loop_bounds, 2):
        if first.expanded(24).intersects(second.expanded(24)):
            diagnostics.append(Diagnostic("Q5", "duplicate-or-overlapping-self-loop", "Self loops overlap or share the same geometry", subject=f"{first_id}<->{second_id}"))
    return diagnostics


def validate_collaboration_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root = ET.parse(svg_path).getroot()
    participants = _nodes(root, "participant")
    structural_links = _nodes(root, "structural-link")
    messages = _nodes(root, "message")
    forbidden = [node for node in root.iter() if node.attrib.get("data-kind") in FORBIDDEN_KINDS]

    visible_participants = [item for item in model.elements if item.id in view.include]
    expected_messages = sorted((item for item in model.relations if item.id in view.relations), key=lambda item: item.metadata["sequence"])
    expected_links = {item["id"]: item for item in view.options.get("structuralLinks", [])}
    if len(participants) != len(visible_participants):
        diagnostics.append(Diagnostic("Q4", "participant-count", f"Expected {len(visible_participants)} participant boxes, found {len(participants)}"))
    rendered_participants = {node.attrib.get("data-semantic-id") for node in participants}
    for item in visible_participants:
        if item.id not in rendered_participants:
            diagnostics.append(Diagnostic("Q4", "missing-participant", "Participant box missing from SVG", subject=item.id))
    if len(structural_links) != len(expected_links):
        diagnostics.append(Diagnostic("Q4", "structural-link-count", f"Expected {len(expected_links)} structural links, found {len(structural_links)}"))
    rendered_links = {node.attrib.get("data-semantic-id"): node for node in structural_links}
    for link_id, link in expected_links.items():
        node = rendered_links.get(link_id)
        if node is None:
            diagnostics.append(Diagnostic("Q4", "missing-structural-link", "Structural communication link missing from SVG", subject=link_id))
            continue
        if {node.attrib.get("data-source"), node.attrib.get("data-target")} != set(link["participants"]):
            diagnostics.append(Diagnostic("Q4", "structural-link-endpoints", "Structural link endpoints do not match model", subject=link_id))
        sequences = [int(value) for value in node.attrib.get("data-message-sequences", "").split(",") if value]
        if sequences != link["messageSequences"]:
            diagnostics.append(Diagnostic("Q4", "structural-link-message-set", "Structural link message sequences do not match model", subject=link_id))
    rendered = {node.attrib.get("data-semantic-id"): node for node in messages}
    if len(messages) != len(expected_messages):
        diagnostics.append(Diagnostic("Q4", "message-count", f"Expected {len(expected_messages)} messages, found {len(messages)}"))
    for relation in expected_messages:
        node = rendered.get(relation.id)
        if node is None:
            diagnostics.append(Diagnostic("Q4", "missing-message", "Message missing from SVG", subject=relation.id))
            continue
        if node.attrib.get("data-sequence") != str(relation.metadata["sequence"]):
            diagnostics.append(Diagnostic("Q4", "message-number", "Rendered message number does not match model sequence", subject=relation.id))
        if node.attrib.get("data-source") != relation.source or node.attrib.get("data-target") != relation.target:
            diagnostics.append(Diagnostic("Q4", "message-direction", "Rendered message sender/receiver does not match model", subject=relation.id))
        if node.attrib.get("data-exact-label") != relation.name:
            diagnostics.append(Diagnostic("Q4", "message-label", "Rendered message label does not match model", subject=relation.id))
        if relation.source == relation.target:
            if node.attrib.get("data-self-message") != "true" or node.attrib.get("data-structural-link") != "SELF":
                diagnostics.append(Diagnostic("Q4", "self-message-loop", "Self-message is not rendered as a self loop", subject=relation.id))
        elif node.attrib.get("data-structural-link") != relation.metadata.get("structuralLink"):
            diagnostics.append(Diagnostic("Q4", "message-link-membership", "Message is assigned to the wrong structural link", subject=relation.id))
        elif node.attrib.get("data-style") != "solid-directional-message":
            diagnostics.append(Diagnostic("Q4", "message-style", "Communication messages must use solid directional arrows", subject=relation.id))
    rendered_sequences = [int(node.attrib["data-sequence"]) for node in messages if node.attrib.get("data-sequence", "").isdigit()]
    if sorted(rendered_sequences) != list(range(1, len(expected_messages) + 1)):
        diagnostics.append(Diagnostic("Q4", "nonsequential-numbering", "Visible interactions must be numbered sequentially from 1"))
    if forbidden:
        diagnostics.append(Diagnostic("Q4", "forbidden-uml-construct", "Lifeline, activation bar, or Sequence fragment present in Collaboration SVG"))
    source = svg_path.read_text(encoding="utf-8")
    for forbidden_text in FORBIDDEN_VISIBLE:
        if forbidden_text in source:
            diagnostics.append(Diagnostic("Q4", "forbidden-content", f"Forbidden visible content: {forbidden_text}"))
    diagnostics.extend(_geometry_diagnostics(root, participants, structural_links, messages))
    return diagnostics
