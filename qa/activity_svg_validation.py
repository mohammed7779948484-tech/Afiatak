from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


def validate_activity_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError as error:
        return [Diagnostic('Q4', 'svg-parse', f'Invalid SVG: {error}')]

    selected = [element for element in model.elements if element.id in view.include]
    expected_by_type = {
        kind: {element.id: element.name for element in selected if element.type == kind}
        for kind in ('initial', 'final', 'action', 'decision', 'merge', 'note')
    }
    nodes = list(root.iter())
    for kind, expected in expected_by_type.items():
        rendered = [node for node in nodes if node.attrib.get('data-kind') == kind]
        if len(rendered) != len(expected):
            diagnostics.append(Diagnostic('Q4', f'{kind}-count', f'Expected {len(expected)} rendered {kind} nodes, found {len(rendered)}'))
        for node in rendered:
            identifier = node.attrib.get('data-semantic-id')
            if identifier not in expected:
                diagnostics.append(Diagnostic('Q4', f'unknown-{kind}', f'Rendered {kind} is not in model', subject=identifier))
                continue
            name_key = 'data-action-name' if kind == 'action' else 'data-node-name' if kind in {'decision', 'merge'} else 'data-note-name' if kind == 'note' else None
            if name_key and node.attrib.get(name_key) != expected[identifier]:
                diagnostics.append(Diagnostic('Q4', f'{kind}-name', f'Rendered {kind} name differs from model', subject=identifier))

    expected_relations = {relation.id: relation for relation in model.relations if relation.id in view.relations}
    rendered_flows = [node for node in nodes if node.attrib.get('data-kind') == 'control-flow']
    if len(rendered_flows) != len(expected_relations):
        diagnostics.append(Diagnostic('Q4', 'control-flow-count', f'Expected {len(expected_relations)} rendered control flows, found {len(rendered_flows)}'))
    labels = {node.attrib.get('data-relation-id'): node.attrib.get('aria-label') for node in nodes if node.attrib.get('data-kind') == 'guard-label'}
    element_by_id = model.by_id
    for node in rendered_flows:
        identifier = node.attrib.get('data-semantic-id')
        relation = expected_relations.get(identifier)
        if relation is None:
            diagnostics.append(Diagnostic('Q4', 'unknown-control-flow', 'Rendered Control Flow is not in model', subject=identifier))
            continue
        if node.attrib.get('data-source') != relation.source or node.attrib.get('data-target') != relation.target:
            diagnostics.append(Diagnostic('Q4', 'control-flow-direction', 'Rendered Control Flow endpoints differ from model', subject=identifier))
        if element_by_id[relation.source].type == 'decision' and labels.get(identifier) != relation.name:
            diagnostics.append(Diagnostic('Q4', 'decision-guard-label', 'Decision guard label differs from model', subject=identifier))

    text = svg_path.read_text(encoding='utf-8')
    title = view.title
    if title not in text:
        diagnostics.append(Diagnostic('Q5', 'missing-title', 'Exact Activity Diagram title is absent from SVG'))
    if 'marker-end="url(#activity-arrow)"' not in text:
        diagnostics.append(Diagnostic('Q5', 'missing-arrowheads', 'Activity Control Flows need directed arrowheads'))
    allowed_kinds = {'initial', 'final', 'action', 'decision', 'merge', 'note', 'control-flow', 'guard-label'}
    for node in nodes:
        kind = node.attrib.get('data-kind')
        if kind and kind not in allowed_kinds:
            diagnostics.append(Diagnostic('Q5', 'mixed-notation', f'Unexpected notation kind: {kind}'))
    for forbidden in ('lifeline', 'message-label', 'actor-head', 'participant-box', 'alt-fragment', 'usecase', '&lt;&lt;include&gt;&gt;', '&lt;&lt;extend&gt;&gt;'):
        if forbidden in text:
            diagnostics.append(Diagnostic('Q5', 'mixed-notation', f'Forbidden non-activity notation found: {forbidden}'))
    rendered_action_names = {node.attrib.get('data-action-name') for node in nodes if node.attrib.get('data-kind') == 'action'}
    rendered_node_names = rendered_action_names | {node.attrib.get('data-node-name') for node in nodes if node.attrib.get('data-kind') in {'decision', 'merge'}}
    for prohibited in view.options.get('prohibitedNodeNames', []):
        if prohibited in rendered_node_names:
            diagnostics.append(Diagnostic('Q5', 'prohibited-node', f'Prohibited Activity node rendered: {prohibited}'))
    return diagnostics
