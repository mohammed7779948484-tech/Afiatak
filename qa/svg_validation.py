from __future__ import annotations

import math
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


def _number(node: ET.Element, name: str) -> float:
    return float(node.attrib[name])


def _box(node: ET.Element) -> tuple[float, float, float, float]:
    return tuple(_number(node, key) for key in ("data-x", "data-y", "data-width", "data-height"))


def _overlap(a: tuple[float, ...], b: tuple[float, ...], *, inset: float = 0) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax + inset < bx + bw and bx + inset < ax + aw and ay + inset < by + bh and by + inset < ay + ah


def _inside(inner: tuple[float, ...], outer: tuple[float, ...]) -> bool:
    x, y, width, height = inner
    ox, oy, ow, oh = outer
    return ox <= x and oy <= y and x + width <= ox + ow and y + height <= oy + oh


def _segment_distance(point, first, second) -> float:
    px, py = point
    ax, ay = first
    bx, by = second
    dx, dy = bx - ax, by - ay
    if dx == dy == 0:
        return math.hypot(px - ax, py - ay)
    ratio = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + ratio * dx), py - (ay + ratio * dy))


def _touches(kind: str, box: tuple[float, ...], point: tuple[float, float]) -> bool:
    x, y, width, height = box
    if kind == "use_case":
        rx, ry = width / 2, height / 2
        value = ((point[0] - x - rx) / rx) ** 2 + ((point[1] - y - ry) / ry) ** 2
        return abs(value - 1) <= 0.12
    centre = x + width / 2
    head = (centre, y + 19)
    if abs(math.hypot(point[0] - head[0], point[1] - head[1]) - 10) <= 2.5:
        return True
    segments = (
        ((centre, y + 29), (centre, y + 58)),
        ((centre - 25, y + 42), (centre + 25, y + 42)),
        ((centre, y + 58), (centre - 23, y + 82)),
        ((centre, y + 58), (centre + 23, y + 82)),
    )
    return any(_segment_distance(point, first, second) <= 2.5 for first, second in segments)


def validate_svg(path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [Diagnostic("Q4", "invalid-svg", str(exc), subject=str(path))]
    if root.tag.rsplit("}", 1)[-1] != "svg" or not root.get("viewBox"):
        diagnostics.append(Diagnostic("Q4", "invalid-svg-root", "SVG root and viewBox are required"))

    all_ids = [node.get("id") for node in root.iter() if node.get("id")]
    if len(all_ids) != len(set(all_ids)):
        diagnostics.append(Diagnostic("Q4", "duplicate-svg-id", "SVG IDs must be unique"))

    semantic_nodes = [node for node in root.iter() if node.get("data-semantic-id")]
    semantic_ids = [node.get("data-semantic-id") for node in semantic_nodes]
    if set(semantic_ids) != set(view.include) or len(semantic_ids) != len(set(semantic_ids)):
        diagnostics.append(Diagnostic("Q4", "semantic-coverage", "SVG must represent each selected semantic element exactly once"))
    relation_nodes = [node for node in root.iter() if node.get("data-relation-id")]
    relation_ids = [node.get("data-relation-id") for node in relation_nodes]
    if set(relation_ids) != set(view.relations) or len(relation_ids) != len(set(relation_ids)):
        diagnostics.append(Diagnostic("Q4", "relation-coverage", "SVG must represent each selected relation exactly once"))

    boundary_node = next((node for node in root.iter() if node.get("id") == "system-boundary"), None)
    if boundary_node is None:
        diagnostics.append(Diagnostic("Q4", "missing-boundary", "System boundary is required"))
        return diagnostics
    try:
        boundary = _box(boundary_node)
        use_cases = [(node.get("data-semantic-id"), _box(node)) for node in semantic_nodes if node.get("data-kind") == "use_case"]
        actors = [(node.get("data-semantic-id"), _box(node)) for node in semantic_nodes if node.get("data-kind") == "actor"]
    except (KeyError, ValueError) as exc:
        diagnostics.append(Diagnostic("Q4", "invalid-bounds", str(exc)))
        return diagnostics
    for item_id, box in use_cases:
        if not _inside(box, boundary):
            diagnostics.append(Diagnostic("Q5", "use-case-outside-boundary", "Use case must be inside the system boundary", subject=item_id))
    for item_id, box in actors:
        if _overlap(box, boundary):
            diagnostics.append(Diagnostic("Q5", "actor-inside-boundary", "Actor must remain outside the system boundary", subject=item_id))
    for index, (first_id, first) in enumerate(use_cases):
        for second_id, second in use_cases[index + 1 :]:
            if _overlap(first, second):
                diagnostics.append(Diagnostic("Q5", "semantic-overlap", f"Overlaps {second_id}", subject=first_id))

    relation_by_id = {item.id: item for item in model.relations}
    boxes = {item_id: box for item_id, box in [*use_cases, *actors]}
    kinds = {node.get("data-semantic-id"): node.get("data-kind") for node in semantic_nodes}
    for node in relation_nodes:
        relation_id = node.get("data-relation-id")
        relation = relation_by_id.get(relation_id)
        if relation is None:
            continue
        try:
            points = [tuple(map(float, item.split(","))) for item in node.get("data-points", "").split()]
        except ValueError as exc:
            diagnostics.append(Diagnostic("Q4", "invalid-route", str(exc), subject=relation_id))
            continue
        if len(points) < 2 or not _touches(kinds[relation.source], boxes[relation.source], points[0]) or not _touches(kinds[relation.target], boxes[relation.target], points[-1]):
            diagnostics.append(Diagnostic("Q5", "relation-direction", "Route must start at its UML source and end at its UML target", subject=relation_id))
            continue
        for first, second in zip(points, points[1:], strict=False):
            if first[0] != second[0] and first[1] != second[1]:
                continue
            for item_id, box in boxes.items():
                if item_id in {relation.source, relation.target}:
                    continue
                x, y, width, height = box
                if first[0] == second[0]:
                    crosses = x < first[0] < x + width and max(first[1], second[1]) > y and min(first[1], second[1]) < y + height
                else:
                    crosses = y < first[1] < y + height and max(first[0], second[0]) > x and min(first[0], second[0]) < x + width
                if crosses:
                    diagnostics.append(Diagnostic("Q5", "connector-through-node", f"Connector crosses {item_id}", subject=relation_id))
    return diagnostics
