from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.activity_diagram_layouts_v3 import layout_for
from engine.core.models import SemanticModel, ViewSpec


def cell(root, identifier: str, value: str, style: str, x: float, y: float, width: float, height: float, *, vertex: bool = True, source: str | None = None, target: str | None = None, points: list[tuple[float, float]] | None = None):
    attrs = {'id': identifier, 'value': value, 'style': style, 'parent': '1'}
    if vertex:
        attrs['vertex'] = '1'
    else:
        attrs['edge'] = '1'
        if source: attrs['source'] = source
        if target: attrs['target'] = target
    node = ET.SubElement(root, 'mxCell', attrs)
    geometry = ET.SubElement(node, 'mxGeometry', {'x': f'{x:g}', 'y': f'{y:g}', 'width': f'{width:g}', 'height': f'{height:g}', 'as': 'geometry'})
    if not vertex:
        geometry.set('relative', '1')
        if points and len(points) > 2:
            array = ET.SubElement(geometry, 'Array', {'as': 'points'})
            for px, py in points[1:-1]: ET.SubElement(array, 'mxPoint', {'x': f'{px:g}', 'y': f'{py:g}'})
    return node


def visible_name(element) -> str:
    return element.metadata.get('visibleLabel', element.name)


def label_geometry(text: str) -> tuple[float, float]:
    words, lines, line = text.split(), [], ''
    for word in words:
        candidate = word if not line else f'{line} {word}'
        if line and len(candidate) > 30: lines.append(line); line = word
        else: line = candidate
    if line: lines.append(line)
    return max(230, min(900, max(len(row) for row in lines) * 25 + 48)), 46 * len(lines) + 28


def export_activity_drawio(model: SemanticModel, view: ViewSpec, output: Path) -> None:
    layout, composition = layout_for(view.id)
    visible = {element.id: element for element in model.elements if element.id in view.include}
    relation_map = {relation.id: relation for relation in model.relations}
    mxfile = ET.Element('mxfile', {'host': 'app.diagrams.net', 'version': '31.1.8', 'type': 'device'})
    diagram = ET.SubElement(mxfile, 'diagram', {'id': view.id, 'name': view.title})
    graph = ET.SubElement(diagram, 'mxGraphModel', {'dx': '0', 'dy': '0', 'grid': '1', 'gridSize': '10', 'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1', 'fold': '1', 'page': '1', 'pageScale': '1', 'pageWidth': str(layout.width), 'pageHeight': str(layout.height), 'math': '0', 'shadow': '0', 'background': '#ffffff'})
    root = ET.SubElement(graph, 'root'); ET.SubElement(root, 'mxCell', {'id': '0'}); ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    cell(root, 'page-background', '', 'shape=rectangle;html=1;fillColor=#FFFFFF;strokeColor=none;movable=0;resizable=0;editable=0;deletable=0;connectable=0;', 0, 0, layout.width, layout.height)
    frame = composition.get('frame', {'x': 150, 'y': 230, 'width': layout.width - 300, 'height': layout.height - 380})
    cell(root, 'process-frame', '', 'rounded=1;html=1;fillColor=none;strokeColor=#111111;strokeWidth=3;arcSize=16;movable=0;resizable=0;editable=0;deletable=0;connectable=0;pointerEvents=0;', frame['x'], frame['y'], frame['width'], frame['height'])
    cell(root, 'page-title', view.title, 'text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=62;fontStyle=1;fontColor=#111111;strokeColor=none;fillColor=none;movable=0;resizable=0;editable=0;deletable=0;connectable=0;', 300, 40, layout.width - 600, 110)
    cell(root, 'frame-title', view.options.get('useCase', view.title.replace('Activity Diagram — ', '')), 'text;html=1;align=left;verticalAlign=middle;fontFamily=Arial;fontSize=60;fontStyle=1;fontColor=#111111;strokeColor=none;fillColor=none;movable=0;resizable=0;editable=0;deletable=0;connectable=0;', frame['x'] + 80, frame['y'] + 35, frame['width'] - 160, 100)
    node_ids: dict[str, str] = {}
    for index, (semantic_id, (x, y)) in enumerate(composition.get('initial', {}).items(), 1):
        identifier = f'node-initial-{index}'; node_ids[semantic_id] = identifier
        cell(root, identifier, '', 'shape=ellipse;html=1;fillColor=#000000;strokeColor=#000000;strokeWidth=2;', x - 32, y - 32, 64, 64)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('actions', {}).items(), 1):
        identifier = f'node-action-{index}'; node_ids[semantic_id] = identifier
        cell(root, identifier, visible_name(visible[semantic_id]), 'rounded=1;whiteSpace=wrap;html=1;fillColor=#F6F6F6;strokeColor=#111111;strokeWidth=3;fontFamily=Arial;fontSize=56;fontColor=#111111;align=center;verticalAlign=middle;spacing=10;', x, y, layout.action_width, layout.action_height)
    for index, (semantic_id, (x, y, width, height)) in enumerate(composition.get('objects', {}).items(), 1):
        identifier = f'node-object-{index}'; node_ids[semantic_id] = identifier
        cell(root, identifier, visible_name(visible[semantic_id]), 'rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#111111;strokeWidth=3;fontFamily=Arial;fontSize=48;fontColor=#111111;align=center;verticalAlign=middle;spacing=8;', x, y, width, height)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('decisions', {}).items(), 1):
        identifier = f'node-decision-{index}'; node_ids[semantic_id] = identifier
        cell(root, identifier, visible_name(visible[semantic_id]), 'shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#111111;strokeWidth=3;fontFamily=Arial;fontSize=46;fontStyle=1;fontColor=#111111;align=center;verticalAlign=middle;spacing=8;', x, y, layout.decision_width, layout.decision_height)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('merges', {}).items(), 1):
        identifier = f'node-merge-{index}'; node_ids[semantic_id] = identifier
        cell(root, identifier, '', 'shape=rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#111111;strokeWidth=3;', x, y, layout.decision_width * .56, layout.decision_height * .56)
    for kind, coords in (('forks', composition.get('forks', {})), ('joins', composition.get('joins', {}))):
        for index, (semantic_id, (x, y, width, height)) in enumerate(coords.items(), 1):
            identifier = f'node-{kind}-{index}'; node_ids[semantic_id] = identifier
            cell(root, identifier, '', 'shape=rectangle;html=1;fillColor=#000000;strokeColor=#000000;strokeWidth=1;', x, y, width, height)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('notes', {}).items(), 1):
        identifier = f'node-note-{index}'; node_ids[semantic_id] = identifier
        cell(root, identifier, visible_name(visible[semantic_id]), 'shape=note;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=2;fontFamily=Arial;fontSize=36;fontStyle=2;fontColor=#222222;align=center;verticalAlign=middle;spacing=8;connectable=0;', x, y, layout.note_width, layout.note_height)
    for index, (semantic_id, (x, y)) in enumerate(composition.get('final', {}).items(), 1):
        outer = f'node-final-outer-{index}'; inner = f'node-final-inner-{index}'; node_ids[semantic_id] = outer
        cell(root, outer, '', 'shape=ellipse;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=4;', x - 50, y - 50, 100, 100)
        cell(root, inner, '', 'shape=ellipse;html=1;fillColor=#000000;strokeColor=#000000;strokeWidth=1;movable=0;resizable=0;editable=0;deletable=0;connectable=0;', x - 27, y - 27, 54, 54)
    edge_style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#111111;strokeWidth=3;'
    label_style = 'text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;fontFamily=Arial;fontSize=43;fontColor=#111111;strokeColor=none;fillColor=#FFFFFF;opacity=96;spacing=5;movable=1;resizable=1;editable=1;deletable=1;connectable=0;'
    for index, relation_id in enumerate(view.relations, 1):
        relation = relation_map[relation_id]; route = composition['routes'][relation.id]
        cell(root, f'edge-{index}', '', edge_style, 0, 0, 0, 0, vertex=False, source=node_ids[relation.source], target=node_ids[relation.target], points=route['points'])
        if relation.name and relation.metadata.get('visibleLabel', True):
            width, height = label_geometry(relation.name); x, y = route['label']
            cell(root, f'label-{index}', relation.name, label_style, x - width / 2, y - height / 2, width, height)
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(mxfile).write(output, encoding='utf-8', xml_declaration=True)
