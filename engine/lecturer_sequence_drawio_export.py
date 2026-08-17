from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.svg.lecturer_sequence_diagram import Layout, _message_y, _positions, wrap


def cell(root, cell_id: str, value: str = '', **attrs):
    return ET.SubElement(root, 'mxCell', {'id':cell_id, 'value':value, **{key:str(value) for key, value in attrs.items()}})


def geometry(node, x: float, y: float, width: float, height: float):
    return ET.SubElement(node, 'mxGeometry', {'x':str(x),'y':str(y),'width':str(width),'height':str(height),'as':'geometry'})


def export_lecturer_sequence_drawio(model, view, output: Path) -> None:
    participants = [item for item in model.elements if item.id in view.include]
    relation_by_id = {item.id: item for item in model.relations}
    relations = sorted((relation_by_id[item_id] for item_id in view.relations), key=lambda item:item.metadata['sequence'])
    layout = Layout()
    xs, widths = _positions(participants, layout)
    ys = _message_y(relations, layout)
    root = ET.Element('mxfile', {'host':'app.diagrams.net','version':'31.1.8','type':'device'})
    diagram = ET.SubElement(root, 'diagram', {'id':view.id,'name':view.title})
    graph = ET.SubElement(diagram, 'mxGraphModel', {'dx':'1200','dy':'900','grid':'1','gridSize':'10','guides':'1','tooltips':'1','connect':'1','arrows':'1','fold':'1','page':'1','pageScale':'1','pageWidth':str(layout.width),'pageHeight':str(layout.height),'math':'0','shadow':'0'})
    cells = ET.SubElement(graph, 'root'); cell(cells, '0'); cell(cells, '1', parent='0')
    counter = 2
    def next_id(prefix: str) -> str:
        nonlocal counter
        result = f'{prefix}-{counter}'; counter += 1; return result
    page = cell(cells, next_id('page'), '', style='rounded=0;html=1;fillColor=#FFFFFF;strokeColor=none;pointerEvents=0;', vertex='1', parent='1'); geometry(page, 0, 0, layout.width, layout.height)
    title = cell(cells, next_id('title'), view.title, style='text;html=1;align=center;verticalAlign=middle;fontSize=64;fontStyle=1;fontColor=#132C45;whiteSpace=wrap;', vertex='1', parent='1'); geometry(title, 650, 65, layout.width-1300, 150)
    for item in participants:
        x = xs[item.id]
        if item.type == 'actor':
            actor = cell(cells, next_id('actor'), item.name, style='shape=umlActor;html=1;verticalAlign=bottom;align=center;spacingBottom=-12;labelBackgroundColor=#FFFFFF;fontSize=34;fontStyle=1;fontColor=#132C45;', vertex='1', parent='1'); geometry(actor, x-135, 270, 270, 270)
        else:
            box = cell(cells, next_id('participant'), f'<b>{item.name}</b>', style='rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F8FC;strokeColor=#244C68;strokeWidth=2;fontColor=#132C45;fontSize=40;align=center;verticalAlign=middle;', vertex='1', parent='1'); geometry(box, x-widths[item.id]/2, layout.header_y, widths[item.id], 210)
        life = cell(cells, next_id('lifeline'), '', style='rounded=0;html=1;fillColor=none;strokeColor=#6B7C8E;dashed=1;dashPattern=13 11;strokeWidth=1.5;pointerEvents=0;', vertex='1', parent='1'); geometry(life, x-1, layout.lifeline_top, 2, layout.lifeline_bottom-layout.lifeline_top)
    row = (layout.message_end-layout.message_start)/max(1,len(relations)-1)
    for relation in relations:
        if relation.type == 'message' and relation.source != relation.target and next(item for item in participants if item.id == relation.target).type != 'actor':
            x = xs[relation.target]
            bar = cell(cells, next_id('activation'), '', style='rounded=0;html=1;fillColor=#E8F2FC;strokeColor=#326C96;strokeWidth=1.5;', vertex='1', parent='1'); geometry(bar, x-16, ys[relation.id]-12, 32, min(row*.82,105))
    def label(x1: float, x2: float, y: float, text: str):
        lines = wrap(text, max(20,min(54,int(abs(x2-x1)/21))))
        width = min(max(300,max(len(line) for line in lines)*24+42), max(360,abs(x2-x1)-46))
        height = 64+48*(len(lines)-1)
        txt = cell(cells, next_id('label'), '<br/>'.join(lines), style='text;html=1;align=center;verticalAlign=middle;fontSize=38;fontStyle=1;fontColor=#102A43;fillColor=#FFFFFF;strokeColor=none;whiteSpace=wrap;', vertex='1', parent='1'); geometry(txt,(x1+x2)/2-width/2,y-height-13,width,height)
    for relation in relations:
        x1,x2,y = xs[relation.source],xs[relation.target],ys[relation.id]
        numbered = f'{relation.metadata["sequence"]}. {relation.name}'
        if relation.source == relation.target:
            right = x1+210
            loop = cell(cells,next_id('self'),'',style='html=1;endArrow=block;strokeColor=#162F46;strokeWidth=2;rounded=0;',edge='1',parent='1')
            geo=ET.SubElement(loop,'mxGeometry',{'relative':'1','as':'geometry'}); ET.SubElement(geo,'mxPoint',{'x':str(x1),'y':str(y),'as':'sourcePoint'}); ET.SubElement(geo,'mxPoint',{'x':str(x1),'y':str(y+66),'as':'targetPoint'}); pts=ET.SubElement(geo,'Array',{'as':'points'}); ET.SubElement(pts,'mxPoint',{'x':str(right),'y':str(y)}); ET.SubElement(pts,'mxPoint',{'x':str(right),'y':str(y+66)})
            lines = wrap(numbered, 24)
            width = max(420, min(650, max(len(line) for line in lines) * 24 + 42))
            height = 64 + 48 * (len(lines) - 1)
            text = cell(cells, next_id('label'), '<br/>'.join(lines), style='text;html=1;align=center;verticalAlign=middle;fontSize=38;fontStyle=1;fontColor=#102A43;fillColor=#FFFFFF;strokeColor=none;whiteSpace=wrap;', vertex='1', parent='1')
            geometry(text, right + 34, y + 8, width, height)
        else:
            style=f'html=1;endArrow={"open" if relation.type == "return_message" else "block"};dashed={1 if relation.type == "return_message" else 0};dashPattern=13 10;strokeColor=#162F46;strokeWidth=2;'
            edge=cell(cells,next_id('message'),'',style=style,edge='1',parent='1'); geo=ET.SubElement(edge,'mxGeometry',{'relative':'1','as':'geometry'}); ET.SubElement(geo,'mxPoint',{'x':str(x1),'y':str(y),'as':'sourcePoint'}); ET.SubElement(geo,'mxPoint',{'x':str(x2),'y':str(y),'as':'targetPoint'})
            label(x1,x2,y,numbered)
    output.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(root).write(output,encoding='utf-8',xml_declaration=True)
