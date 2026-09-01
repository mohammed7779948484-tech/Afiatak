from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.aafiatak_main_use_case_drawio import (
    ACTORS,
    BOUNDARY,
    CANVAS,
    DEPENDENCY_LABELS,
    EXTEND_CONDITION,
    FIELDS,
    GROUP_FOR_USE_CASE,
    ROUTES,
    TITLE,
    USE_CASES,
    Box,
)

PALETTE = {
    "access": {"field": "#F5F8FF", "fill": "#E6EEFC", "stroke": "#5D78A8"},
    "patient": {"field": "#F3FAF7", "fill": "#E3F3EA", "stroke": "#4F876B"},
    "facility": {"field": "#FFF9F0", "fill": "#FCEED8", "stroke": "#A7783B"},
    "operations": {"field": "#F7F4FC", "fill": "#EDE7F7", "stroke": "#74629C"},
    "platform": {"field": "#FFF5F8", "fill": "#F8E5EC", "stroke": "#9B5C70"},
}


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-")


def _cell(root: ET.Element, cell_id: str, value: str = "", **attrs: object) -> ET.Element:
    data = {"id": cell_id, "value": value}
    data.update({key: str(value) for key, value in attrs.items()})
    return ET.SubElement(root, "mxCell", data)


def _geometry(node: ET.Element, box: Box | None = None, *, relative: bool = False) -> ET.Element:
    attrs: dict[str, str] = {"as": "geometry"}
    if relative:
        attrs["relative"] = "1"
    if box is not None:
        attrs.update(
            {
                "x": f"{box.x:.0f}",
                "y": f"{box.y:.0f}",
                "width": f"{box.width:.0f}",
                "height": f"{box.height:.0f}",
            }
        )
    return ET.SubElement(node, "mxGeometry", attrs)


def _waypoints(geometry: ET.Element, points: tuple[tuple[float, float], ...]) -> None:
    if not points:
        return
    array = ET.SubElement(geometry, "Array", {"as": "points"})
    for x, y in points:
        ET.SubElement(array, "mxPoint", {"x": f"{x:.0f}", "y": f"{y:.0f}"})


def _actor_style(external: bool) -> str:
    if external:
        return (
            "rounded=1;arcSize=12;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
            "fillColor=#F7F8FA;strokeColor=#667085;strokeWidth=1.6;fontColor=#2B3340;"
            "fontFamily=Arial;fontSize=18;spacing=8;shadow=0;"
        )
    return (
        "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
        "whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#283443;strokeWidth=1.8;"
        "fontColor=#1F2937;fontFamily=Arial;fontSize=18;fontStyle=1;"
    )


def _use_case_style(group: str) -> str:
    palette = PALETTE[group]
    return (
        "ellipse;perimeter=ellipsePerimeter;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
        f"fillColor={palette['fill']};strokeColor={palette['stroke']};strokeWidth=1.8;"
        "fontColor=#202936;fontFamily=Arial;fontSize=17;fontStyle=0;spacing=8;shadow=0;"
    )


def _association_style(route) -> str:
    return (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "endArrow=none;startArrow=none;strokeColor=#566170;strokeWidth=1.6;"
        f"exitX={route.exit_x:.3f};exitY={route.exit_y:.3f};exitDx=0;exitDy=0;"
        f"entryX={route.entry_x:.3f};entryY={route.entry_y:.3f};entryDx=0;entryDy=0;"
    )


def _dependency_style(route) -> str:
    return (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "dashed=1;dashPattern=8 5;endArrow=open;endFill=0;startArrow=none;"
        "strokeColor=#364152;strokeWidth=1.8;"
        f"exitX={route.exit_x:.3f};exitY={route.exit_y:.3f};exitDx=0;exitDy=0;"
        f"entryX={route.entry_x:.3f};entryY={route.entry_y:.3f};entryDx=0;entryDy=0;"
    )


def _field_style(group: str) -> str:
    return (
        "rounded=1;arcSize=18;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
        f"fillColor={PALETTE[group]['field']};strokeColor={PALETTE[group]['stroke']};"
        "strokeWidth=1;fontColor=#3A4655;fontFamily=Arial;fontSize=17;fontStyle=1;"
        "spacingTop=12;spacingLeft=14;pointerEvents=0;shadow=0;"
    )


def _label_style(*, italic: bool = False, size: int = 15, align: str = "center") -> str:
    font_style = 2 if italic else 0
    return (
        f"text;html=1;align={align};verticalAlign=middle;whiteSpace=wrap;"
        f"fontColor=#374151;fontFamily=Arial;fontSize={size};fontStyle={font_style};"
        "fillColor=none;strokeColor=none;spacing=2;"
    )


def _node_map(model, view) -> dict[str, object]:
    selected = set(view.include)
    return {item.id: item for item in model.elements if item.id in selected}


def _validate_written_drawio(output: Path, expected_node_ids: set[str], expected_relation_ids: set[str]) -> None:
    try:
        root = ET.parse(output).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"generated draw.io XML is not well-formed: {exc}") from exc
    if root.tag != "mxfile":
        raise ValueError("generated draw.io XML must use mxfile as the document root")
    graph = root.find("./diagram/mxGraphModel")
    if graph is None:
        raise ValueError("generated draw.io XML is missing mxGraphModel")
    cells = list(graph.findall("./root/mxCell"))
    by_id = {cell.attrib.get("id", ""): cell for cell in cells}
    if len(by_id) != len(cells) or "" in by_id:
        raise ValueError("generated draw.io XML contains missing or duplicate mxCell IDs")
    if "0" not in by_id or "1" not in by_id or by_id["1"].get("parent") != "0":
        raise ValueError("generated draw.io XML is missing mandatory root/default-layer cells")
    for cell_id, cell in by_id.items():
        if cell_id == "0":
            continue
        parent = cell.get("parent")
        if parent not in by_id:
            raise ValueError(f"generated draw.io cell {cell_id} has invalid parent {parent!r}")
        if cell.get("edge") == "1":
            if cell.get("vertex") is not None:
                raise ValueError(f"generated draw.io edge {cell_id} cannot also be a vertex")
            if cell.get("source") not in by_id or cell.get("target") not in by_id:
                raise ValueError(f"generated draw.io edge {cell_id} has an invalid endpoint")
            geometry = cell.find("mxGeometry")
            if geometry is None or geometry.get("relative") != "1":
                raise ValueError(f"generated draw.io edge {cell_id} requires relative mxGeometry")
    rendered_nodes = {cell_id for cell_id in by_id if cell_id.startswith("node-")}
    rendered_edges = {cell_id for cell_id, cell in by_id.items() if cell.get("edge") == "1"}
    expected_nodes = {f"node-{_safe_id(item_id)}" for item_id in expected_node_ids}
    expected_edges = {f"edge-{_safe_id(relation_id)}" for relation_id in expected_relation_ids}
    if rendered_nodes != expected_nodes:
        raise ValueError("generated draw.io node inventory does not match the approved view")
    if rendered_edges != expected_edges:
        raise ValueError("generated draw.io relationship inventory does not match the approved view")


def export_main_use_case_drawio(model, view, output: Path) -> Path:
    if view.id != "aafiatak-main-use-case" or view.diagram_type != "use_case":
        raise ValueError("native main-use-case exporter only supports aafiatak-main-use-case")

    selected = _node_map(model, view)
    relations = {item.id: item for item in model.relations if item.id in set(view.relations)}
    required_nodes = set(ACTORS) | set(USE_CASES)
    if set(selected) != required_nodes:
        missing = sorted(required_nodes - set(selected))
        extra = sorted(set(selected) - required_nodes)
        raise ValueError(f"draw.io composition/view mismatch; missing={missing}, extra={extra}")
    if set(relations) != set(ROUTES):
        missing = sorted(set(ROUTES) - set(relations))
        extra = sorted(set(relations) - set(ROUTES))
        raise ValueError(f"draw.io route/view mismatch; missing={missing}, extra={extra}")

    root = ET.Element("mxfile", {"host": "app.diagrams.net", "type": "device"})
    diagram = ET.SubElement(root, "diagram", {"id": view.id, "name": view.title})
    graph = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1800",
            "dy": "1000",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(CANVAS[0]),
            "pageHeight": str(CANVAS[1]),
            "background": "#FFFFFF",
            "math": "0",
            "shadow": "0",
            "adaptiveColors": "none",
        },
    )
    cells = ET.SubElement(graph, "root")
    ET.SubElement(cells, "mxCell", {"id": "0"})
    ET.SubElement(cells, "mxCell", {"id": "1", "value": "Background", "parent": "0"})
    ET.SubElement(cells, "mxCell", {"id": "layer-relationships", "value": "Relationships", "parent": "0"})
    ET.SubElement(cells, "mxCell", {"id": "layer-elements", "value": "Diagram Elements", "parent": "0"})
    ET.SubElement(cells, "mxCell", {"id": "layer-labels", "value": "Relationship Labels", "parent": "0"})

    boundary = _cell(
        cells,
        "system-boundary",
        "",
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#22344D;strokeWidth=2.4;shadow=0;pointerEvents=0;",
        vertex="1",
        parent="1",
    )
    _geometry(boundary, BOUNDARY)

    title = _cell(
        cells,
        "diagram-title",
        view.title,
        style="text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;fontColor=#17263B;fontFamily=Arial;fontSize=28;fontStyle=1;fillColor=none;strokeColor=none;",
        vertex="1",
        parent="1",
    )
    _geometry(title, TITLE)

    system_label = _cell(
        cells,
        "system-name",
        str(view.options.get("systemName", "Aafiatak Medical Appointment Booking System")),
        style="text;html=1;align=right;verticalAlign=middle;whiteSpace=wrap;fontColor=#5A6676;fontFamily=Arial;fontSize=15;fontStyle=2;fillColor=none;strokeColor=none;",
        vertex="1",
        parent="1",
    )
    _geometry(system_label, Box(1640, 280, 850, 30))

    for label, box, group in FIELDS:
        field = _cell(cells, f"field-{group}", label, style=_field_style(group), vertex="1", parent="1")
        _geometry(field, box)

    node_cell_ids: dict[str, str] = {}
    for item_id, box in ACTORS.items():
        item = selected[item_id]
        cell_id = f"node-{_safe_id(item_id)}"
        node_cell_ids[item_id] = cell_id
        external = item_id in {
            "actor.payment-gateway",
            "actor.notification-service",
            "actor.map-service",
            "actor.whatsapp-auth-provider",
        }
        value = f"<i>«external system»</i><br><b>{item.name}</b>" if external else item.name
        node = _cell(cells, cell_id, value, style=_actor_style(external), vertex="1", parent="layer-elements")
        _geometry(node, box)

    for item_id, box in USE_CASES.items():
        item = selected[item_id]
        cell_id = f"node-{_safe_id(item_id)}"
        node_cell_ids[item_id] = cell_id
        node = _cell(
            cells,
            cell_id,
            item.name,
            style=_use_case_style(GROUP_FOR_USE_CASE[item_id]),
            vertex="1",
            parent="layer-elements",
        )
        _geometry(node, box)

    for relation_id in view.relations:
        relation = relations[relation_id]
        route = ROUTES[relation_id]
        style = _association_style(route) if relation.type == "association" else _dependency_style(route)
        edge = _cell(
            cells,
            f"edge-{_safe_id(relation_id)}",
            "",
            style=style,
            edge="1",
            parent="layer-relationships",
            source=node_cell_ids[relation.source],
            target=node_cell_ids[relation.target],
        )
        geometry = _geometry(edge, relative=True)
        _waypoints(geometry, route.waypoints)

    for relation_id, box in DEPENDENCY_LABELS.items():
        relation = relations[relation_id]
        label = "«include»" if relation.type == "include" else "«extend»"
        cell = _cell(
            cells,
            f"label-{_safe_id(relation_id)}",
            label,
            style=_label_style(italic=True, size=15),
            vertex="1",
            parent="layer-labels",
        )
        _geometry(cell, box)

    condition = relations["relation.ext-01"].metadata.get("condition", "")
    if condition:
        cell = _cell(
            cells,
            "label-relation-ext-01-condition",
            str(condition),
            style=_label_style(italic=False, size=14, align="center"),
            vertex="1",
            parent="layer-labels",
        )
        _geometry(cell, EXTEND_CONDITION)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True, short_empty_elements=True)
    _validate_written_drawio(output, set(view.include), set(view.relations))
    return output
