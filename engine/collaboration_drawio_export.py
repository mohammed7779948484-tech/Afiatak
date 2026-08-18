from __future__ import annotations

import math
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.collaboration_diagram_layouts import layout_for
from engine.svg.collaboration_diagram import point_on_segment, rect_edge_point, wrap


def cell(root, cell_id: str, value: str = "", **attrs):
    return ET.SubElement(root, "mxCell", {"id": cell_id, "value": value, **{key: str(value) for key, value in attrs.items()}})


def geometry(node, x: float, y: float, width: float, height: float):
    return ET.SubElement(node, "mxGeometry", {"x": f"{x:g}", "y": f"{y:g}", "width": f"{width:g}", "height": f"{height:g}", "as": "geometry"})


def edge_with_points(root, cell_id: str, start: tuple[float, float], end: tuple[float, float], style: str):
    edge = cell(root, cell_id, "", style=style, edge="1", parent="1")
    geo = ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    ET.SubElement(geo, "mxPoint", {"x": f"{start[0]:g}", "y": f"{start[1]:g}", "as": "sourcePoint"})
    ET.SubElement(geo, "mxPoint", {"x": f"{end[0]:g}", "y": f"{end[1]:g}", "as": "targetPoint"})
    return edge


def export_collaboration_drawio(model, view, output: Path) -> None:
    layout, composition = layout_for(view.id)
    participants = [item for item in model.elements if item.id in view.include]
    participant_map = {item.id: item for item in participants}
    relation_map = {item.id: item for item in model.relations}
    relations = sorted((relation_map[item_id] for item_id in view.relations), key=lambda item: item.metadata["sequence"])
    positions = composition["participants"]
    root = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "31.1.8", "type": "device"})
    diagram = ET.SubElement(root, "diagram", {"id": view.id, "name": view.title})
    graph = ET.SubElement(diagram, "mxGraphModel", {"dx": "1600", "dy": "1000", "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": str(layout.width), "pageHeight": str(layout.height), "math": "0", "shadow": "0"})
    cells = ET.SubElement(graph, "root")
    cell(cells, "0")
    cell(cells, "1", parent="0")
    counter = 2

    def next_id(prefix: str) -> str:
        nonlocal counter
        result = f"{prefix}-{counter}"
        counter += 1
        return result

    # The lecture reference uses an unframed white canvas with no diagram title band.
    page = cell(cells, next_id("page"), "", style="rounded=0;html=1;fillColor=#FFFFFF;strokeColor=none;pointerEvents=0;", vertex="1", parent="1")
    geometry(page, 0, 0, layout.width, layout.height)

    node_ids: dict[str, str] = {}
    for item in participants:
        cx, cy = positions[item.id]
        node = cell(cells, next_id("participant"), f"<u>{item.name}</u>", style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#222222;strokeWidth=2.5;fontColor=#222222;fontFamily=Times New Roman;fontSize=48;fontStyle=4;align=center;verticalAlign=middle;", vertex="1", parent="1")
        geometry(node, cx - layout.participant_width / 2, cy - layout.participant_height / 2, layout.participant_width, layout.participant_height)
        node_ids[item.id] = node.attrib["id"]

    link_geometry: dict[str, tuple[tuple[float, float], tuple[float, float]]] = {}
    for link in view.options["structuralLinks"]:
        source_id, target_id = link["participants"]
        start = rect_edge_point(positions[source_id], positions[target_id], layout.participant_width / 2, layout.participant_height / 2)
        end = rect_edge_point(positions[target_id], positions[source_id], layout.participant_width / 2, layout.participant_height / 2)
        link_geometry[link["id"]] = (start, end)
        edge_with_points(cells, next_id(f"link-{link['id']}"), start, end, "html=1;endArrow=none;startArrow=none;strokeColor=#777777;strokeWidth=2;rounded=0;")

    by_link: dict[str, list] = {}
    self_messages: list = []
    for relation in relations:
        if relation.source == relation.target:
            self_messages.append(relation)
        else:
            by_link.setdefault(relation.metadata["structuralLink"], []).append(relation)

    def label(x: float, y: float, width: float, relation) -> float:
        lines = wrap(relation.name, max(22, int((width - 100) / 31)))
        height = max(112, 24 + 72 * len(lines))
        numbered = f'{relation.metadata["sequence"]}.&nbsp;&nbsp;{"<br/>".join(lines)}'
        # Text floats beside the link as in the lecturer reference; no card, fill, or border is drawn.
        text = cell(cells, next_id("message-label"), numbered, style="text;html=1;align=left;verticalAlign=top;fontSize=50;fontColor=#333333;fontFamily=Times New Roman;fillColor=none;strokeColor=none;whiteSpace=wrap;spacingLeft=0;spacingTop=0;", vertex="1", parent="1")
        geometry(text, x, y, width, height)
        return y + height + 18

    for link in view.options["structuralLinks"]:
        link_id = link["id"]
        start, end = link_geometry[link_id]
        messages = sorted(by_link.get(link_id, []), key=lambda item: item.metadata["sequence"])
        cursor_y = composition["links"][link_id]["labelBox"][1]
        box_x, _, box_width = composition["links"][link_id]["labelBox"]
        for index, relation in enumerate(messages):
            source_is_first = relation.source == link["participants"][0]
            direction_start, direction_end = (start, end) if source_is_first else (end, start)
            fraction = 0.5 if len(messages) == 1 else 0.14 + 0.72 * index / (len(messages) - 1)
            centre = point_on_segment(direction_start, direction_end, fraction)
            ux, uy = direction_end[0] - direction_start[0], direction_end[1] - direction_start[1]
            magnitude = math.hypot(ux, uy) or 1
            ux, uy = ux / magnitude, uy / magnitude
            length = min(340, max(190, math.dist(start, end) * 0.14))
            arrow_start = (centre[0] - ux * length / 2, centre[1] - uy * length / 2)
            arrow_end = (centre[0] + ux * length / 2, centre[1] + uy * length / 2)
            edge_with_points(cells, next_id(f"message-{relation.metadata['sequence']}"), arrow_start, arrow_end, "html=1;endArrow=block;endFill=1;strokeColor=#777777;strokeWidth=2;rounded=0;")
            cursor_y = label(box_x, cursor_y, box_width, relation)

    for relation in self_messages:
        cx, cy = positions[relation.source]
        box_x, box_y, box_width = composition["selfMessages"][relation.id]["box"]
        top = cy - layout.participant_height / 2
        edge = cell(cells, next_id(f"self-{relation.metadata['sequence']}"), "", style="html=1;endArrow=block;endFill=1;strokeColor=#777777;strokeWidth=2;rounded=1;curved=1;", edge="1", parent="1")
        geo = ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
        ET.SubElement(geo, "mxPoint", {"x": f"{cx - 180:g}", "y": f"{top:g}", "as": "sourcePoint"})
        ET.SubElement(geo, "mxPoint", {"x": f"{cx + 180:g}", "y": f"{top:g}", "as": "targetPoint"})
        points = ET.SubElement(geo, "Array", {"as": "points"})
        ET.SubElement(points, "mxPoint", {"x": f"{cx:g}", "y": f"{top - 520:g}"})
        label(box_x, box_y, box_width, relation)

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
