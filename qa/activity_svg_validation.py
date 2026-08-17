from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


def rendered_name(element) -> str:
    label = element.metadata.get('visibleLabel')
    return label if isinstance(label, str) else element.name


def validate_activity_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError as error:
        return [Diagnostic('Q4', 'svg-parse', f'Invalid SVG: {error}')]
    selected = [element for element in model.elements if element.id in view.include]
    expected_by_type = {
        kind: {element.id: rendered_name(element) for element in selected if element.type == kind}
        for kind in ('initial', 'final', 'action', 'object', 'decision', 'merge', 'fork', 'join', 'note')
    }
    nodes = list(root.iter())
    name_keys = {'action': 'data-action-name', 'object': 'data-object-name', 'decision': 'data-node-name', 'merge': 'data-node-name', 'note': 'data-note-name'}
    for kind, expected in expected_by_type.items():
        rendered = [node for node in nodes if node.attrib.get('data-kind') == kind]
        if len(rendered) != len(expected):
            diagnostics.append(Diagnostic('Q4', f'{kind}-count', f'Expected {len(expected)} rendered {kind} nodes, found {len(rendered)}'))
        for node in rendered:
            identifier = node.attrib.get('data-semantic-id')
            if identifier not in expected:
                diagnostics.append(Diagnostic('Q4', f'unknown-{kind}', f'Rendered {kind} is not in model', subject=identifier))
                continue
            name_key = name_keys.get(kind)
            if name_key and node.attrib.get(name_key) != expected[identifier]:
                diagnostics.append(Diagnostic('Q4', f'{kind}-name', f'Rendered {kind} name differs from v3 visible label', subject=identifier))
    expected_relations = {relation.id: relation for relation in model.relations if relation.id in view.relations}
    rendered_flows = [node for node in nodes if node.attrib.get('data-kind') in {'control-flow', 'object-flow'}]
    if len(rendered_flows) != len(expected_relations):
        diagnostics.append(Diagnostic('Q4', 'flow-count', f'Expected {len(expected_relations)} rendered flows, found {len(rendered_flows)}'))
    labels = {node.attrib.get('data-relation-id'): node.attrib.get('aria-label') for node in nodes if node.attrib.get('data-kind') == 'guard-label'}
    by_id = model.by_id
    for node in rendered_flows:
        identifier = node.attrib.get('data-semantic-id')
        relation = expected_relations.get(identifier)
        if relation is None:
            diagnostics.append(Diagnostic('Q4', 'unknown-flow', 'Rendered flow is not in model', subject=identifier))
            continue
        expected_kind = 'object-flow' if relation.type == 'object_flow' else 'control-flow'
        if node.attrib.get('data-kind') != expected_kind:
            diagnostics.append(Diagnostic('Q4', 'flow-kind', 'Rendered flow kind differs from model', subject=identifier))
        if node.attrib.get('data-source') != relation.source or node.attrib.get('data-target') != relation.target:
            diagnostics.append(Diagnostic('Q4', 'flow-direction', 'Rendered flow endpoints differ from model', subject=identifier))
        if relation.type == 'control_flow' and by_id[relation.source].type == 'decision' and labels.get(identifier) != relation.name:
            diagnostics.append(Diagnostic('Q4', 'decision-guard-label', 'Decision guard label differs from model', subject=identifier))
    text = svg_path.read_text(encoding='utf-8')
    if view.title not in text:
        diagnostics.append(Diagnostic('Q5', 'missing-title', 'Exact Activity Diagram title is absent from SVG'))
    use_case = view.options.get('useCase')
    if use_case and use_case not in text:
        diagnostics.append(Diagnostic('Q5', 'missing-process-name', 'Use Case name is absent from process frame'))
    if 'class="process-frame"' not in text:
        diagnostics.append(Diagnostic('Q5', 'missing-process-frame', 'Lecturer-style rounded Activity/Process frame is absent'))
    if 'marker-end="url(#activity-arrow)"' not in text:
        diagnostics.append(Diagnostic('Q5', 'missing-arrowheads', 'Activity Control Flows need directed arrowheads'))
    allowed_kinds = {'initial', 'final', 'action', 'object', 'decision', 'merge', 'fork', 'join', 'note', 'control-flow', 'object-flow', 'guard-label'}
    for node in nodes:
        kind = node.attrib.get('data-kind')
        if kind and kind not in allowed_kinds:
            diagnostics.append(Diagnostic('Q5', 'mixed-notation', f'Unexpected notation kind: {kind}'))
    for forbidden in ('lifeline', 'message-label', 'actor-head', 'participant-box', 'alt-fragment', 'usecase', '&lt;&lt;include&gt;&gt;', '&lt;&lt;extend&gt;&gt;', '#FFF7D6', '#163D59'):
        if forbidden in text:
            diagnostics.append(Diagnostic('Q5', 'mixed-notation', f'Forbidden old/non-activity notation found: {forbidden}'))
    rendered_names = {node.attrib.get(key) for node in nodes for key in ('data-action-name', 'data-object-name', 'data-node-name') if node.attrib.get(key)}
    for prohibited in view.options.get('prohibitedNodeNames', []):
        if prohibited in rendered_names:
            diagnostics.append(Diagnostic('Q5', 'prohibited-node', f'Prohibited Activity node rendered: {prohibited}'))
    return diagnostics
