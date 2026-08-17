from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions import aafiatak_sd01_patient_registration_otp as composition


def cell(root, cell_id: str, value: str = '', **attrs):
    data = {'id': cell_id, 'value': value, **{key: str(value) for key, value in attrs.items()}}
    return ET.SubElement(root, 'mxCell', data)


def geometry(cell_node, x: float, y: float, width: float, height: float):
    return ET.SubElement(cell_node, 'mxGeometry', {'x':str(x), 'y':str(y), 'width':str(width), 'height':str(height), 'as':'geometry'})


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
    return lines


def export_sequence_drawio(model, view, output: Path) -> None:
    selected = {item.id: item for item in model.elements if item.id in view.include}
    relation_map = {item.id: item for item in model.relations}
    relations = sorted((relation_map[item_id] for item_id in view.relations), key=lambda r: r.metadata['sequence'])
    root = ET.Element('mxfile', {'host':'app.diagrams.net', 'version':'31.1.8', 'type':'device'})
    diagram = ET.SubElement(root, 'diagram', {'id':'aafiatak-sd01', 'name':'SD-01 Patient Registration OTP'})
    graph = ET.SubElement(diagram, 'mxGraphModel', {'dx':'1200','dy':'900','grid':'1','gridSize':'10','guides':'1','tooltips':'1','connect':'1','arrows':'1','fold':'1','page':'1','pageScale':'1','pageWidth':str(composition.CANVAS[0]),'pageHeight':str(composition.CANVAS[1]),'math':'0','shadow':'0'})
    cells = ET.SubElement(graph, 'root')
    cell(cells, '0'); cell(cells, '1', parent='0')
    counter = 2
    def next_id(prefix: str) -> str:
        nonlocal counter
        result = f'{prefix}-{counter}'; counter += 1; return result
    bg = cell(cells, next_id('page'), '', style='rounded=0;html=1;fillColor=#FFFFFF;strokeColor=none;pointerEvents=0;', vertex='1', parent='1')
    geometry(bg, 0, 0, *composition.CANVAS)
    title = cell(cells, next_id('title'), view.title, style='text;html=1;align=center;verticalAlign=middle;fontSize=60;fontStyle=1;fontColor=#132C45;whiteSpace=wrap;', vertex='1', parent='1')
    geometry(title, 700, 70, 4600, 130)
    for participant_id in view.include:
        item = selected[participant_id]
        x = composition.PARTICIPANT_X[participant_id]
        width = composition.PARTICIPANT_WIDTH[participant_id]
        if item.type == 'actor':
            actor = cell(cells, next_id('actor'), item.name, style='shape=umlActor;html=1;verticalAlign=bottom;align=center;spacingBottom=-12;labelBackgroundColor=#FFFFFF;fontSize=32;fontStyle=1;fontColor=#132C45;', vertex='1', parent='1')
            geometry(actor, x-125, 270, 250, 260)
        else:
            header = cell(cells, next_id('participant'), f'<b>{item.name}</b>', style='rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F8FC;strokeColor=#244C68;strokeWidth=2;fontColor=#132C45;fontSize=36;align=center;verticalAlign=middle;', vertex='1', parent='1')
            geometry(header, x-width/2, composition.HEADER_Y, width, 210)
        lifeline = cell(cells, next_id('lifeline'), '', style='rounded=0;html=1;fillColor=none;strokeColor=#6B7C8E;dashed=1;dashPattern=12 10;strokeWidth=1.5;pointerEvents=0;', vertex='1', parent='1')
        geometry(lifeline, x-1, composition.LIFELINE_TOP, 2, composition.LIFELINE_BOTTOM-composition.LIFELINE_TOP)
    for participant_id, y0, y1, offset in composition.ACTIVATIONS:
        x = composition.PARTICIPANT_X[participant_id] + offset
        bar = cell(cells, next_id('activation'), '', style='rounded=0;html=1;fillColor=#E8F2FC;strokeColor=#326C96;strokeWidth=1.5;', vertex='1', parent='1')
        geometry(bar, x-15, y0, 30, y1-y0)
    def edge(x1: float, y: float, x2: float, label: str, dashed: bool, edge_id: str):
        style = f'html=1;endArrow={"open" if dashed else "block"};dashed={1 if dashed else 0};dashPattern=12 9;strokeColor=#162F46;strokeWidth=2;labelBackgroundColor=#FFFFFF;'
        node = cell(cells, edge_id, '', style=style, edge='1', parent='1')
        geo = ET.SubElement(node, 'mxGeometry', {'relative':'1','as':'geometry'})
        ET.SubElement(geo, 'mxPoint', {'x':str(x1),'y':str(y),'as':'sourcePoint'})
        ET.SubElement(geo, 'mxPoint', {'x':str(x2),'y':str(y),'as':'targetPoint'})
        lines = wrap(label, max(17, min(47, int(abs(x2-x1)/19))))
        width = min(max(270, max(len(line) for line in lines)*21+40), max(340, abs(x2-x1)-40))
        height = 58 + 40*(len(lines)-1)
        text = cell(cells, next_id('label'), '<br/>'.join(lines), style='text;html=1;align=center;verticalAlign=middle;fontSize=34;fontStyle=1;fontColor=#102A43;fillColor=#FFFFFF;strokeColor=none;whiteSpace=wrap;', vertex='1', parent='1')
        geometry(text, (x1+x2)/2-width/2, y-height-12, width, height)
    for relation in relations:
        y = composition.MESSAGE_Y[relation.id]
        x1, x2 = composition.PARTICIPANT_X[relation.source], composition.PARTICIPANT_X[relation.target]
        numbered = f'{relation.metadata["sequence"]}. {relation.name}'
        if relation.source == relation.target:
            right = x1 + 185
            loop = cell(cells, next_id('self'), '', style='html=1;endArrow=block;strokeColor=#162F46;strokeWidth=2;rounded=0;', edge='1', parent='1')
            geo = ET.SubElement(loop, 'mxGeometry', {'relative':'1','as':'geometry'})
            ET.SubElement(geo, 'mxPoint', {'x':str(x1),'y':str(y),'as':'sourcePoint'})
            ET.SubElement(geo, 'mxPoint', {'x':str(x1),'y':str(y+62),'as':'targetPoint'})
            points = ET.SubElement(geo, 'Array', {'as':'points'}); ET.SubElement(points, 'mxPoint', {'x':str(right),'y':str(y)}); ET.SubElement(points, 'mxPoint', {'x':str(right),'y':str(y+62)})
            label = cell(cells, next_id('label'), '<br/>'.join(wrap(numbered, 24)), style='text;html=1;align=left;verticalAlign=middle;fontSize=34;fontStyle=1;fontColor=#102A43;fillColor=#FFFFFF;strokeColor=none;whiteSpace=wrap;', vertex='1', parent='1')
            geometry(label, x1+30, y-118, 390, 118)
        else:
            edge(x1, y, x2, numbered, relation.type == 'return_message', next_id('message'))
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
