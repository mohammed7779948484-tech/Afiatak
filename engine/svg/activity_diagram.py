from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.activity_diagram_layouts_v3 import layout_for
from engine.core.models import SemanticModel, ViewSpec

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)


def tag(name: str) -> str:
    return f'{{{SVG}}}{name}'


def wrap(text: str, maximum: int) -> list[str]:
    words, lines, line = text.split(), [], ''
    for word in words:
        candidate = word if not line else f'{line} {word}'
        if line and len(candidate) > maximum:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or ['']


def add_text(parent, text: str, x: float, y: float, css: str, anchor: str = 'middle'):
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{y:g}', 'class': css, 'text-anchor': anchor})
    node.text = text
    return node


def draw_wrapped(parent, text: str, x: float, centre_y: float, css: str, maximum: int, line_height: int):
    lines = wrap(text, maximum)
    start_y = centre_y - (len(lines) - 1) * line_height / 2 + 14
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{start_y:g}', 'class': css, 'text-anchor': 'middle'})
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag('tspan'), {'x': f'{x:g}', **({'dy': str(line_height)} if index else {})})
        span.text = line
    return node


def visible_name(item) -> str:
    label = item.metadata.get('visibleLabel')
    return label if isinstance(label, str) else item.name


def draw_initial(parent, item, x: float, y: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'initial', 'data-semantic-id': item.id, 'aria-label': 'Initial Node'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '32', 'class': 'initial-node'})


def draw_final(parent, item, x: float, y: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'final', 'data-semantic-id': item.id, 'aria-label': 'Activity Final'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '50', 'class': 'final-ring'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '27', 'class': 'final-core'})


def draw_action(parent, item, x: float, y: float, width: float, height: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'action', 'data-semantic-id': item.id, 'data-action-name': visible_name(item), 'aria-label': visible_name(item)})
    ET.SubElement(group, tag('rect'), {'x': f'{x:g}', 'y': f'{y:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'rx': '26', 'class': 'action-box'})
    draw_wrapped(group, visible_name(item), x + width / 2, y + height / 2, 'action-text', 38, 62)


def draw_object(parent, item, x: float, y: float, width: float, height: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'object', 'data-semantic-id': item.id, 'data-object-name': visible_name(item), 'aria-label': visible_name(item)})
    ET.SubElement(group, tag('rect'), {'x': f'{x:g}', 'y': f'{y:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'class': 'object-box'})
    draw_wrapped(group, visible_name(item), x + width / 2, y + height / 2, 'object-text', 30, 54)


def draw_diamond(parent, item, x: float, y: float, width: float, height: float, *, kind: str):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': kind, 'data-semantic-id': item.id, 'data-node-name': visible_name(item), 'aria-label': visible_name(item)})
    points = f'{x + width / 2:g},{y:g} {x + width:g},{y + height / 2:g} {x + width / 2:g},{y + height:g} {x:g},{y + height / 2:g}'
    ET.SubElement(group, tag('polygon'), {'points': points, 'class': 'decision-box' if kind == 'decision' else 'merge-box'})
    if kind == 'decision' or item.metadata.get('visibleLabel', True):
        maximum = max(18, int((width - 90) / 29))
        draw_wrapped(group, visible_name(item), x + width / 2, y + height / 2, 'decision-text' if kind == 'decision' else 'merge-text', maximum, 42)


def draw_note(parent, item, x: float, y: float, width: float, height: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'note', 'data-semantic-id': item.id, 'data-note-name': visible_name(item), 'aria-label': visible_name(item)})
    fold = min(56, height / 3)
    outline = f'M {x:g} {y:g} H {x + width - fold:g} L {x + width:g} {y + fold:g} V {y + height:g} H {x:g} Z'
    ET.SubElement(group, tag('path'), {'d': outline, 'class': 'note-box'})
    ET.SubElement(group, tag('polyline'), {'points': f'{x + width - fold:g},{y:g} {x + width - fold:g},{y + fold:g} {x + width:g},{y + fold:g}', 'class': 'note-fold'})
    draw_wrapped(group, visible_name(item), x + width / 2, y + height / 2, 'note-text', 36, 38)


def draw_bar(parent, item, x: float, y: float, width: float, height: float, kind: str):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': kind, 'data-semantic-id': item.id, 'aria-label': kind.title()})
    ET.SubElement(group, tag('rect'), {'x': f'{x:g}', 'y': f'{y:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'class': 'fork-join'})


def label_size(text: str) -> tuple[float, float]:
    lines = wrap(text, 30)
    return max(230, min(900, max(len(line) for line in lines) * 25 + 48)), 46 * len(lines) + 28


def draw_edge(parent, relation, route):
    edge_type = 'object-flow' if relation.type == 'object_flow' else 'control-flow'
    group = ET.SubElement(parent, tag('g'), {'id': relation.id, 'data-kind': edge_type, 'data-semantic-id': relation.id, 'data-source': relation.source, 'data-target': relation.target, 'aria-label': relation.name or edge_type})
    points = ' '.join(f'{x:g},{y:g}' for x, y in route['points'])
    marker = 'url(#object-arrow)' if edge_type == 'object-flow' else 'url(#activity-arrow)'
    ET.SubElement(group, tag('polyline'), {'points': points, 'class': edge_type, 'marker-end': marker})


def draw_guard(parent, relation, route):
    if not relation.name or not relation.metadata.get('visibleLabel', True):
        return
    x, y = route['label']
    width, height = label_size(relation.name)
    group = ET.SubElement(parent, tag('g'), {'data-kind': 'guard-label', 'data-relation-id': relation.id, 'aria-label': relation.name})
    ET.SubElement(group, tag('rect'), {'x': f'{x - width / 2:g}', 'y': f'{y - height / 2:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'class': 'label-bg'})
    node = ET.SubElement(group, tag('text'), {'x': f'{x:g}', 'y': f'{y - height / 2 + 34:g}', 'class': 'guard-text', 'text-anchor': 'middle'})
    for index, line in enumerate(wrap(relation.name, 30)):
        span = ET.SubElement(node, tag('tspan'), {'x': f'{x:g}', **({'dy': '46'} if index else {})})
        span.text = line


def render_activity_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout, composition = layout_for(view.id)
    visible = {item.id: item for item in model.elements if item.id in view.include}
    relation_map = {relation.id: relation for relation in model.relations}
    relations = [relation_map[relation_id] for relation_id in view.relations]
    maximum_raster_dimension = 8192
    scale = min(1.0, maximum_raster_dimension / max(layout.width, layout.height))
    root = ET.Element(tag('svg'), {'width': str(round(layout.width * scale)), 'height': str(round(layout.height * scale)), 'viewBox': f'0 0 {layout.width} {layout.height}', 'role': 'img', 'aria-labelledby': 'diagram-title diagram-description'})
    title = ET.SubElement(root, tag('title'), {'id': 'diagram-title'}); title.text = view.title
    desc = ET.SubElement(root, tag('desc'), {'id': 'diagram-description'}); desc.text = f'Lecturer page-11 style UML Activity Diagram for {view.options.get("useCase", "the selected Use Case")}.'
    defs = ET.SubElement(root, tag('defs'))
    style = ET.SubElement(defs, tag('style'))
    style.text = '''
      .page { fill:#FFFFFF; } .process-frame { fill:none; stroke:#111111; stroke-width:5; }
      .page-title { font-family:Arial,sans-serif; font-size:62px; font-weight:700; fill:#111111; }
      .frame-title { font-family:Arial,sans-serif; font-size:60px; font-weight:700; fill:#111111; }
      .action-box { fill:#F6F6F6; stroke:#111111; stroke-width:4; } .action-text { font-family:Arial,sans-serif; font-size:56px; font-weight:500; fill:#111111; }
      .object-box { fill:#FFFFFF; stroke:#111111; stroke-width:4; } .object-text { font-family:Arial,sans-serif; font-size:48px; font-weight:500; fill:#111111; }
      .decision-box,.merge-box { fill:#FFFFFF; stroke:#111111; stroke-width:4; } .decision-text { font-family:Arial,sans-serif; font-size:46px; font-weight:600; fill:#111111; } .merge-text { font-family:Arial,sans-serif; font-size:34px; fill:#111111; }
      .initial-node,.final-core { fill:#000000; stroke:#000000; stroke-width:3; } .final-ring { fill:#FFFFFF; stroke:#000000; stroke-width:6; }
      .control-flow,.object-flow { fill:none; stroke:#111111; stroke-width:4; stroke-linejoin:round; stroke-linecap:round; } .object-flow { stroke-width:4; }
      .fork-join { fill:#000000; stroke:#000000; }
      .label-bg { fill:#FFFFFF; opacity:.96; } .guard-text { font-family:Arial,sans-serif; font-size:43px; font-weight:500; fill:#111111; }
      .note-box { fill:#FFFFFF; stroke:#333333; stroke-width:3; } .note-fold { fill:none; stroke:#333333; stroke-width:3; } .note-text { font-family:Arial,sans-serif; font-size:36px; font-style:italic; fill:#222222; }
    '''
    for marker_id in ('activity-arrow', 'object-arrow'):
        marker = ET.SubElement(defs, tag('marker'), {'id': marker_id, 'viewBox': '0 0 16 14', 'markerWidth': '42', 'markerHeight': '37', 'refX': '16', 'refY': '7', 'orient': 'auto', 'markerUnits': 'userSpaceOnUse'})
        ET.SubElement(marker, tag('path'), {'d': 'M 1 1 L 16 7 L 1 13 Z', 'fill': '#111111'})
    ET.SubElement(root, tag('rect'), {'x': '0', 'y': '0', 'width': str(layout.width), 'height': str(layout.height), 'class': 'page'})
    frame = composition.get('frame', {'x': 150, 'y': 230, 'width': layout.width - 300, 'height': layout.height - 380})
    ET.SubElement(root, tag('rect'), {'x': str(frame['x']), 'y': str(frame['y']), 'width': str(frame['width']), 'height': str(frame['height']), 'rx': '70', 'class': 'process-frame'})
    add_text(root, view.title, layout.width / 2, 110, 'page-title')
    add_text(root, view.options.get('useCase', view.title.replace('Activity Diagram — ', '')), frame['x'] + 100, frame['y'] + 95, 'frame-title', 'start')
    edge_layer = ET.SubElement(root, tag('g'), {'aria-label': 'Activity flows'})
    for relation in relations:
        draw_edge(edge_layer, relation, composition['routes'][relation.id])
    node_layer = ET.SubElement(root, tag('g'), {'aria-label': 'Activity nodes'})
    for semantic_id, (x, y) in composition.get('initial', {}).items(): draw_initial(node_layer, visible[semantic_id], x, y)
    for semantic_id, (x, y) in composition.get('actions', {}).items(): draw_action(node_layer, visible[semantic_id], x, y, layout.action_width, layout.action_height)
    for semantic_id, (x, y, width, height) in composition.get('objects', {}).items(): draw_object(node_layer, visible[semantic_id], x, y, width, height)
    for semantic_id, (x, y) in composition.get('decisions', {}).items(): draw_diamond(node_layer, visible[semantic_id], x, y, layout.decision_width, layout.decision_height, kind='decision')
    for semantic_id, (x, y) in composition.get('merges', {}).items(): draw_diamond(node_layer, visible[semantic_id], x, y, layout.decision_width * .56, layout.decision_height * .56, kind='merge')
    for semantic_id, (x, y, width, height) in composition.get('forks', {}).items(): draw_bar(node_layer, visible[semantic_id], x, y, width, height, 'fork')
    for semantic_id, (x, y, width, height) in composition.get('joins', {}).items(): draw_bar(node_layer, visible[semantic_id], x, y, width, height, 'join')
    for semantic_id, (x, y) in composition.get('notes', {}).items(): draw_note(node_layer, visible[semantic_id], x, y, layout.note_width, layout.note_height)
    for semantic_id, (x, y) in composition.get('final', {}).items(): draw_final(node_layer, visible[semantic_id], x, y)
    label_layer = ET.SubElement(root, tag('g'), {'aria-label': 'Decision guards'})
    for relation in relations: draw_guard(label_layer, relation, composition['routes'][relation.id])
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
