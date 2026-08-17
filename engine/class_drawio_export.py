from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions import aafiatak_mvp_class_diagram as composition


def _cell(root, cell_id: str, value: str = '', **attrs):
    data = {'id': cell_id, 'value': value, **{key: str(value) for key, value in attrs.items()}}
    return ET.SubElement(root, 'mxCell', data)


def _geometry(cell, x: float, y: float, width: float, height: float, *, relative: bool = False):
    data = {'x': str(x), 'y': str(y), 'width': str(width), 'height': str(height), 'as': 'geometry'}
    if relative:
        data['relative'] = '1'
    return ET.SubElement(cell, 'mxGeometry', data)


def _html_class(item) -> str:
    attrs = '<br/>'.join(item.metadata['attributes'])
    ops = '<br/>'.join(item.metadata['operations'])
    responsibility = item.metadata['responsibility']
    return (
        f'<div style="text-align:center;font-weight:bold;font-size:12px">{item.name}</div>'
        f'<hr/><div style="text-align:left;font-size:9px">{attrs}</div>'
        f'<hr/><div style="text-align:left;font-size:9px;color:#1F536D">{ops}</div>'
        f'<hr/><div style="text-align:left;font-size:8px;font-style:italic;color:#5D6670">{responsibility}</div>'
    )


def _label_position(box, peer) -> tuple[float, float]:
    cx, cy = box.x + box.width / 2, box.y + box.height / 2
    px, py = peer.x + peer.width / 2, peer.y + peer.height / 2
    if abs(px - cx) > abs(py - cy):
        return (box.x + box.width + 8 if px > cx else box.x - 42, cy - 10)
    return (cx - 15, box.y + box.height + 5 if py > cy else box.y - 25)


def export_class_drawio(model, view, output: Path) -> None:
    selected = {item.id: item for item in model.elements if item.id in view.include}
    classes = [item for item in selected.values() if item.type == 'class']
    notes = [item for item in selected.values() if item.type == 'note']
    relation_by_id = {relation.id: relation for relation in model.relations}
    root = ET.Element('mxfile', {'host': 'app.diagrams.net', 'version': '31.1.8', 'type': 'device'})
    diagram = ET.SubElement(root, 'diagram', {'name': 'MVP Class Diagram', 'id': 'aafiatak-mvp-class'})
    graph = ET.SubElement(diagram, 'mxGraphModel', {'dx': '1000', 'dy': '800', 'grid': '1', 'gridSize': '10', 'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1', 'fold': '1', 'page': '1', 'pageScale': '1', 'pageWidth': '9000', 'pageHeight': '6364', 'math': '0', 'shadow': '0'})
    cells = ET.SubElement(graph, 'root')
    _cell(cells, '0')
    _cell(cells, '1', parent='0')
    counter = 2

    def new_id(prefix: str) -> str:
        nonlocal counter
        value = f'{prefix}-{counter}'
        counter += 1
        return value

    page = _cell(cells, new_id('page'), '', style='rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;pointerEvents=0;', vertex='1', parent='1')
    _geometry(page, 0, 0, composition.CANVAS[0], composition.CANVAS[1])
    title = _cell(cells, new_id('title'), view.title, style='text;html=1;align=center;verticalAlign=middle;fontSize=26;fontStyle=1;fontColor=#182B3D;whiteSpace=wrap;', vertex='1', parent='1')
    _geometry(title, 2200, 45, 4600, 70)
    for label, box, color in composition.ZONES:
        zone = _cell(cells, new_id('zone'), label, style=f'rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#D5DEE9;fontColor=#4A5A6A;fontStyle=1;fontSize=16;verticalAlign=top;align=left;spacingTop=10;spacingLeft=15;opacity=40;pointerEvents=0;', vertex='1', parent='1')
        _geometry(zone, box.x, box.y, box.width, box.height)
    class_cell_ids: dict[str, str] = {}
    for item in classes:
        box = composition.CLASS_BOXES[item.id]
        cell_id = new_id(item.id)
        class_cell_ids[item.id] = cell_id
        cell = _cell(cells, cell_id, _html_class(item), style='rounded=0;whiteSpace=wrap;html=1;overflow=hidden;fillColor=#FFFFFF;strokeColor=#314E6B;strokeWidth=2;fontColor=#273D52;align=left;verticalAlign=top;spacing=8;', vertex='1', parent='1')
        _geometry(cell, box.x, box.y, box.width, box.height)
    for item in notes:
        box = composition.NOTE_BOXES[item.id]
        text = item.metadata['text'].replace('\n', '<br/>')
        cell = _cell(cells, new_id(item.id), f'<b>{item.metadata["note_id"]}</b><br/>{text}', style='shape=note;whiteSpace=wrap;html=1;fillColor=#FFF9CC;strokeColor=#B39B33;fontColor=#665B24;fontSize=10;align=left;verticalAlign=top;spacing=10;', vertex='1', parent='1')
        _geometry(cell, box.x, box.y, box.width, box.height)
    for relation_id in view.relations:
        relation = relation_by_id[relation_id]
        source_box = composition.CLASS_BOXES[relation.source]
        target_box = composition.CLASS_BOXES[relation.target]
        style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#6C7A89;strokeWidth=1.5;endArrow=none;'
        if relation.type == 'composition':
            style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#563D7C;strokeWidth=1.8;startArrow=diamondThin;startFill=1;endArrow=none;'
        elif relation.type == 'aggregation':
            style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#26756E;strokeWidth=1.8;startArrow=diamondThin;startFill=0;endArrow=none;'
        edge = _cell(cells, new_id(relation.id), '', style=style, edge='1', parent='1', source=class_cell_ids[relation.source], target=class_cell_ids[relation.target])
        ET.SubElement(edge, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
        sx, sy = _label_position(source_box, target_box)
        tx, ty = _label_position(target_box, source_box)
        source_label = str(relation.metadata['sourceMultiplicity'])
        target_label = str(relation.metadata['targetMultiplicity'])
        cell = _cell(cells, new_id('mult'), source_label, style='text;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;fontColor=#102A43;fillColor=#FFFFFF;strokeColor=none;whiteSpace=wrap;', vertex='1', parent='1')
        _geometry(cell, sx, sy, 38, 20)
        cell = _cell(cells, new_id('mult'), target_label, style='text;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;fontColor=#102A43;fillColor=#FFFFFF;strokeColor=none;whiteSpace=wrap;', vertex='1', parent='1')
        _geometry(cell, tx, ty, 38, 20)
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
