"""Editable diagrams.net export derived from the CMP-01 semantic model and shared component composition."""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.component_diagram_layouts import TOKENS, layout_for


def _cell(root, cell_id: str, value: str = "", **attrs):
    return ET.SubElement(root, "mxCell", {"id": cell_id, "value": value, **{key: str(value) for key, value in attrs.items()}})


def _geometry(node, x: float, y: float, width: float, height: float):
    return ET.SubElement(node, "mxGeometry", {"x": f"{x:.2f}", "y": f"{y:.2f}", "width": f"{width:.2f}", "height": f"{height:.2f}", "as": "geometry"})


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
    return x, placement.label_y - TOKENS.interface_label_font_size, placement.label_width, height


def _boundary(layout, placement) -> tuple[float, float]:
    owner = layout.component_boxes[placement.component_id]
    if placement.side == "left":
        return owner.x, placement.y
    if placement.side == "right":
        return owner.right, placement.y
    if placement.side == "top":
        return placement.x, owner.y
    if placement.side == "bottom":
        return placement.x, owner.bottom
    raise ValueError(f"Unsupported Component interface side: {placement.side}")


def _stem_points(layout, placement, provided: bool) -> tuple[tuple[float, float], tuple[float, float]]:
    boundary = _boundary(layout, placement)
    if placement.side == "left":
        glyph_edge = (placement.x + TOKENS.provided_radius, placement.y)
    elif placement.side == "top":
        glyph_edge = (placement.x, placement.y + TOKENS.provided_radius)
    elif placement.side == "right":
        glyph_edge = (placement.x + 16.0, placement.y)
    elif placement.side == "bottom":
        glyph_edge = (placement.x, placement.y + TOKENS.required_radius + 16.0)
    else:
        raise ValueError(f"Unsupported Component interface side: {placement.side}")
    return (glyph_edge, boundary) if provided else (boundary, glyph_edge)


def export_component_drawio(model, view, output: Path) -> None:
    layout = layout_for(view.id)
    selected = {item.id: item for item in model.elements if item.id in view.include}
    relations = {item.id: item for item in model.relations if item.id in view.relations}
    root = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "31.1.8", "type": "device"})
    diagram = ET.SubElement(root, "diagram", {"id": view.id, "name": view.title})
    graph = ET.SubElement(
        diagram,
        "mxGraphModel",
        {"dx": "1600", "dy": "1000", "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": str(layout.width), "pageHeight": str(layout.height), "background": "#FFFFFF", "math": "0", "shadow": "0"},
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

    title = _cell(cells, next_id("title"), view.title, style=f"text;html=1;align=center;verticalAlign=middle;fontSize={int(TOKENS.title_font_size)};fontStyle=1;fontColor=#1F1F1F;fontFamily=Times New Roman;fillColor=none;strokeColor=none;whiteSpace=wrap;", vertex="1", parent="1")
    _geometry(title, 800, 85, layout.width - 1600, 210)

    for item_id, box in layout.component_boxes.items():
        item = selected[item_id]
        vertex = _cell(cells, next_id("component"), item.name, style=f"shape=module;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#262626;strokeWidth={TOKENS.component_stroke_width};fontColor=#1F1F1F;fontFamily=Arial;fontSize={int(TOKENS.component_name_font_size)};fontStyle=1;align=center;verticalAlign=middle;", vertex="1", parent="1")
        _geometry(vertex, box.x, box.y, box.width, box.height)

    # Stems are explicit because both exports represent a physical attachment
    # between the Component boundary and its lollipop/socket glyph.
    for item_id, placement in layout.interfaces.items():
        item = selected[item_id]
        stem = _stem_points(layout, placement, item.type == "provided_interface")
        _edge(cells, next_id("interface-stem"), stem, f"endArrow=none;startArrow=none;strokeColor=#303030;strokeWidth={TOKENS.glyph_stroke_width};rounded=0;html=1;")

    for item_id, placement in layout.interfaces.items():
        item = selected[item_id]
        if item.type == "provided_interface":
            radius = TOKENS.provided_radius
            glyph = _cell(cells, next_id("provided"), "", style=f"ellipse;html=1;fillColor=#FFFFFF;strokeColor=#202020;strokeWidth={TOKENS.glyph_stroke_width};", vertex="1", parent="1")
            _geometry(glyph, placement.x - radius, placement.y - radius, radius * 2, radius * 2)
        else:
            glyph = _cell(cells, next_id("required"), "", style=f"shape=requiredInterface;html=1;fillColor=#FFFFFF;strokeColor=#202020;strokeWidth={TOKENS.glyph_stroke_width};", vertex="1", parent="1")
            if placement.side == "right":
                _geometry(glyph, placement.x - TOKENS.required_radius + 16, placement.y - TOKENS.required_radius, TOKENS.required_radius * 2, TOKENS.required_radius * 2)
            else:
                _geometry(glyph, placement.x - TOKENS.required_radius, placement.y - TOKENS.required_radius + 16, TOKENS.required_radius * 2, TOKENS.required_radius * 2)
        x, y, width, height = _label_geometry(placement, TOKENS.interface_label_line_height * 2)
        label = _cell(cells, next_id("interface-label"), item.name, style=f"text;html=1;align={placement.label_anchor};verticalAlign=middle;fontSize={int(TOKENS.interface_label_font_size)};fontColor=#303030;fontFamily=Arial;fillColor=none;strokeColor=none;whiteSpace=wrap;", vertex="1", parent="1")
        _geometry(label, x, y, width, height)

    for relation in relations.values():
        if relation.type == "connector":
            _edge(cells, next_id("assembly"), layout.connector_paths[relation.id], f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;startArrow=none;strokeColor=#353535;strokeWidth={TOKENS.connector_stroke_width};")

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
