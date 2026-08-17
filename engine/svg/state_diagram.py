from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.state_diagram_layouts import layout_for
from engine.core.models import SemanticModel, ViewSpec

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)


def tag(name: str) -> str:
    return f'{{{SVG}}}{name}'


def add_text(parent, text: str, x: float, y: float, css: str, anchor: str = 'start'):
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{y:g}', 'class': css, 'text-anchor': anchor})
    node.text = text
    return node


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


def draw_wrapped(parent, text: str, x: float, y: float, css: str, maximum: int, line_height: int, anchor: str = 'middle'):
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{y:g}', 'class': css, 'text-anchor': anchor})
    for index, line in enumerate(wrap(text, maximum)):
        span = ET.SubElement(node, tag('tspan'), {'x': f'{x:g}', **({'dy': str(line_height)} if index else {})})
        span.text = line
    return node


def _label(parent, text: str, x: float, y: float):
    lines = wrap(text, 42)
    width = max(480, min(1300, max(len(line) for line in lines) * 33 + 70))
    height = 62 * len(lines) + 40
    group = ET.SubElement(parent, tag('g'), {'class': 'transition-label'})
    ET.SubElement(group, tag('rect'), {'x': f'{x-width/2:g}', 'y': f'{y-height/2:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'rx': '8', 'class': 'label-bg'})
    node = ET.SubElement(group, tag('text'), {'x': f'{x:g}', 'y': f'{y-height/2+46:g}', 'class': 'transition-text', 'text-anchor': 'middle'})
    for index, line in enumerate(lines):
        span = ET.SubElement(node, tag('tspan'), {'x': f'{x:g}', **({'dy': '62'} if index else {})})
        span.text = line


def _draw_state(parent, item, x: float, y: float, width: float, height: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'state', 'data-semantic-id': item.id, 'data-state-name': item.name, 'aria-label': item.name})
    ET.SubElement(group, tag('rect'), {'x': f'{x:g}', 'y': f'{y:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'rx': '34', 'class': 'state-box'})
    activity = str(item.metadata.get('do', '')).strip()
    if activity:
        ET.SubElement(group, tag('line'), {'x1': f'{x+60:g}', 'y1': f'{y+height/2:g}', 'x2': f'{x+width-60:g}', 'y2': f'{y+height/2:g}', 'class': 'state-divider'})
        add_text(group, item.name, x + width / 2, y + height / 2 - 42, 'state-name', 'middle')
        draw_wrapped(group, f'do / {activity}', x + width / 2, y + height / 2 + 72, 'state-activity', 42, 46)
    else:
        add_text(group, item.name, x + width / 2, y + height / 2 + 25, 'state-name', 'middle')


def _draw_initial(parent, item, x: float, y: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'initial', 'data-semantic-id': item.id, 'aria-label': 'Initial pseudostate'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '38', 'class': 'initial-node'})


def _draw_final(parent, item, x: float, y: float):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'final', 'data-semantic-id': item.id, 'aria-label': 'Final pseudostate'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '52', 'class': 'final-ring'})
    ET.SubElement(group, tag('circle'), {'cx': f'{x:g}', 'cy': f'{y:g}', 'r': '29', 'class': 'initial-node'})


def _draw_transition(parent, relation, spec):
    points = spec['points']
    group = ET.SubElement(parent, tag('g'), {'id': relation.id, 'data-kind': 'transition', 'data-semantic-id': relation.id, 'data-source': relation.source, 'data-target': relation.target, 'aria-label': relation.name})
    point_string = ' '.join(f'{x:g},{y:g}' for x, y in points)
    ET.SubElement(group, tag('polyline'), {'points': point_string, 'class': 'transition-line', 'marker-end': 'url(#state-arrow)'})
    if relation.metadata.get('visibleLabel', True):
        _label(group, relation.name, *spec['label'])


def render_state_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout, composition = layout_for(view.id)
    visible = {item.id: item for item in model.elements if item.id in view.include}
    relation_by_id = {item.id: item for item in model.relations}
    relations = [relation_by_id[item_id] for item_id in view.relations]
    root = ET.Element(tag('svg'), {'width': str(layout.width), 'height': str(layout.height), 'viewBox': f'0 0 {layout.width} {layout.height}', 'role': 'img', 'aria-labelledby': 'diagram-title diagram-description'})
    title = ET.SubElement(root, tag('title'), {'id': 'diagram-title'}); title.text = view.title
    desc = ET.SubElement(root, tag('desc'), {'id': 'diagram-description'}); desc.text = f'Lecturer-style UML State Diagram for the {view.options.get("modeledObject", "selected")} lifecycle.'
    defs = ET.SubElement(root, tag('defs'))
    style = ET.SubElement(defs, tag('style'))
    style.text = '''
      .page { fill:#FFFFFF; } .page-border { fill:none; stroke:#D9E2EC; stroke-width:2; }
      .page-title { font-family:Arial,sans-serif; font-size:76px; font-weight:700; fill:#132C45; }
      .state-box { fill:#F6F9FC; stroke:#163D59; stroke-width:5; } .state-divider { stroke:#9FB3C8; stroke-width:2.5; }
      .state-name { font-family:Arial,sans-serif; font-size:64px; font-weight:700; fill:#102A43; } .state-activity { font-family:Arial,sans-serif; font-size:46px; font-style:italic; fill:#274C63; }
      .initial-node { fill:#102A43; stroke:#102A43; stroke-width:4; } .final-ring { fill:#FFFFFF; stroke:#102A43; stroke-width:7; }
      .transition-line { fill:none; stroke:#102A43; stroke-width:5; stroke-linejoin:round; stroke-linecap:round; }
      .label-bg { fill:#FFFFFF; opacity:.98; } .transition-text { font-family:Arial,sans-serif; font-size:44px; font-weight:600; fill:#102A43; }
    '''
    marker = ET.SubElement(defs, tag('marker'), {'id': 'state-arrow', 'markerWidth': '16', 'markerHeight': '14', 'refX': '14', 'refY': '7', 'orient': 'auto', 'markerUnits': 'strokeWidth'})
    ET.SubElement(marker, tag('path'), {'d': 'M 0 0 L 15 7 L 0 14 Z', 'fill': '#102A43'})
    ET.SubElement(root, tag('rect'), {'x': '0', 'y': '0', 'width': str(layout.width), 'height': str(layout.height), 'class': 'page'})
    ET.SubElement(root, tag('rect'), {'x': '55', 'y': '55', 'width': str(layout.width - 110), 'height': str(layout.height - 110), 'rx': '14', 'class': 'page-border'})
    add_text(root, view.title, layout.width / 2, layout.title_y, 'page-title', 'middle')
    nodes = ET.SubElement(root, tag('g'), {'aria-label': 'State lifecycle nodes'})
    for item_id, (x, y) in composition.get('initial', {}).items():
        _draw_initial(nodes, visible[item_id], x, y)
    for item_id, (x, y) in composition.get('states', {}).items():
        _draw_state(nodes, visible[item_id], x, y, layout.state_width, layout.state_height)
    for item_id, (x, y) in composition.get('final', {}).items():
        _draw_final(nodes, visible[item_id], x, y)
    edges = ET.SubElement(root, tag('g'), {'aria-label': 'Labeled state transitions'})
    for relation in relations:
        _draw_transition(edges, relation, composition['routes'][relation.id])
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
