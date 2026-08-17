from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic

FORBIDDEN_VISIBLE = (
    'Patient Service', 'Patient Repository', 'Booking Service', 'Payment Service',
    'Queue Service', 'API Gateway', 'OTP Validator', 'SMS Provider', 'Password Service',
    'Repository', 'Controller', 'Microservice', 'Event Bus', 'CQRS Handler', 'ORM',
    '<<system participant>>', '<<external system>>', 'alt ', 'opt ', 'loop ', 'break ',
    'par ', 'critical ', 'ref ', 'Alternative Flow', 'Failure Flow', 'Exception Flow',
)


def validate_sequence_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root = ET.parse(svg_path).getroot()
    lifelines = [node for node in root.iter() if node.attrib.get('data-kind') == 'lifeline']
    messages = [node for node in root.iter() if node.attrib.get('data-kind') == 'message']
    forbidden_nodes = [node for node in root.iter() if node.attrib.get('data-kind') in {'alt-fragment', 'opt-fragment', 'loop-fragment', 'break-fragment', 'par-fragment', 'critical-fragment', 'ref-fragment', 'note'}]
    visible_participants = [item for item in model.elements if item.id in view.include]
    expected_main = sorted((item for item in model.relations if item.id in view.relations), key=lambda item: item.metadata['sequence'])
    if len(lifelines) != len(visible_participants):
        diagnostics.append(Diagnostic('Q4', 'lifeline-count', f'Expected {len(visible_participants)} lifelines, found {len(lifelines)}'))
    expected_lifeline_ids = {item.id for item in visible_participants}
    rendered_lifeline_ids = {node.attrib.get('data-semantic-id') for node in lifelines}
    for item_id in expected_lifeline_ids - rendered_lifeline_ids:
        diagnostics.append(Diagnostic('Q4', 'missing-lifeline', 'Lifeline missing from SVG', subject=item_id))
    rendered_main = [node for node in messages if node.attrib.get('data-semantic-id') in view.relations]
    if len(rendered_main) != len(expected_main):
        diagnostics.append(Diagnostic('Q4', 'main-message-count', f'Expected {len(expected_main)} main messages, found {len(rendered_main)}'))
    rendered_message_ids = {node.attrib.get('data-semantic-id') for node in rendered_main}
    for relation in expected_main:
        if relation.id not in rendered_message_ids:
            diagnostics.append(Diagnostic('Q4', 'missing-main-message', 'Main-flow message missing from SVG', subject=relation.id))
            continue
        matching = next(node for node in rendered_main if node.attrib.get('data-semantic-id') == relation.id)
        expected_style = 'dashed-return' if relation.type == 'return_message' else 'solid-request'
        if matching.attrib.get('data-style') != expected_style:
            diagnostics.append(Diagnostic('Q4', 'message-style', f'Expected {expected_style}', subject=relation.id))
        if matching.attrib.get('data-sequence') != str(relation.metadata['sequence']):
            diagnostics.append(Diagnostic('Q4', 'message-number', 'Rendered message number does not match model sequence', subject=relation.id))
    rendered_numbers = [int(node.attrib['data-sequence']) for node in rendered_main if node.attrib.get('data-sequence', '').isdigit()]
    if rendered_numbers != list(range(1, len(expected_main) + 1)):
        diagnostics.append(Diagnostic('Q4', 'nonsequential-numbering', 'Visible interactions must be numbered sequentially from 1'))
    if forbidden_nodes:
        diagnostics.append(Diagnostic('Q4', 'forbidden-uml-construct', 'Combined fragment or visible note present in lecturer-style Sequence Diagram'))
    source = svg_path.read_text(encoding='utf-8')
    for forbidden_text in FORBIDDEN_VISIBLE:
        if forbidden_text in source:
            diagnostics.append(Diagnostic('Q4', 'forbidden-content', f'Forbidden visible content: {forbidden_text}'))
    return diagnostics
