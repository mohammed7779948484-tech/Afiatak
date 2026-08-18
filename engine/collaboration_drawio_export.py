"""Editable diagrams.net exporter backed by the shared collaboration render plan."""
from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.collaboration_geometry import build_collaboration_render_plan


def cell(root, cell_id: str, value: str = "", **attrs):
    return ET.SubElement(root, "mxCell", {"id": cell_id, "value": value, **{key: str(value) for key, value in attrs.items()}})


def geometry(node, x: float, y: float, width: float, height: float):
    return ET.SubElement(node, "mxGeometry", {"x": f"{x:.2f}", "y": f"{y:.2f}", "width": f"{width:.2f}", "height": f"{height:.2f}", "as": "geometry"})


def polyline_edge(root, cell_id: str, points, style: str):
    edge = cell(root, cell_id, "", style=style, edge="1", parent="1")
    geo = ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    ET.SubElement(geo, "mxPoint", {"x": f"{points[0].x:.2f}", "y": f"{points[0].y:.2f}", "as": "sourcePoint"})
    ET.SubElement(geo, "mxPoint", {"x": f"{points[-1].x:.2f}", "y": f"{points[-1].y:.2f}", "as": "targetPoint"})
    if len(points) > 2:
        route = ET.SubElement(geo, "Array", {"as": "points"})
        for point in points[1:-1]:
            ET.SubElement(route, "mxPoint", {"x": f"{point.x:.2f}", "y": f"{point.y:.2f}"})
    return edge


def export_collaboration_drawio(model, view, output: Path) -> None:
    plan = build_collaboration_render_plan(model, view)
    root = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "31.1.8", "type": "device"})
    diagram = ET.SubElement(root, "diagram", {"id": view.id, "name": view.title})
    graph = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1600", "dy": "1000", "grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1", "pageScale": "1",
            "pageWidth": str(int(plan.canvas.width)), "pageHeight": str(int(plan.canvas.height)), "math": "0", "shadow": "0",
        },
    )
    cells = ET.SubElement(graph, "root")
    cell(cells, "0")
    cell(cells, "1", parent="0")
    counter = 2

    def next_id(prefix: str) -> str:
        nonlocal counter
        result = f"{prefix}-{counter}"
        counter += 1
        return result

    page = cell(cells, next_id("page"), "", style="rounded=0;html=1;fillColor=#FFFFFF;strokeColor=none;pointerEvents=0;", vertex="1", parent="1")
    geometry(page, plan.canvas.x, plan.canvas.y, plan.canvas.width, plan.canvas.height)
    heading_value = "<br/>".join(plan.heading.lines)
    heading = cell(cells, next_id("heading"), heading_value, style="text;html=1;align=left;verticalAlign=top;fontSize=58;fontStyle=1;fontColor=#8B1E1E;fontFamily=Times New Roman;fillColor=none;strokeColor=none;whiteSpace=wrap;spacingLeft=0;spacingTop=0;", vertex="1", parent="1")
    geometry(heading, plan.heading.bounds.x, plan.heading.bounds.y, plan.heading.bounds.width, plan.heading.bounds.height)

    for participant in plan.participants.values():
        bounds = participant.bounds
        node = cell(cells, next_id("participant"), f"<u>{participant.element.name}</u>", style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#222222;strokeWidth=2.5;fontColor=#222222;fontFamily=Times New Roman;fontSize=48;fontStyle=4;align=center;verticalAlign=middle;", vertex="1", parent="1")
        geometry(node, bounds.x, bounds.y, bounds.width, bounds.height)

    for link in plan.links.values():
        polyline_edge(cells, next_id(f"link-{link.link_id}"), link.polyline.points, "html=1;endArrow=none;startArrow=none;strokeColor=#777777;strokeWidth=2;rounded=0;")

    for run in plan.runs.values():
        arrows = {arrow.relation.id: arrow for arrow in run.arrows}
        for label in run.labels:
            arrow = arrows[label.relation.id]
            polyline_edge(cells, next_id(f"message-{label.relation.metadata['sequence']}"), (arrow.segment.start, arrow.segment.end), "html=1;endArrow=block;endFill=1;strokeColor=#555555;strokeWidth=2;rounded=0;")
            value = f"{label.text.number}&nbsp;&nbsp;" + "<br/>".join(label.text.lines)
            text = cell(cells, next_id("message-label"), value, style="text;html=1;align=left;verticalAlign=top;fontSize=50;fontColor=#333333;fontFamily=Times New Roman;fillColor=none;strokeColor=none;whiteSpace=wrap;spacingLeft=0;spacingTop=0;", vertex="1", parent="1")
            bounds = label.text.bounds
            geometry(text, bounds.x, bounds.y, bounds.width, bounds.height)

    for loop in plan.loops:
        polyline_edge(cells, next_id(f"self-{loop.relation.metadata['sequence']}"), loop.path.points, "html=1;endArrow=block;endFill=1;strokeColor=#555555;strokeWidth=2;rounded=1;curved=1;")
        label = loop.label
        value = f"{label.text.number}&nbsp;&nbsp;" + "<br/>".join(label.text.lines)
        text = cell(cells, next_id("self-label"), value, style="text;html=1;align=left;verticalAlign=top;fontSize=50;fontColor=#333333;fontFamily=Times New Roman;fillColor=none;strokeColor=none;whiteSpace=wrap;spacingLeft=0;spacingTop=0;", vertex="1", parent="1")
        bounds = label.text.bounds
        geometry(text, bounds.x, bounds.y, bounds.width, bounds.height)

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
