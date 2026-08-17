from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.activity_diagram_layouts import layout_for
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
    start_y = centre_y - (len(lines) - 1) * line_height / 2 + 16
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{start_y:g}', 'class': css, 'text-anchor': 'middle'})
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag('tspan'), {'x': f'{x:g}', **({'dy': str(line_height)} if index else {})})
        span.text = line
    return node


def draw_initial(parent, item, x: float, y: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'initial', 'data-semantic-id': item.id, 'aria-label': 'Initial Node'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '38', 'class': 'initial-node'})


def draw_final(parent, item, x: float, y: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'final', 'data-semantic-id': item.id, 'aria-label': 'Activity Final'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '54', 'class': 'final-ring'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '29', 'class': 'final-core'})


def draw_action(parent, item, x: float, y: float, width: float, height: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'action', 'data-semantic-id': item.id, 'data-action-name': item.name, 'aria-label': item.name})
    ET.SubElement(group, tag('rect'), {'x': f'{x:g}', 'y': f'{y:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'rx': '34', 'class': 'action-box'})
    draw_wrapped(group, item.name, x + width / 2, y + height / 2, 'action-text', 46, 76)


def draw_diamond(parent, item, x: float, y: float, width: float, height: float, *, kind: str):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': kind, 'data-semantic-id': item.id, 'data-node-name': item.name, 'aria-label': item.name})
    points = f'{x + width / 2:g},{y:g} {x + width:g},{y + height / 2:g} {x + width / 2:g},{y + height:g} {x:g},{y + height / 2:g}'
    css = 'decision-box' if kind == 'decision' else 'merge-box'
    ET.SubElement(group, tag('polygon'), {'points': points, 'class': css})
    if kind == 'decision' or item.metadata.get('visibleLabel', True):
        maximum = max(22, int((width - 100) / 30))
        draw_wrapped(group, item.name, x + width / 2, y + height / 2, 'decision-text' if kind == 'decision' else 'merge-text', maximum, 46)


def draw_note(parent, item, x: float, y: float, width: float, height: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'note', 'data-semantic-id': item.id, 'data-note-name': item.name, 'aria-label': item.name})
    fold = min(70, height / 3)
    outline = f'M {x:g} {y:g} H {x + width - fold:g} L {x + width:g} {y + fold:g} V {y + height:g} H {x:g} Z'
    ET.SubElement(group, tag('path'), {'d': outline, 'class': 'note-box'})
    ET.SubElement(group, tag('polyline'), {'points': f'{x + width - fold:g},{y:g} {x + width - fold:g},{y + fold:g} {x + width:g},{y + fold:g}', 'class': 'note-fold'})
    draw_wrapped(group, item.name, x + width / 2, y + height / 2, 'note-text', 42, 42)


def label_size(text: str) -> tuple[float, float, list[str]]:
    lines = wrap(text, 34)
    width = max(280, min(1050, max(len(line) for line in lines) * 29 + 64))
    height = 52 * len(lines) + 34
    return width, height, lines


def draw_edge(parent, relation, route):
    group = ET.SubElement(parent, tag('g'), {'id': relation.id, 'data-kind': 'control-flow', 'data-semantic-id': relation.id, 'data-source': relation.source, 'data-target': relation.target, 'aria-label': relation.name or 'Control flow'})
    point_string = ' '.join(f'{x:g},{y:g}' for x, y in route['points'])
    ET.SubElement(group, tag('polyline'), {'points': point_string, 'class': 'control-flow', 'marker-end': 'url(#activity-arrow)'})
    return group


def draw_guard(parent, relation, route):
    if not relation.name or not relation.metadata.get('visibleLabel', True):
        return
    x, y = route['label']
    width, height, lines = label_size(relation.name)
    group = ET.SubElement(parent, tag('g'), {'data-kind': 'guard-label', 'data-relation-id': relation.id, 'aria-label': relation.name})
    ET.SubElement(group, tag('rect'), {'x': f'{x - width / 2:g}', 'y': f'{y - height / 2:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'rx': '8', 'class': 'label-bg'})
    node = ET.SubElement(group, tag('text'), {'x': f'{x:g}', 'y': f'{y - height / 2 + 38:g}', 'class': 'guard-text', 'text-anchor': 'middle'})
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag('tspan'), {'x': f'{x:g}', **({'dy': '52'} if index else {})})
        span.text = line


def render_activity_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout, composition = layout_for(view.id)
    visible = {item.id: item for item in model.elements if item.id in view.include}
    relations_by_id = {relation.id: relation for relation in model.relations}
    relations = [relations_by_id[relation_id] for relation_id in view.relations]

    # Preserve the authored vector coordinate system while limiting the physical raster
    # viewport to a browser-safe size. This avoids blank Chromium screenshots on very
    # large canvases while retaining full detail in SVG and vector PDF outputs.
    maximum_raster_dimension = 8192
    raster_scale = min(1.0, maximum_raster_dimension / max(layout.width, layout.height))
    raster_width = round(layout.width * raster_scale)
    raster_height = round(layout.height * raster_scale)
    root = ET.Element(tag('svg'), {'width': str(raster_width), 'height': str(raster_height), 'viewBox': f'0 0 {layout.width} {layout.height}', 'role': 'img', 'aria-labelledby': 'diagram-title diagram-description'})
    title = ET.SubElement(root, tag('title'), {'id': 'diagram-title'})
    title.text = view.title
    desc = ET.SubElement(root, tag('desc'), {'id': 'diagram-description'})
    desc.text = f'Lecturer-style UML Activity Diagram for {view.options.get("useCase", "the selected Use Case")}.'
    defs = ET.SubElement(root, tag('defs'))
    style = ET.SubElement(defs, tag('style'))
    style.text = '''
      .page { fill:#FFFFFF; } .page-border { fill:none; stroke:#D9E2EC; stroke-width:2; }
      .page-title { font-family:Arial,sans-serif; font-size:88px; font-weight:700; fill:#132C45; }
      .action-box { fill:#F6F9FC; stroke:#163D59; stroke-width:5; } .action-text { font-family:Arial,sans-serif; font-size:68px; font-weight:600; fill:#102A43; }
      .decision-box { fill:#FFF7D6; stroke:#9B6D05; stroke-width:5; } .decision-text { font-family:Arial,sans-serif; font-size:52px; font-weight:700; fill:#5D4300; }
      .merge-box { fill:#FFFFFF; stroke:#6B7C93; stroke-width:5; } .merge-text { font-family:Arial,sans-serif; font-size:38px; font-weight:600; fill:#334E68; }
      .initial-node,.final-core { fill:#102A43; stroke:#102A43; stroke-width:4; } .final-ring { fill:#FFFFFF; stroke:#102A43; stroke-width:7; }
      .control-flow { fill:none; stroke:#102A43; stroke-width:5; stroke-linejoin:round; stroke-linecap:round; }
      .label-bg { fill:#FFFFFF; opacity:.98; } .guard-text { font-family:Arial,sans-serif; font-size:52px; font-weight:700; fill:#102A43; }
      .note-box { fill:#FFFDF5; stroke:#8C7A48; stroke-width:3; } .note-fold { fill:none; stroke:#8C7A48; stroke-width:3; } .note-text { font-family:Arial,sans-serif; font-size:44px; font-style:italic; fill:#5D5435; }
    '''
    marker = ET.SubElement(defs, tag('marker'), {'id': 'activity-arrow', 'markerWidth': '16', 'markerHeight': '14', 'refX': '14', 'refY': '7', 'orient': 'auto', 'markerUnits': 'strokeWidth'})
    ET.SubElement(marker, tag('path'), {'d': 'M 0 0 L 15 7 L 0 14 Z', 'fill': '#102A43'})

    ET.SubElement(root, tag('rect'), {'x': '0', 'y': '0', 'width': str(layout.width), 'height': str(layout.height), 'class': 'page'})
    ET.SubElement(root, tag('rect'), {'x': '55', 'y': '55', 'width': str(layout.width - 110), 'height': str(layout.height - 110), 'rx': '14', 'class': 'page-border'})
    add_text(root, view.title, layout.width / 2, layout.title_y, 'page-title')

    edge_layer = ET.SubElement(root, tag('g'), {'aria-label': 'Activity control flows'})
    for relation in relations:
        draw_edge(edge_layer, relation, composition['routes'][relation.id])

    node_layer = ET.SubElement(root, tag('g'), {'aria-label': 'Activity nodes'})
    for semantic_id, (x, y) in composition.get('initial', {}).items():
        draw_initial(node_layer, visible[semantic_id], x, y)
    for semantic_id, (x, y) in composition.get('actions', {}).items():
        draw_action(node_layer, visible[semantic_id], x, y, layout.action_width, layout.action_height)
    for semantic_id, (x, y) in composition.get('decisions', {}).items():
        draw_diamond(node_layer, visible[semantic_id], x, y, layout.decision_width, layout.decision_height, kind='decision')
    for semantic_id, (x, y) in composition.get('merges', {}).items():
        draw_diamond(node_layer, visible[semantic_id], x, y, layout.decision_width * 0.62, layout.decision_height * 0.62, kind='merge')
    for semantic_id, (x, y) in composition.get('notes', {}).items():
        draw_note(node_layer, visible[semantic_id], x, y, layout.note_width, layout.note_height)
    for semantic_id, (x, y) in composition.get('final', {}).items():
        draw_final(node_layer, visible[semantic_id], x, y)

    label_layer = ET.SubElement(root, tag('g'), {'aria-label': 'Decision guards'})
    for relation in relations:
        draw_guard(label_layer, relation, composition['routes'][relation.id])

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
