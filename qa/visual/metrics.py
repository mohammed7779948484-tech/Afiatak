from __future__ import annotations

import math
import statistics
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.io import ROOT, load_yaml

Point = tuple[float, float]
Rect = tuple[float, float, float, float]


def _style(style: str | None) -> dict[str, str]:
    return {
        key: value
        for part in (style or "").split(";")
        if "=" in part
        for key, value in [part.split("=", 1)]
    }


def _rect(cell: ET.Element) -> Rect | None:
    geometry = cell.find("mxGeometry")
    if geometry is None or geometry.get("relative") == "1":
        return None
    try:
        return (
            float(geometry.get("x", 0)),
            float(geometry.get("y", 0)),
            float(geometry.get("width", "nan")),
            float(geometry.get("height", "nan")),
        )
    except (KeyError, ValueError):
        return None


def _absolute_rect(cell_id: str, cells: dict[str, ET.Element]) -> Rect | None:
    cell = cells.get(cell_id)
    box = _rect(cell) if cell is not None else None
    if cell is None or box is None:
        return None
    x, y, width, height = box
    parent = cell.get("parent")
    seen: set[str] = set()
    while parent in cells and parent not in seen:
        seen.add(parent)
        owner = cells[parent]
        owner_box = _rect(owner)
        if owner_box is not None and owner.get("vertex") == "1":
            x += owner_box[0]
            y += owner_box[1]
        parent = owner.get("parent")
    return x, y, width, height


def _centre(box: Rect) -> Point:
    return box[0] + box[2] / 2, box[1] + box[3] / 2


def _endpoint(edge: ET.Element, end: str, cells: dict[str, ET.Element]) -> Point | None:
    box = _absolute_rect(edge.get(end, ""), cells)
    if box is None:
        return None
    style = _style(edge.get("style"))
    prefix = "exit" if end == "source" else "entry"
    try:
        x_factor = float(style.get(f"{prefix}X", 0.5))
        y_factor = float(style.get(f"{prefix}Y", 0.5))
    except ValueError:
        x_factor = y_factor = 0.5
    return box[0] + x_factor * box[2], box[1] + y_factor * box[3]


def _route(edge: ET.Element, cells: dict[str, ET.Element]) -> list[Point] | None:
    source = _endpoint(edge, "source", cells)
    target = _endpoint(edge, "target", cells)
    geometry = edge.find("mxGeometry")
    points = geometry.find("Array") if geometry is not None else None
    if source is None or target is None:
        return None
    route = [source]
    if points is not None:
        for point in points.findall("mxPoint"):
            try:
                route.append((float(point.get("x", "nan")), float(point.get("y", "nan"))))
            except (KeyError, ValueError):
                continue
    route.append(target)
    return route


def _simplify(points: list[Point]) -> list[Point]:
    result: list[Point] = []
    for point in points:
        if result and point == result[-1]:
            continue
        while len(result) > 1:
            first, second = result[-2], result[-1]
            cross = (second[0] - first[0]) * (point[1] - second[1]) - (
                second[1] - first[1]
            ) * (point[0] - second[0])
            if abs(cross) > 1e-9:
                break
            result.pop()
        result.append(point)
    return result


def _orientation(a: Point, b: Point, c: Point) -> int:
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return 0 if abs(value) < 1e-9 else (1 if value > 0 else -1)


def _segments_cross(a: Point, b: Point, c: Point, d: Point) -> bool:
    first = (_orientation(a, b, c), _orientation(a, b, d))
    second = (_orientation(c, d, a), _orientation(c, d, b))
    return first[0] != first[1] and second[0] != second[1] and 0 not in (*first, *second)


def _routes_cross(first: list[Point], second: list[Point]) -> bool:
    return any(
        _segments_cross(a, b, c, d)
        for a, b in zip(first, first[1:])
        for c, d in zip(second, second[1:])
    )


def _route_hits_rect(points: list[Point], box: Rect) -> bool:
    x, y, width, height = box
    corners = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
    borders = list(zip(corners, corners[1:] + corners[:1]))
    for first, second in zip(points, points[1:]):
        if x < first[0] < x + width and y < first[1] < y + height:
            return True
        if any(_segments_cross(first, second, a, b) for a, b in borders):
            return True
    return False


def _overlap(first: Rect, second: Rect) -> bool:
    return (
        first[0] < second[0] + second[2]
        and second[0] < first[0] + first[2]
        and first[1] < second[1] + second[3]
        and second[1] < first[1] + first[3]
    )


def _expand(box: Rect, amount: float) -> Rect:
    return box[0] - amount, box[1] - amount, box[2] + 2 * amount, box[3] + 2 * amount


def _rounded(value: float | None) -> float | None:
    return round(value, 3) if value is not None else None


def analyze_visual_metrics(path: Path | str) -> dict:
    root = ET.parse(path).getroot()
    model = root.find(".//mxGraphModel")
    page_width = float(model.get("pageWidth", 0)) if model is not None else 0.0
    page_height = float(model.get("pageHeight", 0)) if model is not None else 0.0

    cells: dict[str, ET.Element] = {}
    metadata: dict[str, dict[str, str]] = {}
    for item in root.findall(".//mxCell"):
        cell_id = item.get("id")
        if cell_id:
            cells[cell_id] = item
    for wrapper in root.findall(".//object"):
        cell = wrapper.find("mxCell")
        wrapper_id = wrapper.get("id")
        if cell is not None and wrapper_id:
            cells[wrapper_id] = cell
            metadata[wrapper_id] = dict(wrapper.attrib)

    boxes = {
        cell_id: box
        for cell_id in cells
        if (box := _absolute_rect(cell_id, cells)) is not None
    }
    semantic_types = {
        cell_id: values.get("semanticType") for cell_id, values in metadata.items()
    }
    actors = sorted(cell_id for cell_id, kind in semantic_types.items() if kind == "actor")
    use_cases = sorted(cell_id for cell_id, kind in semantic_types.items() if kind == "use_case")
    semantic_nodes = actors + use_cases
    edges = sorted(
        (cell_id, cell) for cell_id, cell in cells.items() if cell.get("edge") == "1"
    )
    routes = {
        edge_id: _simplify(points)
        for edge_id, edge in edges
        if (points := _route(edge, cells)) is not None
    }
    measured_routes = dict(routes)
    for edge_id, edge in edges:
        if edge_id in measured_routes:
            continue
        source = _endpoint(edge, "source", cells)
        target = _endpoint(edge, "target", cells)
        if source is not None and target is not None:
            measured_routes[edge_id] = [source, target]

    crossing_pairs: list[list[str]] = []
    routed_items = sorted(routes.items())
    for index, (first_id, first_route) in enumerate(routed_items):
        for second_id, second_route in routed_items[index + 1 :]:
            first = cells[first_id]
            second = cells[second_id]
            if {first.get("source"), first.get("target")} & {
                second.get("source"),
                second.get("target"),
            }:
                continue
            if _routes_cross(first_route, second_route):
                crossing_pairs.append([first_id, second_id])

    route_through: list[dict[str, str]] = []
    geometry_tokens = load_yaml(ROOT / "design" / "geometry.yaml")["quality"]
    clearance = float(geometry_tokens["minimum_connector_clearance"])
    actor_label_clearance = float(geometry_tokens["minimum_actor_label_clearance"])
    clearance_violations: list[dict[str, str]] = []
    for edge_id, points in routed_items:
        edge = cells[edge_id]
        endpoints = {edge.get("source"), edge.get("target")}
        for node_id in semantic_nodes:
            node_box = boxes[node_id]
            if node_id in actors:
                node_box = (
                    node_box[0],
                    node_box[1],
                    node_box[2],
                    node_box[3] + actor_label_clearance,
                )
            if node_id not in endpoints and _route_hits_rect(points, node_box):
                route_through.append({"edge": edge_id, "node": node_id})
            if node_id not in endpoints and _route_hits_rect(points, _expand(node_box, clearance)):
                clearance_violations.append({"edge": edge_id, "node": node_id})

    overlap_pairs = [
        [first, second]
        for index, first in enumerate(semantic_nodes)
        for second in semantic_nodes[index + 1 :]
        if _overlap(boxes[first], boxes[second])
    ]
    lengths = {
        edge_id: sum(math.dist(first, second) for first, second in zip(points, points[1:]))
        for edge_id, points in sorted(measured_routes.items())
    }
    bends = {edge_id: max(0, len(points) - 2) for edge_id, points in routed_items}

    boundary = boxes.get("system-boundary")
    boundary_area = boundary[2] * boundary[3] if boundary else 0.0
    internal_area = sum(boxes[item][2] * boxes[item][3] for item in use_cases)
    all_boxes = [boxes[item] for item in semantic_nodes]
    occupied_bbox = None
    if all_boxes:
        min_x = min(item[0] for item in all_boxes)
        min_y = min(item[1] for item in all_boxes)
        max_x = max(item[0] + item[2] for item in all_boxes)
        max_y = max(item[1] + item[3] for item in all_boxes)
        occupied_bbox = [min_x, min_y, max_x - min_x, max_y - min_y]

    zone_balance = {"detectable": False, "method": None, "counts": None, "imbalance": None}
    zone_counts: dict[str, int] = {}
    for node_id in use_cases:
        zone = metadata.get(node_id, {}).get("presentationZone")
        if zone:
            zone_counts[zone] = zone_counts.get(zone, 0) + 1
    if zone_counts:
        counts = list(zone_counts.values())
        mean = statistics.fmean(counts)
        zone_balance = {
            "detectable": True,
            "method": "presentation-zones",
            "counts": dict(sorted(zone_counts.items())),
            "imbalance": _rounded((max(counts) - min(counts)) / mean if mean else 0.0),
        }

    grid_columns, grid_rows = 6, 4
    congestion_counts = [0] * (grid_columns * grid_rows)
    if page_width and page_height:
        cell_width = page_width / grid_columns
        cell_height = page_height / grid_rows
        for points in routes.values():
            for first, second in zip(points, points[1:]):
                distance = math.dist(first, second)
                steps = max(1, math.ceil(distance / min(cell_width, cell_height)))
                visited = set()
                for step in range(steps + 1):
                    ratio = step / steps
                    x = first[0] + (second[0] - first[0]) * ratio
                    y = first[1] + (second[1] - first[1]) * ratio
                    column = min(grid_columns - 1, max(0, int(x / page_width * grid_columns)))
                    row = min(grid_rows - 1, max(0, int(y / page_height * grid_rows)))
                    visited.add(row * grid_columns + column)
                for index in visited:
                    congestion_counts[index] += 1
    congestion_mean = statistics.fmean(congestion_counts) if congestion_counts else 0.0

    association_lengths: dict[str, list[float]] = {actor: [] for actor in actors}
    association_edge_count = 0
    for edge_id, edge in edges:
        actor = next(
            (item for item in (edge.get("source"), edge.get("target")) if item in association_lengths),
            None,
        )
        other = edge.get("target") if edge.get("source") == actor else edge.get("source")
        if actor and other in use_cases and edge_id in lengths:
            association_edge_count += 1
            association_lengths[actor].append(lengths[edge_id])
    all_association_lengths = [value for values in association_lengths.values() for value in values]

    typography = load_yaml(ROOT / "design" / "typography.yaml")
    minimum_font_size = float(typography["minimum_size"])
    label_warnings: list[dict[str, str]] = []
    for cell_id in semantic_nodes:
        style = _style(cells[cell_id].get("style"))
        try:
            font_size = float(style.get("fontSize", typography["node"]["size"]))
        except (TypeError, ValueError):
            font_size = float(typography["node"]["size"])
        if font_size < minimum_font_size:
            label_warnings.append(
                {
                    "code": "label-font-too-small",
                    "subject": cell_id,
                    "message": f"Label font size {font_size:g}px is below {minimum_font_size:g}px",
                }
            )

    inconsistent_warnings: list[dict[str, str]] = []
    for kind, node_ids in (("actor", actors), ("use_case", use_cases)):
        if len(node_ids) < 2:
            continue
        widths = [boxes[item][2] for item in node_ids]
        heights = [boxes[item][3] for item in node_ids]
        median_width = statistics.median(widths)
        median_height = statistics.median(heights)
        outliers = [
            item
            for item in node_ids
            if abs(boxes[item][2] - median_width) > median_width * 0.1
            or abs(boxes[item][3] - median_height) > median_height * 0.1
        ]
        if outliers:
            inconsistent_warnings.append(
                {
                    "code": "inconsistent-node-size",
                    "subject": kind,
                    "message": f"{kind} geometry varies by more than 10%: {', '.join(outliers)}",
                }
            )

    return {
        "canvas": {"width": page_width, "height": page_height},
        "counts": {
            "useCases": len(use_cases),
            "actors": len(actors),
            "edges": len(edges),
            "routedEdges": len(routes),
            "measuredEdges": len(measured_routes),
            "actorAssociations": association_edge_count,
        },
        "routing": {
            "crossings": len(crossing_pairs),
            "crossingPairs": crossing_pairs,
            "edgeLength": {
                "method": "explicit-polyline-or-endpoint-distance",
                "average": _rounded(statistics.fmean(lengths.values()) if lengths else 0.0),
                "maximum": _rounded(max(lengths.values()) if lengths else 0.0),
                "total": _rounded(sum(lengths.values())),
            },
            "bends": {
                "measuredEdges": len(bends),
                "unknownRouteEdges": len(edges) - len(bends),
                "total": sum(bends.values()),
                "averagePerEdge": _rounded(statistics.fmean(bends.values()) if bends else 0.0),
                "maximumPerEdge": max(bends.values(), default=0),
            },
            "routeThroughNodeCount": len(route_through),
            "routeThroughNodes": route_through,
            "clearance": clearance,
            "clearanceViolationCount": len(clearance_violations),
            "clearanceViolations": clearance_violations,
        },
        "overlap": {"count": len(overlap_pairs), "pairs": overlap_pairs},
        "occupancy": {
            "boundaryCanvasRatio": _rounded(
                boundary_area / (page_width * page_height)
                if boundary_area and page_width and page_height
                else None
            ),
            "internalNodeAreaRatio": _rounded(internal_area / boundary_area if boundary_area else None),
            "contentBoundingBoxCanvasRatio": _rounded(
                occupied_bbox[2] * occupied_bbox[3] / (page_width * page_height)
                if occupied_bbox and page_width and page_height
                else None
            ),
            "contentBoundingBox": occupied_bbox,
        },
        "zoneBalance": zone_balance,
        "congestion": {
            "method": f"segment-midpoints-{grid_columns}x{grid_rows}-grid",
            "maximumSegmentsPerCell": max(congestion_counts, default=0),
            "meanSegmentsPerCell": _rounded(congestion_mean),
            "hotspotCellCount": sum(
                value > max(2.0, congestion_mean * 2) for value in congestion_counts
            ),
        },
        "actorAssociationProximity": {
            "averageRouteLength": _rounded(
                statistics.fmean(all_association_lengths) if all_association_lengths else None
            ),
            "maximumRouteLength": _rounded(max(all_association_lengths) if all_association_lengths else None),
            "perActorAverageRouteLength": {
                actor: _rounded(statistics.fmean(values)) if values else None
                for actor, values in sorted(association_lengths.items())
            },
        },
        "labelAndSizeWarnings": label_warnings + inconsistent_warnings,
    }
