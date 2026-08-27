"""Editable diagrams.net export derived from the DEP-01 semantic model and shared deployment composition."""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.deployment_diagram_layouts import TOKENS, layout_for


def _cell(root, cell_id: str, value: str = "", **attrs):
    return ET.SubElement(root, "mxCell", {"id": cell_id, "value": value, **{key: str(value) for key, value in attrs.items()}})


def _geometry(node, x: float, y: float, width: float, height: float, *, relative: bool = False):
    attrs = {"x": f"{x:.2f}", "y": f"{y:.2f}", "width": f"{width:.2f}", "height": f"{height:.2f}", "as": "geometry"}
    if relative:
        attrs["relative"] = "1"
    return ET.SubElement(node, "mxGeometry", attrs)


def _port_style(prefix: str, box, point: tuple[float, float]) -> str:
    x, y = point
    return f"{prefix}X={(x - box.x) / box.width:.5f};{prefix}Y={(y - box.y) / box.height:.5f};{prefix}Dx=0;{prefix}Dy=0;"


def _edge(root, cell_id: str, source: str, target: str, source_box, target_box, points: tuple[tuple[float, float], ...], style: str):
    ports = _port_style("exit", source_box, points[0]) + _port_style("entry", target_box, points[-1])
    edge = _cell(root, cell_id, "", style=style + ports, edge="1", parent="1", source=source, target=target)
    geometry = ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    if len(points) > 2:
        route = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in points[1:-1]:
            ET.SubElement(route, "mxPoint", {"x": f"{x:.2f}", "y": f"{y:.2f}"})


def _rich_label(stereotype: str, label: str) -> str:
    return f'<span style="font-size:{int(TOKENS.contained_stereotype_font_size)}px;font-style:italic;">«{stereotype}»</span><br>{label}'


def _contained_style(visual_kind: str) -> str:
    base = f"html=1;align=center;verticalAlign=middle;fontSize={int(TOKENS.contained_font_size)};fontColor=#242424;fontFamily=Arial;fillColor=#FFFFFF;strokeColor=#343434;strokeWidth={TOKENS.contained_stroke_width};whiteSpace=wrap;"
    if visual_kind == "execution-environment":
        return f"shape=cube;size=12;gradientColor=none;shadow=0;{base}"
    if visual_kind == "deployed-artifact":
        return f"shape=note;size=20;gradientColor=none;shadow=0;{base}"
    return f"rounded=0;dashed=1;dashPattern=9 7;shadow=0;{base}"


def export_deployment_drawio(model, view, output: Path) -> None:
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
    _geometry(title, 750, 80, layout.width - 1500, 220)

    node_cells: dict[str, str] = {}
    for item_id, node_layout in layout.nodes.items():
        item = selected[item_id]
        box = node_layout.box
        node_id = next_id("node")
        node_cells[item_id] = node_id
        node = _cell(cells, node_id, "", style=f"shape=cube;size=24;html=1;whiteSpace=wrap;fillColor=#FFFFFF;gradientColor=none;strokeColor=#262626;strokeWidth={TOKENS.node_stroke_width};shadow=0;", vertex="1", parent="1")
        _geometry(node, box.x, box.y, box.width, box.height)
        if node_layout.node_stereotype:
            stereotype = _cell(cells, next_id("node-stereotype"), f"«{node_layout.node_stereotype}»", style=f"text;html=1;align=center;verticalAlign=middle;fontSize={int(TOKENS.node_stereotype_font_size)};fontStyle=2;fontColor=#454545;fontFamily=Arial;fillColor=none;strokeColor=none;whiteSpace=wrap;", vertex="1", parent=node_id)
            _geometry(stereotype, node_layout.title_bounds.x - box.x, node_layout.title_bounds.y - box.y, node_layout.title_bounds.width, TOKENS.node_stereotype_line_height + 10)
            name_y = node_layout.title_bounds.y - box.y + TOKENS.node_stereotype_line_height + 16
            name_height = node_layout.title_bounds.height - TOKENS.node_stereotype_line_height - 16
        else:
            name_y = node_layout.title_bounds.y - box.y
            name_height = node_layout.title_bounds.height
        name = _cell(cells, next_id("node-name"), item.name, style=f"text;html=1;align=center;verticalAlign=middle;fontSize={int(TOKENS.node_name_font_size)};fontStyle=1;fontColor=#1F1F1F;fontFamily=Arial;fillColor=none;strokeColor=none;whiteSpace=wrap;", vertex="1", parent=node_id)
        _geometry(name, node_layout.title_bounds.x - box.x, name_y, node_layout.title_bounds.width, name_height)
        for contained_item in node_layout.contained:
            prefix = {"execution-environment": "runtime", "deployed-artifact": "artifact", "device-context": "device-context"}[contained_item.visual_kind]
            contained = _cell(
                cells,
                next_id(prefix),
                _rich_label(contained_item.stereotype, contained_item.label),
                style=_contained_style(contained_item.visual_kind),
                vertex="1",
                parent=node_id,
            )
            bounds = contained_item.bounds
            _geometry(contained, bounds.x - box.x, bounds.y - box.y, bounds.width, bounds.height)
        if node_layout.subtitle:
            subtitle, subtitle_bounds = node_layout.subtitle
            note = _cell(cells, next_id("subtitle"), subtitle, style=f"text;html=1;align=center;verticalAlign=middle;fontSize={int(TOKENS.subtitle_font_size)};fontStyle=2;fontColor=#454545;fontFamily=Arial;fillColor=none;strokeColor=none;whiteSpace=wrap;", vertex="1", parent=node_id)
            _geometry(note, subtitle_bounds.x - box.x, subtitle_bounds.y - box.y, subtitle_bounds.width, subtitle_bounds.height)

    for relation in relations.values():
        if relation.type == "communication_path":
            _edge(
                cells,
                next_id("communication"),
                node_cells[relation.source],
                node_cells[relation.target],
                layout.nodes[relation.source].box,
                layout.nodes[relation.target].box,
                layout.communication_paths[relation.id],
                f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;startArrow=none;strokeColor=#303030;strokeWidth={TOKENS.connector_stroke_width};",
            )

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
