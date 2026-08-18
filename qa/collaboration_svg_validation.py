from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

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
    "loop ",
    "break ",
    "par ",
    "critical ",
    "ref ",
    "Alternative Flow",
    "Failure Flow",
    "Exception Flow",
)


def validate_collaboration_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root = ET.parse(svg_path).getroot()
    participants = [node for node in root.iter() if node.attrib.get("data-kind") == "participant"]
    structural_links = [node for node in root.iter() if node.attrib.get("data-kind") == "structural-link"]
    messages = [node for node in root.iter() if node.attrib.get("data-kind") == "message"]
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
        expected_pair = set(link["participants"])
        rendered_pair = {node.attrib.get("data-source"), node.attrib.get("data-target")}
        if rendered_pair != expected_pair:
            diagnostics.append(Diagnostic("Q4", "structural-link-endpoints", "Structural link endpoints do not match model", subject=link_id))
        rendered_sequences = [int(value) for value in node.attrib.get("data-message-sequences", "").split(",") if value]
        if rendered_sequences != link["messageSequences"]:
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
    return diagnostics
