from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)


@dataclass(frozen=True)
class Layout:
    width: int = 7500
    height: int = 5303
    title_y: int = 150
    header_y: int = 290
    lifeline_top: int = 625
    lifeline_bottom: int = 5050
    message_start: int = 820
    message_end: int = 4920


def tag(name: str) -> str:
    return f'{{{SVG}}}{name}'


def add_text(parent, text: str, x: float, y: float, css: str, anchor: str = 'start'):
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{y:g}', 'class': css, 'text-anchor': anchor})
    node.text = text
    return node


def wrap(text: str, max_chars: int) -> list[str]:
    words, lines, line = text.split(), [], ''
    for word in words:
        candidate = word if not line else f'{line} {word}'
        if line and len(candidate) > max_chars:
            lines.append(line); line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or ['']


def _positions(participants: list, layout: Layout) -> tuple[dict[str, float], dict[str, float]]:
    count = len(participants)
    left, right = 520, layout.width - 520
    spacing = (right - left) / max(1, count - 1)
    xs = {item.id: left + index * spacing for index, item in enumerate(participants)}
    # Keep boxes inside their allocation when a diagram has many lifelines.
    # This preserves readable typography while avoiding header overlap in SD-05.
    width_cap = max(650, min(1320, spacing - 85))
    widths = {item.id: min(width_cap, max(650, 360 + 31 * len(item.name))) for item in participants}
    return xs, widths


def _message_y(relations: list, layout: Layout) -> dict[str, float]:
    if not relations:
        return {}
    if len(relations) == 1:
        return {relations[0].id: layout.message_start}
    row = min(145, (layout.message_end - layout.message_start) / (len(relations) - 1))
    return {relation.id: layout.message_start + index * row for index, relation in enumerate(relations)}


def _activation_intervals(relations: list, ys: dict[str, float], participants: dict[str, object], row: float) -> list[tuple[str, float, float, float]]:
    intervals: list[tuple[str, float, float, float]] = []
    for relation in relations:
        target = participants[relation.target]
        if target.type != 'actor' and relation.type == 'message':
            offset = 23 if relation.source == relation.target else 0
            intervals.append((relation.target, ys[relation.id] - 12, min(ys[relation.id] + row * 0.82, ys[relation.id] + 105), offset))
    return intervals


def _draw_label(parent, number: int, label: str, x1: float, x2: float, y: float):
    visible = f'{number}. {label}'
    max_chars = max(20, min(54, int(abs(x2 - x1) / 21)))
    lines = wrap(visible, max_chars)
    width = min(max(300, max(len(line) for line in lines) * 24 + 42), max(360, abs(x2 - x1) - 46))
    height = 48 * len(lines) + 20
    x = (x1 + x2) / 2 - width / 2
    ET.SubElement(parent, tag('rect'), {'x':f'{x:g}', 'y':f'{y-height-13:g}', 'width':f'{width:g}', 'height':f'{height:g}', 'rx':'5', 'class':'label-bg'})
    text = ET.SubElement(parent, tag('text'), {'x':f'{(x1+x2)/2:g}', 'y':f'{y-height+18:g}', 'class':'message-label', 'text-anchor':'middle'})
    for index, line in enumerate(lines):
        span = ET.SubElement(text, tag('tspan'), {'x':f'{(x1+x2)/2:g}', **({'dy':'48'} if index else {})})
        span.text = line


def _draw_self_label(parent, number: int, label: str, x: float, y: float):
    visible = f'{number}. {label}'
    lines = wrap(visible, 24)
    width = max(420, min(650, max(len(line) for line in lines) * 24 + 42))
    height = 48 * len(lines) + 20
    ET.SubElement(parent, tag('rect'), {'x':f'{x:g}', 'y':f'{y+8:g}', 'width':f'{width:g}', 'height':f'{height:g}', 'rx':'5', 'class':'label-bg'})
    text = ET.SubElement(parent, tag('text'), {'x':f'{x+width/2:g}', 'y':f'{y+43:g}', 'class':'message-label', 'text-anchor':'middle'})
    for index, line in enumerate(lines):
        span = ET.SubElement(text, tag('tspan'), {'x':f'{x+width/2:g}', **({'dy':'48'} if index else {})})
        span.text = line


def _draw_actor(parent, item, x: float, layout: Layout):
    group = ET.SubElement(parent, tag('g'), {'id':item.id, 'data-kind':'lifeline', 'data-semantic-id':item.id, 'aria-label':item.name})
    ET.SubElement(group, tag('circle'), {'cx':str(x),'cy':'315','r':'25','class':'actor-head'})
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':'340','x2':str(x),'y2':'414','class':'actor-stroke'})
    ET.SubElement(group, tag('line'), {'x1':str(x-43),'y1':'367','x2':str(x+43),'y2':'367','class':'actor-stroke'})
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':'414','x2':str(x-38),'y2':'465','class':'actor-stroke'})
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':'414','x2':str(x+38),'y2':'465','class':'actor-stroke'})
    width = max(560, 34 * len(item.name) + 110)
    ET.SubElement(group, tag('rect'), {'x':str(x-width/2),'y':'478','width':str(width),'height':'80','rx':'8','class':'actor-label'})
    add_text(group, item.name, x, 530, 'participant-name', 'middle')
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':str(layout.lifeline_top),'x2':str(x),'y2':str(layout.lifeline_bottom),'class':'lifeline'})


def _draw_object(parent, item, x: float, width: float, layout: Layout):
    group = ET.SubElement(parent, tag('g'), {'id':item.id, 'data-kind':'lifeline', 'data-semantic-id':item.id, 'aria-label':item.name})
    ET.SubElement(group, tag('rect'), {'x':str(x-width/2),'y':str(layout.header_y),'width':str(width),'height':'210','rx':'8','class':'participant-box'})
    add_text(group, item.name, x, 420, 'participant-name', 'middle')
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':str(layout.lifeline_top),'x2':str(x),'y2':str(layout.lifeline_bottom),'class':'lifeline'})


def _draw_message(parent, relation, y: float, x1: float, x2: float):
    sequence = relation.metadata['sequence']
    group = ET.SubElement(parent, tag('g'), {'id':relation.id, 'data-kind':'message', 'data-semantic-id':relation.id, 'data-sequence':str(sequence), 'data-style':'dashed-return' if relation.type == 'return_message' else 'solid-request'})
    dashed = relation.type == 'return_message'
    if relation.source == relation.target:
        right = x1 + 210
        attrs = {'d':f'M {x1+14:g} {y:g} H {right:g} V {y+66:g} H {x1+14:g}', 'class':'message-line self-message', 'marker-end':'url(#open-arrow)' if dashed else 'url(#solid-arrow)'}
        if dashed: attrs['stroke-dasharray'] = '13 10'
        ET.SubElement(group, tag('path'), attrs)
        _draw_self_label(group, sequence, relation.name, right + 34, y)
        return
    attrs = {'x1':f'{x1:g}','y1':f'{y:g}','x2':f'{x2:g}','y2':f'{y:g}', 'class':'message-line', 'marker-end':'url(#open-arrow)' if dashed else 'url(#solid-arrow)'}
    if dashed: attrs['stroke-dasharray'] = '13 10'
    ET.SubElement(group, tag('line'), attrs)
    _draw_label(group, sequence, relation.name, x1, x2, y)


def render_lecturer_sequence_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    participants = [item for item in model.elements if item.id in view.include]
    participant_by_id = {item.id: item for item in participants}
    relation_by_id = {item.id: item for item in model.relations}
    relations = sorted((relation_by_id[item_id] for item_id in view.relations), key=lambda item: item.metadata['sequence'])
    if len(relations) < 1:
        raise ValueError('Lecturer-style sequence requires at least one message')
    layout = Layout()
    xs, widths = _positions(participants, layout)
    ys = _message_y(relations, layout)
    row = (layout.message_end - layout.message_start) / max(1, len(relations) - 1)
    root = ET.Element(tag('svg'), {'width':str(layout.width),'height':str(layout.height),'viewBox':f'0 0 {layout.width} {layout.height}','role':'img','aria-labelledby':'diagram-title diagram-description'})
    title = ET.SubElement(root, tag('title'), {'id':'diagram-title'}); title.text = view.title
    desc = ET.SubElement(root, tag('desc'), {'id':'diagram-description'}); desc.text = f'Lecturer-style UML Sequence Diagram with {len(participants)} lifelines and {len(relations)} numbered main-success interactions.'
    defs = ET.SubElement(root, tag('defs'))
    style = ET.SubElement(defs, tag('style'))
    style.text = '''
      .page { fill:#FFFFFF; } .page-border { fill:none; stroke:#D9E2EC; stroke-width:2; }
      .participant-box { stroke:#244C68; stroke-width:3; fill:#F5F8FC; } .participant-name { font-family:Arial,sans-serif; font-size:49px; font-weight:700; fill:#132C45; }
      .actor-head { fill:#FFFFFF; stroke:#132C45; stroke-width:4; } .actor-stroke { stroke:#132C45; stroke-width:4; stroke-linecap:round; } .actor-label { fill:#F5F8FC; stroke:#244C68; stroke-width:3; }
      .lifeline { stroke:#6B7C8E; stroke-width:2.2; stroke-dasharray:13 11; } .activation { fill:#E8F2FC; stroke:#326C96; stroke-width:2; }
      .message-line { stroke:#162F46; stroke-width:3; fill:none; stroke-linecap:round; } .self-message { stroke:#162F46; stroke-width:3; fill:none; stroke-linejoin:round; }
      .label-bg { fill:#FFFFFF; opacity:.98; } .message-label { font-family:Arial,sans-serif; font-size:45px; font-weight:600; fill:#102A43; }
      .page-title { font-family:Arial,sans-serif; font-size:76px; font-weight:700; fill:#132C45; }
    '''
    solid = ET.SubElement(defs, tag('marker'), {'id':'solid-arrow','markerWidth':'13','markerHeight':'11','refX':'11','refY':'5.5','orient':'auto','markerUnits':'strokeWidth'})
    ET.SubElement(solid, tag('path'), {'d':'M 0 0 L 12 5.5 L 0 11 Z','fill':'#162F46'})
    opened = ET.SubElement(defs, tag('marker'), {'id':'open-arrow','markerWidth':'14','markerHeight':'12','refX':'12','refY':'6','orient':'auto','markerUnits':'strokeWidth'})
    ET.SubElement(opened, tag('path'), {'d':'M 0 0 L 12 6 L 0 12','fill':'none','stroke':'#162F46','stroke-width':'2'})
    ET.SubElement(root, tag('rect'), {'x':'0','y':'0','width':str(layout.width),'height':str(layout.height),'class':'page'})
    ET.SubElement(root, tag('rect'), {'x':'55','y':'55','width':str(layout.width-110),'height':str(layout.height-110),'rx':'14','class':'page-border'})
    add_text(root, view.title, layout.width/2, layout.title_y, 'page-title', 'middle')
    participant_group = ET.SubElement(root, tag('g'), {'aria-label':'Sequence participants and lifelines'})
    for item in participants:
        if item.type == 'actor': _draw_actor(participant_group, item, xs[item.id], layout)
        else: _draw_object(participant_group, item, xs[item.id], widths[item.id], layout)
    activation_group = ET.SubElement(root, tag('g'), {'aria-label':'Meaningful activation bars'})
    for item_id, y0, y1, offset in _activation_intervals(relations, ys, participant_by_id, row):
        x = xs[item_id] + offset
        ET.SubElement(activation_group, tag('rect'), {'x':str(x-16),'y':str(y0),'width':'32','height':str(y1-y0),'class':'activation'})
    message_group = ET.SubElement(root, tag('g'), {'aria-label':'Numbered main-success messages'})
    for relation in relations:
        _draw_message(message_group, relation, ys[relation.id], xs[relation.source], xs[relation.target])
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
