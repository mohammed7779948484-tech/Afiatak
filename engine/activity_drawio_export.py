from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.activity_diagram_layouts import layout_for
from engine.core.models import SemanticModel, ViewSpec


def cell(root, identifier: str, value: str, style: str, x: float, y: float, width: float, height: float, *, vertex: bool = True, source: str | None = None, target: str | None = None, points: list[tuple[float, float]] | None = None):
    attrs = {'id': identifier, 'value': value, 'style': style, 'parent': '1'}
    if vertex:
        attrs['vertex'] = '1'
    else:
        attrs['edge'] = '1'
        if source:
            attrs['source'] = source
        if target:
            attrs['target'] = target
    node = ET.SubElement(root, 'mxCell', attrs)
    geometry = ET.SubElement(node, 'mxGeometry', {'x': f'{x:g}', 'y': f'{y:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'as': 'geometry'})
    if not vertex:
        geometry.set('relative', '1')
        if points and len(points) > 2:
            array = ET.SubElement(geometry, 'Array', {'as': 'points'})
            for px, py in points[1:-1]:
                ET.SubElement(array, 'mxPoint', {'x': f'{px:g}', 'y': f'{py:g}'})
    return node


def wrap_label(text: str, maximum: int = 34) -> list[str]:
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


def label_geometry(text: str) -> tuple[float, float]:
    lines = wrap_label(text)
    return max(280, min(1050, max(len(line) for line in lines) * 29 + 64)), 52 * len(lines) + 34


def export_activity_drawio(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout, composition = layout_for(view.id)
    visible = {element.id: element for element in model.elements if element.id in view.include}
    relations_by_id = {relation.id: relation for relation in model.relations}

    mxfile = ET.Element('mxfile', {'host': 'app.diagrams.net', 'version': '31.1.8', 'type': 'device'})
    diagram = ET.SubElement(mxfile, 'diagram', {'id': view.id, 'name': view.title})
    graph = ET.SubElement(diagram, 'mxGraphModel', {'dx': '0', 'dy': '0', 'grid': '1', 'gridSize': '10', 'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1', 'fold': '1', 'page': '1', 'pageScale': '1', 'pageWidth': str(layout.width), 'pageHeight': str(layout.height), 'math': '0', 'shadow': '0', 'background': '#ffffff'})
    root = ET.SubElement(graph, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    cell(root, 'page-background', '', 'shape=rectangle;html=1;fillColor=#FFFFFF;strokeColor=none;movable=0;resizable=0;editable=0;deletable=0;connectable=0;', 0, 0, layout.width, layout.height)
    cell(root, 'page-title', view.title, 'text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=88;fontStyle=1;fontColor=#132C45;strokeColor=none;fillColor=none;movable=0;resizable=0;editable=0;deletable=0;connectable=0;', 600, 90, layout.width - 1200, 140)

    node_ids: dict[str, str] = {}
    for index, (semantic_id, (x, y)) in enumerate(composition.get('initial', {}).items(), start=1):
        identifier = f'node-initial-{index}'
        node_ids[semantic_id] = identifier
        cell(root, identifier, '', 'shape=ellipse;html=1;fillColor=#102A43;strokeColor=#102A43;strokeWidth=3;', x - 38, y - 38, 76, 76)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('actions', {}).items(), start=1):
        identifier = f'node-action-{index}'
        node_ids[semantic_id] = identifier
        cell(root, identifier, visible[semantic_id].name, 'rounded=1;whiteSpace=wrap;html=1;fillColor=#F6F9FC;strokeColor=#163D59;strokeWidth=3;fontFamily=Arial;fontSize=68;fontStyle=1;fontColor=#102A43;align=center;verticalAlign=middle;spacing=12;', x, y, layout.action_width, layout.action_height)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('decisions', {}).items(), start=1):
        identifier = f'node-decision-{index}'
        node_ids[semantic_id] = identifier
        cell(root, identifier, visible[semantic_id].name, 'shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFF7D6;strokeColor=#9B6D05;strokeWidth=3;fontFamily=Arial;fontSize=52;fontStyle=1;fontColor=#5D4300;align=center;verticalAlign=middle;spacing=10;', x, y, layout.decision_width, layout.decision_height)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('merges', {}).items(), start=1):
        identifier = f'node-merge-{index}'
        node_ids[semantic_id] = identifier
        cell(root, identifier, '', 'shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6B7C93;strokeWidth=3;', x, y, layout.decision_width * 0.62, layout.decision_height * 0.62)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('notes', {}).items(), start=1):
        identifier = f'node-note-{index}'
        node_ids[semantic_id] = identifier
        cell(root, identifier, visible[semantic_id].name, 'shape=note;whiteSpace=wrap;html=1;fillColor=#FFFDF5;strokeColor=#8C7A48;strokeWidth=2;fontFamily=Arial;fontSize=44;fontStyle=2;fontColor=#5D5435;align=center;verticalAlign=middle;spacing=10;connectable=0;', x, y, layout.note_width, layout.note_height)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('final', {}).items(), start=1):
        outer = f'node-final-outer-{index}'
        inner = f'node-final-inner-{index}'
        node_ids[semantic_id] = outer
        cell(root, outer, '', 'shape=ellipse;html=1;fillColor=#FFFFFF;strokeColor=#102A43;strokeWidth=5;', x - 54, y - 54, 108, 108)
        cell(root, inner, '', 'shape=ellipse;html=1;fillColor=#102A43;strokeColor=#102A43;strokeWidth=2;movable=0;resizable=0;editable=0;deletable=0;connectable=0;', x - 29, y - 29, 58, 58)

    edge_style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#102A43;strokeWidth=3;'
    label_style = 'text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;fontFamily=Arial;fontSize=52;fontStyle=1;fontColor=#102A43;strokeColor=none;fillColor=#FFFFFF;opacity=98;spacing=6;movable=1;resizable=1;editable=1;deletable=1;connectable=0;'
    for index, relation_id in enumerate(view.relations, start=1):
        relation = relations_by_id[relation_id]
        route = composition['routes'][relation.id]
        cell(root, f'edge-{index}', '', edge_style, 0, 0, 0, 0, vertex=False, source=node_ids[relation.source], target=node_ids[relation.target], points=route['points'])
        if relation.name and relation.metadata.get('visibleLabel', True):
            width, height = label_geometry(relation.name)
            label_x, label_y = route['label']
            cell(root, f'label-{index}', relation.name, label_style, label_x - width / 2, label_y - height / 2, width, height)

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(mxfile).write(output, encoding='utf-8', xml_declaration=True)
