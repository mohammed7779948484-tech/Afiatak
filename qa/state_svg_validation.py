from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


def validate_state_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError as error:
        return [Diagnostic('Q4', 'svg-parse', f'Invalid SVG: {error}')]
    expected_states = [item for item in model.elements if item.id in view.include and item.type == 'state']
    expected_relations = [item for item in model.relations if item.id in view.relations]
    groups = list(root.iter())
    rendered_states = [node for node in groups if node.attrib.get('data-kind') == 'state']
    rendered_initial = [node for node in groups if node.attrib.get('data-kind') == 'initial']
    rendered_final = [node for node in groups if node.attrib.get('data-kind') == 'final']
    rendered_transitions = [node for node in groups if node.attrib.get('data-kind') == 'transition']
    if len(rendered_states) != len(expected_states):
        diagnostics.append(Diagnostic('Q4', 'state-count', f'Expected {len(expected_states)} rendered State boxes, found {len(rendered_states)}'))
    if len(rendered_initial) != 1:
        diagnostics.append(Diagnostic('Q4', 'initial-count', 'State SVG must render exactly one Initial pseudostate'))
    expected_final_count = sum(item.type == 'final' for item in model.elements if item.id in view.include)
    if len(rendered_final) != expected_final_count:
        diagnostics.append(Diagnostic('Q4', 'final-count', f'Expected {expected_final_count} rendered Final pseudostates, found {len(rendered_final)}'))
    if len(rendered_transitions) != len(expected_relations):
        diagnostics.append(Diagnostic('Q4', 'transition-count', f'Expected {len(expected_relations)} rendered transitions, found {len(rendered_transitions)}'))
    expected_names = {item.id: item.name for item in expected_states}
    for node in rendered_states:
        identifier = node.attrib.get('data-semantic-id')
        if identifier not in expected_names:
            diagnostics.append(Diagnostic('Q4', 'unknown-state', 'Rendered State is not in model', subject=identifier))
        elif node.attrib.get('data-state-name') != expected_names[identifier]:
            diagnostics.append(Diagnostic('Q4', 'state-name', 'Rendered State name differs from model', subject=identifier))
    expected_edges = {item.id: (item.source, item.target, item.name) for item in expected_relations}
    for node in rendered_transitions:
        identifier = node.attrib.get('data-semantic-id')
        if identifier not in expected_edges:
            diagnostics.append(Diagnostic('Q4', 'unknown-transition', 'Rendered Transition is not in model', subject=identifier))
            continue
        source, target, label = expected_edges[identifier]
        if node.attrib.get('data-source') != source or node.attrib.get('data-target') != target:
            diagnostics.append(Diagnostic('Q4', 'transition-direction', 'Rendered Transition endpoints differ from model', subject=identifier))
        if node.attrib.get('aria-label') != label:
            diagnostics.append(Diagnostic('Q4', 'transition-label', 'Rendered Transition label differs from model', subject=identifier))
    text = svg_path.read_text(encoding='utf-8')
    if 'marker-end="url(#state-arrow)"' not in text:
        diagnostics.append(Diagnostic('Q5', 'missing-arrowheads', 'State transitions need directed arrowheads'))
    for prohibited in view.options.get('prohibitedContent', []):
        if prohibited in {node.attrib.get('data-state-name') for node in rendered_states}:
            diagnostics.append(Diagnostic('Q5', 'prohibited-state', f'Prohibited State rendered: {prohibited}'))
    for forbidden in ('lifeline', 'message-label', 'actor-head', 'participant-box', 'alt-fragment', 'shape=note'):
        if forbidden in text:
            diagnostics.append(Diagnostic('Q5', 'mixed-notation', f'Forbidden non-state notation found: {forbidden}'))
    return diagnostics
