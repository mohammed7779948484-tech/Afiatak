from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions import aafiatak_sd01_patient_registration_otp as composition
from engine.core.models import SemanticModel, ViewSpec

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)


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
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or ['']


def draw_label(parent, sequence: int, label: str, x1: float, x2: float, y: float):
    visible = f'{sequence}. {label}'
    max_chars = max(17, min(47, int(abs(x2 - x1) / 19)))
    lines = wrap(visible, max_chars)
    width = min(max(270, max(len(line) for line in lines) * 21 + 40), max(330, abs(x2 - x1) - 36))
    height = 40 * len(lines) + 18
    x = (x1 + x2) / 2 - width / 2
    ET.SubElement(parent, tag('rect'), {'x':f'{x:g}', 'y':f'{y-height-12:g}', 'width':f'{width:g}', 'height':f'{height:g}', 'rx':'5', 'class':'label-bg'})
    text = ET.SubElement(parent, tag('text'), {'x':f'{(x1+x2)/2:g}', 'y':f'{y-height+15:g}', 'class':'message-label', 'text-anchor':'middle'})
    for index, line in enumerate(lines):
        span = ET.SubElement(text, tag('tspan'), {'x':f'{(x1+x2)/2:g}', **({'dy':'40'} if index else {})})
        span.text = line


def draw_message(parent, source_id: str, target_id: str, y: float, label: str, relation_id: str, sequence: int, *, dashed: bool, self_message: bool = False):
    x1 = composition.PARTICIPANT_X[source_id]
    x2 = composition.PARTICIPANT_X[target_id]
    group = ET.SubElement(parent, tag('g'), {'id':relation_id, 'data-kind':'message', 'data-semantic-id':relation_id, 'data-sequence':str(sequence), 'data-style':'dashed-return' if dashed else 'solid-request'})
    if self_message:
        right = x1 + 185
        attrs = {'d':f'M {x1+14:g} {y:g} H {right:g} V {y+62:g} H {x1+14:g}', 'class':'message-line self-message', 'marker-end':'url(#open-arrow)' if dashed else 'url(#solid-arrow)'}
        if dashed:
            attrs['stroke-dasharray'] = '12 9'
        ET.SubElement(group, tag('path'), attrs)
        draw_label(group, sequence, label, x1+24, right+145, y+18)
        return
    attrs = {'x1':f'{x1:g}', 'y1':f'{y:g}', 'x2':f'{x2:g}', 'y2':f'{y:g}', 'class':'message-line', 'marker-end':'url(#open-arrow)' if dashed else 'url(#solid-arrow)'}
    if dashed:
        attrs['stroke-dasharray'] = '12 9'
    ET.SubElement(group, tag('line'), attrs)
    draw_label(group, sequence, label, x1, x2, y)


def draw_actor(parent, item_id: str, name: str):
    x = composition.PARTICIPANT_X[item_id]
    group = ET.SubElement(parent, tag('g'), {'id':item_id, 'data-kind':'lifeline', 'data-semantic-id':item_id, 'aria-label':name})
    ET.SubElement(group, tag('circle'), {'cx':str(x),'cy':'315','r':'24','class':'actor-head'})
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':'339','x2':str(x),'y2':'410','class':'actor-stroke'})
    ET.SubElement(group, tag('line'), {'x1':str(x-42),'y1':'365','x2':str(x+42),'y2':'365','class':'actor-stroke'})
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':'410','x2':str(x-38),'y2':'462','class':'actor-stroke'})
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':'410','x2':str(x+38),'y2':'462','class':'actor-stroke'})
    ET.SubElement(group, tag('rect'), {'x':str(x-300),'y':'475','width':'600','height':'82','rx':'8','class':'actor-label'})
    add_text(group, name, x, 528, 'participant-name', 'middle')
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':str(composition.LIFELINE_TOP),'x2':str(x),'y2':str(composition.LIFELINE_BOTTOM),'class':'lifeline'})


def draw_object(parent, item_id: str, name: str):
    x = composition.PARTICIPANT_X[item_id]
    width = composition.PARTICIPANT_WIDTH[item_id]
    group = ET.SubElement(parent, tag('g'), {'id':item_id, 'data-kind':'lifeline', 'data-semantic-id':item_id, 'aria-label':name})
    ET.SubElement(group, tag('rect'), {'x':str(x-width/2),'y':str(composition.HEADER_Y),'width':str(width),'height':'210','rx':'8','class':'participant-box'})
    add_text(group, name, x, 417, 'participant-name', 'middle')
    ET.SubElement(group, tag('line'), {'x1':str(x),'y1':str(composition.LIFELINE_TOP),'x2':str(x),'y2':str(composition.LIFELINE_BOTTOM),'class':'lifeline'})


def draw_activation(parent, participant_id: str, y0: float, y1: float, offset: float):
    x = composition.PARTICIPANT_X[participant_id] + offset
    ET.SubElement(parent, tag('rect'), {'x':str(x-15),'y':str(y0),'width':'30','height':str(y1-y0),'class':'activation'})


def render_sequence_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    selected = {item.id: item for item in model.elements if item.id in view.include}
    relation_map = {item.id: item for item in model.relations}
    relations = sorted((relation_map[item] for item in view.relations), key=lambda relation: relation.metadata['sequence'])
    if len(selected) != 5 or len(relations) != 19:
        raise ValueError('SD-01 requires exactly 5 lifelines and 19 main-flow messages')
    root = ET.Element(tag('svg'), {'width':str(composition.CANVAS[0]), 'height':str(composition.CANVAS[1]), 'viewBox':f'0 0 {composition.CANVAS[0]} {composition.CANVAS[1]}', 'role':'img', 'aria-labelledby':'diagram-title diagram-description'})
    title = ET.SubElement(root, tag('title'), {'id':'diagram-title'}); title.text = view.title
    description = ET.SubElement(root, tag('desc'), {'id':'diagram-description'}); description.text = 'Lecturer-style UML Sequence Diagram SD-01 with five lifelines and nineteen numbered main-success interactions.'
    defs = ET.SubElement(root, tag('defs'))
    style = ET.SubElement(defs, tag('style'))
    style.text = '''
      .page { fill:#FFFFFF; } .page-border { fill:none; stroke:#D9E2EC; stroke-width:2; }
      .participant-box { stroke:#244C68; stroke-width:3; fill:#F5F8FC; } .participant-name { font-family:Arial,sans-serif; font-size:40px; font-weight:700; fill:#132C45; }
      .actor-head { fill:#FFFFFF; stroke:#132C45; stroke-width:4; } .actor-stroke { stroke:#132C45; stroke-width:4; stroke-linecap:round; } .actor-label { fill:#F5F8FC; stroke:#244C68; stroke-width:3; }
      .lifeline { stroke:#6B7C8E; stroke-width:2.2; stroke-dasharray:12 10; } .activation { fill:#E8F2FC; stroke:#326C96; stroke-width:2; }
      .message-line { stroke:#162F46; stroke-width:3; fill:none; stroke-linecap:round; } .self-message { stroke:#162F46; stroke-width:3; fill:none; stroke-linejoin:round; }
      .label-bg { fill:#FFFFFF; opacity:.98; } .message-label { font-family:Arial,sans-serif; font-size:36px; font-weight:600; fill:#102A43; }
      .page-title { font-family:Arial,sans-serif; font-size:70px; font-weight:700; fill:#132C45; }
    '''
    solid = ET.SubElement(defs, tag('marker'), {'id':'solid-arrow', 'markerWidth':'13','markerHeight':'11','refX':'11','refY':'5.5','orient':'auto','markerUnits':'strokeWidth'})
    ET.SubElement(solid, tag('path'), {'d':'M 0 0 L 12 5.5 L 0 11 Z','fill':'#162F46'})
    open_arrow = ET.SubElement(defs, tag('marker'), {'id':'open-arrow', 'markerWidth':'14','markerHeight':'12','refX':'12','refY':'6','orient':'auto','markerUnits':'strokeWidth'})
    ET.SubElement(open_arrow, tag('path'), {'d':'M 0 0 L 12 6 L 0 12','fill':'none','stroke':'#162F46','stroke-width':'2'})
    ET.SubElement(root, tag('rect'), {'x':'0','y':'0','width':str(composition.CANVAS[0]),'height':str(composition.CANVAS[1]),'class':'page'})
    ET.SubElement(root, tag('rect'), {'x':'55','y':'55','width':str(composition.CANVAS[0]-110),'height':str(composition.CANVAS[1]-110),'rx':'14','class':'page-border'})
    add_text(root, view.title, composition.CANVAS[0]/2, composition.TITLE_Y, 'page-title', 'middle')
    participants = ET.SubElement(root, tag('g'), {'aria-label':'Sequence participants and lifelines'})
    for item_id in view.include:
        item = selected[item_id]
        if item.type == 'actor':
            draw_actor(participants, item_id, item.name)
        else:
            draw_object(participants, item_id, item.name)
    activations = ET.SubElement(root, tag('g'), {'aria-label':'Meaningful activation bars'})
    for participant_id, y0, y1, offset in composition.ACTIVATIONS:
        draw_activation(activations, participant_id, y0, y1, offset)
    main_messages = ET.SubElement(root, tag('g'), {'aria-label':'Numbered main-success messages'})
    for relation in relations:
        draw_message(main_messages, relation.source, relation.target, composition.MESSAGE_Y[relation.id], relation.name, relation.id, relation.metadata['sequence'], dashed=relation.type == 'return_message', self_message=relation.source == relation.target)
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
