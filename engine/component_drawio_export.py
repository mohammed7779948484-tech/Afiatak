"""Editable diagrams.net export derived from the CMP-01 semantic model and component composition."""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.component_diagram_layouts import Rect, layout_for


def _cell(root, cell_id: str, value: str = "", **attrs):
    return ET.SubElement(
        root,
        "mxCell",
        {"id": cell_id, "value": value, **{key: str(value) for key, value in attrs.items()}},
    )


def _geometry(node, x: float, y: float, width: float, height: float):
    return ET.SubElement(
        node,
        "mxGeometry",
        {"x": f"{x:.2f}", "y": f"{y:.2f}", "width": f"{width:.2f}", "height": f"{height:.2f}", "as": "geometry"},
    )


def _edge(root, cell_id: str, points: tuple[tuple[float, float], ...], style: str):
    edge = _cell(root, cell_id, "", style=style, edge="1", parent="1")
    geometry = ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    ET.SubElement(geometry, "mxPoint", {"x": f"{points[0][0]:.2f}", "y": f"{points[0][1]:.2f}", "as": "sourcePoint"})
    ET.SubElement(geometry, "mxPoint", {"x": f"{points[-1][0]:.2f}", "y": f"{points[-1][1]:.2f}", "as": "targetPoint"})
    if len(points) > 2:
        route = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in points[1:-1]:
            ET.SubElement(route, "mxPoint", {"x": f"{x:.2f}", "y": f"{y:.2f}"})


def _label_geometry(placement, height: float) -> tuple[float, float, float, float]:
    if placement.label_anchor == "end":
        x = placement.label_x - placement.label_width
    elif placement.label_anchor == "middle":
        x = placement.label_x - placement.label_width / 2
    else:
        x = placement.label_x
    return x, placement.label_y - 44, placement.label_width, height


def export_component_drawio(model, view, output: Path) -> None:
    layout = layout_for(view.id)
    selected = {item.id: item for item in model.elements if item.id in view.include}
    relations = {item.id: item for item in model.relations if item.id in view.relations}
    root = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "31.1.8", "type": "device"})
    diagram = ET.SubElement(root, "diagram", {"id": view.id, "name": view.title})
    graph = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1600", "dy": "1000", "grid": "1", "gridSize": "10", "guides": "1",
            "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1",
            "pageScale": "1", "pageWidth": str(layout.width), "pageHeight": str(layout.height),
            "math": "0", "shadow": "0",
        },
    )
    cells = ET.SubElement(graph, "root")
    _cell(cells, "0")
    _cell(cells, "1", parent="0")
    counter = 2

    def next_id(prefix: str) -> str:
        nonlocal counter
        value = f"{prefix}-{counter}"
        counter += 1
        return value

    page = _cell(cells, next_id("page"), "", style="rounded=0;html=1;fillColor=#FFFFFF;strokeColor=none;pointerEvents=0;", vertex="1", parent="1")
    _geometry(page, 0, 0, layout.width, layout.height)
    title = _cell(cells, next_id("title"), view.title, style="text;html=1;align=center;verticalAlign=middle;fontSize=38;fontStyle=1;fontColor=#222222;fontFamily=Times New Roman;fillColor=none;strokeColor=none;whiteSpace=wrap;", vertex="1", parent="1")
    _geometry(title, 1300, 110, layout.width - 2600, 180)

    for item_id, box in layout.component_boxes.items():
        item = selected[item_id]
        vertex = _cell(cells, next_id("component"), item.name, style="shape=module;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#242424;strokeWidth=2;fontColor=#202020;fontFamily=Arial;fontSize=30;fontStyle=1;align=center;verticalAlign=middle;", vertex="1", parent="1")
        _geometry(vertex, box.x, box.y, box.width, box.height)

    for item_id, placement in layout.interfaces.items():
        item = selected[item_id]
        if item.type == "provided_interface":
            glyph = _cell(cells, next_id("provided"), "", style="ellipse;html=1;fillColor=#FFFFFF;strokeColor=#202020;strokeWidth=2;", vertex="1", parent="1")
            _geometry(glyph, placement.x - 55, placement.y - 55, 110, 110)
        else:
            glyph = _cell(cells, next_id("required"), "", style="shape=requiredInterface;html=1;fillColor=#FFFFFF;strokeColor=#202020;strokeWidth=2;", vertex="1", parent="1")
            if placement.side == "right":
                _geometry(glyph, placement.x - 35, placement.y - 65, 130, 130)
            else:
                _geometry(glyph, placement.x - 65, placement.y - 35, 130, 130)
        x, y, width, height = _label_geometry(placement, 110)
        label = _cell(cells, next_id("interface-label"), item.name, style="text;html=1;align=%s;verticalAlign=middle;fontSize=20;fontColor=#282828;fontFamily=Arial;fillColor=none;strokeColor=none;whiteSpace=wrap;" % placement.label_anchor, vertex="1", parent="1")
        _geometry(label, x, y, width, height)

    for relation in relations.values():
        if relation.type == "connector":
            _edge(cells, next_id("assembly"), layout.connector_paths[relation.id], "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;startArrow=none;strokeColor=#353535;strokeWidth=2;")

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
