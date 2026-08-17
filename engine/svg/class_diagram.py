from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions import aafiatak_mvp_class_diagram as composition
from engine.core.models import SemanticModel, ViewSpec

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)

def tag(name: str) -> str:
    return f'{{{SVG}}}{name}'

def esc(value: str) -> str:
    return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def wrap(text: str, max_chars: int) -> list[str]:
    words = text.split()
    out: list[str] = []
    line = ''
    for word in words:
        candidate = word if not line else f'{line} {word}'
        if line and len(candidate) > max_chars:
            out.append(line); line = word
        else:
            line = candidate
    if line: out.append(line)
    return out or ['']

def add_text(parent, text: str, x: float, y: float, css: str, anchor: str = 'start'):
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{y:g}', 'class': css, 'text-anchor': anchor})
    node.text = text
    return node

def multiline(parent, lines: list[str], x: float, y: float, css: str, leading: float, anchor: str = 'start'):
    node = ET.SubElement(parent, tag('text'), {'x': f'{x:g}', 'y': f'{y:g}', 'class': css, 'text-anchor': anchor})
    for index, line in enumerate(lines):
        attrs = {'x': f'{x:g}'}
        if index: attrs['dy'] = f'{leading:g}'
        span = ET.SubElement(node, tag('tspan'), attrs)
        span.text = line
    return node

def point_on_box(box, tx: float, ty: float) -> tuple[float, float]:
    cx, cy = box.x + box.width/2, box.y + box.height/2
    dx, dy = tx - cx, ty - cy
    if abs(dx / max(box.width, 1)) > abs(dy / max(box.height, 1)):
        return (box.x + box.width if dx > 0 else box.x, cy)
    return (cx, box.y + box.height if dy > 0 else box.y)

def route(source, target, lane: int) -> list[tuple[float, float]]:
    sx, sy = source.x + source.width/2, source.y + source.height/2
    tx, ty = target.x + target.width/2, target.y + target.height/2
    sp = point_on_box(source, tx, ty)
    tp = point_on_box(target, sx, sy)
    if abs(tx - sx) >= abs(ty - sy):
        mid = (sp[0] + tp[0]) / 2 + lane * 12
        return [sp, (mid, sp[1]), (mid, tp[1]), tp]
    mid = (sp[1] + tp[1]) / 2 + lane * 12
    return [sp, (sp[0], mid), (tp[0], mid), tp]

def path_d(points: list[tuple[float,float]]) -> str:
    return 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x,y in points)

def draw_relation(parent, relation, boxes, index: int):
    source = boxes[relation.source]; target = boxes[relation.target]
    points = route(source, target, (index % 7) - 3)
    relation_type = relation.type
    style = 'relation association'
    if relation_type == 'composition': style = 'relation composition'
    if relation_type == 'aggregation': style = 'relation aggregation'
    attrs = {'id': relation.id, 'class': style, 'd': path_d(points), 'data-kind': 'relation', 'data-semantic-id': relation.id}
    if relation_type == 'composition': attrs['marker-start'] = 'url(#filled-diamond)'
    if relation_type == 'aggregation': attrs['marker-start'] = 'url(#hollow-diamond)'
    ET.SubElement(parent, tag('path'), attrs)
    sm = str(relation.metadata.get('sourceMultiplicity', relation.metadata.get('source_multiplicity', '')))
    tm = str(relation.metadata.get('targetMultiplicity', relation.metadata.get('target_multiplicity', '')))
    x1,y1 = points[0]; x2,y2 = points[1]
    lx1,ly1 = (x1 + (x2-x1)*0.18, y1 + (y2-y1)*0.18)
    x1,y1 = points[-1]; x2,y2 = points[-2]
    lx2,ly2 = (x1 + (x2-x1)*0.18, y1 + (y2-y1)*0.18)
    add_text(parent, sm, lx1 + 10, ly1 - 9, 'multiplicity')
    add_text(parent, tm, lx2 + 10, ly2 - 9, 'multiplicity')

def draw_class(parent, item, box):
    group = ET.SubElement(parent, tag('g'), {'id': item.id, 'data-kind': 'class', 'data-semantic-id': item.id, 'aria-label': item.name})
    ET.SubElement(group, tag('rect'), {'x':str(box.x),'y':str(box.y),'width':str(box.width),'height':str(box.height),'class':'class-box','rx':'4'})
    attrs = item.metadata.get('attributes', [])
    ops = item.metadata.get('operations', [])
    responsibility = item.metadata.get('responsibility', item.description)
    name_h = 60
    attr_h = max(50, len(attrs) * 27 + 24)
    op_h = max(50, len(ops) * 27 + 24)
    y_attr = box.y + name_h
    y_op = y_attr + attr_h
    y_resp = y_op + op_h
    ET.SubElement(group, tag('line'), {'x1':str(box.x),'x2':str(box.x+box.width),'y1':str(y_attr),'y2':str(y_attr),'class':'separator'})
    ET.SubElement(group, tag('line'), {'x1':str(box.x),'x2':str(box.x+box.width),'y1':str(y_op),'y2':str(y_op),'class':'separator'})
    ET.SubElement(group, tag('line'), {'x1':str(box.x),'x2':str(box.x+box.width),'y1':str(y_resp),'y2':str(y_resp),'class':'separator'})
    add_text(group, item.name, box.x+box.width/2, box.y+39, 'class-name', 'middle')
    multiline(group, attrs, box.x+18, y_attr+27, 'class-attribute', 27)
    multiline(group, ops, box.x+18, y_op+27, 'class-operation', 27)
    resp_lines = wrap(responsibility, max(28, int(box.width/19)))
    multiline(group, resp_lines[:4], box.x+18, y_resp+27, 'class-responsibility', 23)

def draw_note(parent, item, box):
    text = item.metadata.get('text', item.description)
    group = ET.SubElement(parent, tag('g'), {'id':item.id, 'data-kind':'note', 'data-semantic-id':item.id, 'aria-label':item.name})
    fold = 26
    points = f'{box.x},{box.y} {box.x+box.width-fold},{box.y} {box.x+box.width},{box.y+fold} {box.x+box.width},{box.y+box.height} {box.x},{box.y+box.height}'
    ET.SubElement(group, tag('polygon'), {'points':points,'class':'note-box'})
    ET.SubElement(group, tag('polyline'), {'points':f'{box.x+box.width-fold},{box.y} {box.x+box.width-fold},{box.y+fold} {box.x+box.width},{box.y+fold}','class':'note-fold'})
    add_text(group, item.metadata.get('note_id', item.name), box.x+16, box.y+23, 'note-title')
    multiline(group, wrap(text, max(26, int(box.width/16))), box.x+16, box.y+50, 'note-text', 18)

def render_class_diagram_svg(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    selected = {item.id: item for item in model.elements if item.id in view.include}
    classes = [item for item in selected.values() if item.type == 'class']
    notes = [item for item in selected.values() if item.type == 'note']
    if len(classes) != 30 or len(notes) != 10:
        raise ValueError('MVP Class Diagram requires exactly 30 classes and 10 notes')
    relation_map = {item.id: item for item in model.relations}
    relations = [relation_map[rid] for rid in view.relations]
    if len(relations) != 52:
        raise ValueError('MVP Class Diagram requires exactly 52 relationships')
    root = ET.Element(tag('svg'), {'width':str(composition.CANVAS[0]), 'height':str(composition.CANVAS[1]), 'viewBox':f'0 0 {composition.CANVAS[0]} {composition.CANVAS[1]}', 'role':'img', 'aria-labelledby':'diagram-title diagram-description'})
    title = ET.SubElement(root, tag('title'), {'id':'diagram-title'}); title.text = view.title
    desc = ET.SubElement(root, tag('desc'), {'id':'diagram-description'}); desc.text = 'One-sheet MVP domain Class Diagram with 30 classes, 52 typed relationships, multiplicities, and 10 UML notes.'
    style = ET.SubElement(ET.SubElement(root, tag('defs')), tag('style'))
    style.text = '''
      .page { fill:#FFFFFF; } .zone { stroke:#D5DEE9; stroke-width:2; } .zone-title { font-family:Arial,sans-serif; font-size:28px; font-weight:700; letter-spacing:1px; fill:#4A5A6A; }
      .class-box { fill:#FFFFFF; stroke:#314E6B; stroke-width:2.4; } .separator { stroke:#7890A7; stroke-width:1.4; }
      .class-name { font-family:Arial,sans-serif; font-size:28px; font-weight:700; fill:#18344E; } .class-attribute { font-family:Arial,sans-serif; font-size:19px; fill:#273D52; }
      .class-operation { font-family:Arial,sans-serif; font-size:19px; fill:#1F536D; } .class-responsibility { font-family:Arial,sans-serif; font-size:18px; font-style:italic; fill:#5D6670; }
      .relation { fill:none; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; } .association { stroke:#6C7A89; opacity:.86; } .composition { stroke:#563D7C; opacity:.92; } .aggregation { stroke:#26756E; opacity:.92; }
      .multiplicity { font-family:Arial,sans-serif; font-size:26px; font-weight:700; fill:#102A43; paint-order:stroke; stroke:#FFFFFF; stroke-width:6; stroke-linejoin:round; }
      .note-box { fill:#FFF9CC; stroke:#B39B33; stroke-width:1.8; } .note-fold { fill:none; stroke:#B39B33; stroke-width:1.6; } .note-title { font-family:Arial,sans-serif; font-size:18px; font-weight:700; fill:#75641A; } .note-text { font-family:Arial,sans-serif; font-size:16px; fill:#665B24; }
      .page-title { font-family:Arial,sans-serif; font-size:48px; font-weight:700; fill:#182B3D; }
    '''
    defs = root.find(tag('defs'))
    filled = ET.SubElement(defs, tag('marker'), {'id':'filled-diamond','markerWidth':'18','markerHeight':'14','refX':'2','refY':'7','orient':'auto','markerUnits':'strokeWidth'})
    ET.SubElement(filled, tag('path'), {'d':'M 16 7 L 8 1 L 0 7 L 8 13 Z','fill':'#563D7C','stroke':'#563D7C'})
    hollow = ET.SubElement(defs, tag('marker'), {'id':'hollow-diamond','markerWidth':'18','markerHeight':'14','refX':'2','refY':'7','orient':'auto','markerUnits':'strokeWidth'})
    ET.SubElement(hollow, tag('path'), {'d':'M 16 7 L 8 1 L 0 7 L 8 13 Z','fill':'#FFFFFF','stroke':'#26756E','stroke-width':'1.2'})
    ET.SubElement(root, tag('rect'), {'width':str(composition.CANVAS[0]),'height':str(composition.CANVAS[1]),'class':'page'})
    add_text(root, view.title, composition.CANVAS[0]/2, 110, 'page-title', 'middle')
    zones = ET.SubElement(root, tag('g'), {'aria-label':'Non-semantic visual zones'})
    for label, box, color in composition.ZONES:
        ET.SubElement(zones, tag('rect'), {'x':str(box.x),'y':str(box.y),'width':str(box.width),'height':str(box.height),'rx':'18','class':'zone','fill':color})
        add_text(zones, label, box.x+24, box.y+38, 'zone-title')
    relation_group = ET.SubElement(root, tag('g'), {'aria-label':'UML class relationships'})
    for index, relation in enumerate(relations):
        draw_relation(relation_group, relation, composition.CLASS_BOXES, index)
    class_group = ET.SubElement(root, tag('g'), {'aria-label':'Class boxes'})
    for item in classes:
        draw_class(class_group, item, composition.CLASS_BOXES[item.id])
    note_group = ET.SubElement(root, tag('g'), {'aria-label':'UML notes'})
    for item in notes:
        draw_note(note_group, item, composition.NOTE_BOXES[item.id])
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
