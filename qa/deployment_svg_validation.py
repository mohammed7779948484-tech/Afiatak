from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


FORBIDDEN_KINDS = {
    "actor", "use-case", "lifeline", "activation", "message", "state", "transition",
    "action", "decision", "merge", "fork", "join", "class", "component",
    "provided-interface", "required-interface", "assembly-connector",
}
FORBIDDEN_VISIBLE = (
    "AWS", "Azure", "GCP", "Vercel", "Railway", "VPS", "Docker", "Kubernetes",
    "Load Balancer", "CDN", "Reverse Proxy", "Nginx", "Caddy", "Apache", "API Gateway",
    "Redis", "Cache Server", "Queue Worker", "Message Broker", "Kafka", "RabbitMQ",
    "Object Storage", "File Server", "SMS Gateway", "SMS Provider", "HIS", "EHR",
    "Internal Scheduling Server", "Cashier", "Accounting Server", "Cloud",
)


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def within(self, other: "Rect", margin: float) -> bool:
        return self.x >= other.x + margin and self.y >= other.y + margin and self.right <= other.right - margin and self.bottom <= other.bottom - margin

    def intersects(self, other: "Rect") -> bool:
        return self.x < other.right and self.right > other.x and self.y < other.bottom and self.bottom > other.y


def _rect(value: str) -> Rect:
    x, y, width, height = (float(part) for part in value.split(","))
    return Rect(x, y, width, height)


def _point(value: str) -> tuple[float, float]:
    x, y = (float(part) for part in value.split(","))
    return x, y


def _points(value: str) -> list[tuple[float, float]]:
    return [_point(part) for part in value.split()]


def _nodes(root, kind: str):
    return [node for node in root.iter() if node.attrib.get("data-kind") == kind]


def _expected_count(view: ViewSpec, key: str, fallback: int) -> int:
    return int(view.options.get("expectedCounts", {}).get(key, fallback))


def _point_in_rect(point: tuple[float, float], rect: Rect, strict: bool = True) -> bool:
    x, y = point
    if strict:
        return rect.x < x < rect.right and rect.y < y < rect.bottom
    return rect.x <= x <= rect.right and rect.y <= y <= rect.bottom


def _orientation(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a: tuple[float, float], b: tuple[float, float], p: tuple[float, float]) -> bool:
    return min(a[0], b[0]) - 0.01 <= p[0] <= max(a[0], b[0]) + 0.01 and min(a[1], b[1]) - 0.01 <= p[1] <= max(a[1], b[1]) + 0.01


def _segments_intersect(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float], d: tuple[float, float]) -> bool:
    ab_c = _orientation(a, b, c)
    ab_d = _orientation(a, b, d)
    cd_a = _orientation(c, d, a)
    cd_b = _orientation(c, d, b)
    if (ab_c > 0) != (ab_d > 0) and (cd_a > 0) != (cd_b > 0):
        return True
    return (abs(ab_c) < 0.01 and _on_segment(a, b, c)) or (abs(ab_d) < 0.01 and _on_segment(a, b, d)) or (abs(cd_a) < 0.01 and _on_segment(c, d, a)) or (abs(cd_b) < 0.01 and _on_segment(c, d, b))


def _segments_intersect_rect(points: list[tuple[float, float]], rect: Rect) -> bool:
    corners = ((rect.x, rect.y), (rect.right, rect.y), (rect.right, rect.bottom), (rect.x, rect.bottom))
    edges = tuple(zip(corners, corners[1:] + corners[:1]))
    for start, end in zip(points, points[1:]):
        if _point_in_rect(start, rect) or _point_in_rect(end, rect):
            return True
        if any(_segments_intersect(start, end, edge_start, edge_end) for edge_start, edge_end in edges):
            return True
    return False


def _on_boundary(point: tuple[float, float], rect: Rect, tolerance: float = 12.0) -> bool:
    x, y = point
    horizontal = rect.x - tolerance <= x <= rect.right + tolerance and (abs(y - rect.y) <= tolerance or abs(y - rect.bottom) <= tolerance)
    vertical = rect.y - tolerance <= y <= rect.bottom + tolerance and (abs(x - rect.x) <= tolerance or abs(x - rect.right) <= tolerance)
    return horizontal or vertical


def _geometry_diagnostics(root, nodes, paths) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        page = _rect(root.attrib["data-page-bounds"])
        title_bounds = _rect(root.attrib["data-title-bounds"])
    except (KeyError, ValueError):
        return [Diagnostic("Q5", "geometry-metadata-missing", "Deployment SVG must expose page and title bounds")]

    node_bounds: dict[str, Rect] = {}
    rendered_label_bounds: list[tuple[str, Rect]] = [("title", title_bounds)]
    for node in nodes:
        semantic_id = node.attrib.get("data-semantic-id", "unknown")
        try:
            front = _rect(node.attrib["data-bounds"])
            shape = _rect(node.attrib["data-shape-bounds"])
            name = _rect(node.attrib["data-name-bounds"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "node-geometry-missing", "Deployment node must expose bounds, shape bounds, and name bounds", subject=semantic_id))
            continue
        node_bounds[semantic_id] = front
        rendered_label_bounds.append((f"name:{semantic_id}", name))
        if not shape.within(page, 80):
            diagnostics.append(Diagnostic("Q5", "node-page-bounds", "Deployment node exceeds safe page bounds", subject=semantic_id))
        if not name.within(front, 45):
            diagnostics.append(Diagnostic("Q5", "node-name-bounds", "Deployment node name does not fit safely within the front face", subject=semantic_id))
        if title_bounds.intersects(shape):
            diagnostics.append(Diagnostic("Q5", "title-node-collision", "Diagram title intersects a deployment node", subject=semantic_id))

    for (first_id, first), (second_id, second) in combinations(node_bounds.items(), 2):
        if first.intersects(second):
            diagnostics.append(Diagnostic("Q5", "deployment-node-overlap", "Deployment node front faces overlap", subject=f"{first_id}<->{second_id}"))

    for item in _nodes(root, "deployed-item"):
        owner = item.attrib.get("data-owner-node", "")
        item_name = item.attrib.get("data-item-name", "unknown")
        try:
            bounds = _rect(item.attrib["data-bounds"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "contained-item-geometry-missing", "Contained item requires bounds metadata", subject=item_name))
            continue
        rendered_label_bounds.append((f"item:{item_name}", bounds))
        owner_box = node_bounds.get(owner)
        if owner_box is None or not bounds.within(owner_box, 45):
            diagnostics.append(Diagnostic("Q5", "contained-item-outside-owner", "Contained runtime/component must remain inside its owning deployment node", subject=item_name))

    for subtitle in _nodes(root, "node-subtitle"):
        owner = subtitle.attrib.get("data-owner-node", "")
        try:
            bounds = _rect(subtitle.attrib["data-bounds"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "subtitle-geometry-missing", "Node subtitle requires bounds metadata", subject=owner))
            continue
        rendered_label_bounds.append((f"subtitle:{owner}", bounds))
        owner_box = node_bounds.get(owner)
        if owner_box is None or not bounds.within(owner_box, 25):
            diagnostics.append(Diagnostic("Q5", "node-subtitle-outside-owner", "Node subtitle must remain inside its owning deployment node", subject=owner))

    for (first_id, first), (second_id, second) in combinations(rendered_label_bounds, 2):
        if first.intersects(second):
            diagnostics.append(Diagnostic("Q5", "deployment-label-overlap", "Deployment title, name, contained item, or subtitle labels overlap", subject=f"{first_id}<->{second_id}"))

    path_points: dict[str, list[tuple[float, float]]] = {}
    for path in paths:
        semantic_id = path.attrib.get("data-semantic-id", "unknown")
        source_id = path.attrib.get("data-source-id", "")
        target_id = path.attrib.get("data-target-id", "")
        try:
            points = _points(path.attrib["data-points"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "communication-path-geometry-missing", "Communication path requires parseable route points", subject=semantic_id))
            continue
        path_points[semantic_id] = points
        if len(points) < 2:
            diagnostics.append(Diagnostic("Q5", "communication-path-route-short", "Communication path requires at least two route points", subject=semantic_id))
            continue
        for point in points:
            if not _point_in_rect(point, page, strict=False):
                diagnostics.append(Diagnostic("Q5", "communication-path-page-bounds", "Communication path extends beyond the page", subject=semantic_id))
                break
        for point, endpoint_id in ((points[0], source_id), (points[-1], target_id)):
            box = node_bounds.get(endpoint_id)
            if box is None or not _on_boundary(point, box):
                diagnostics.append(Diagnostic("Q5", "communication-path-detached-node", "Communication path endpoint is detached from its declared node", subject=f"{semantic_id}->{endpoint_id}"))
        for node_id, box in node_bounds.items():
            if node_id not in {source_id, target_id} and _segments_intersect_rect(points, box):
                diagnostics.append(Diagnostic("Q5", "communication-path-through-unrelated-node", "Communication path crosses an unrelated deployment node", subject=f"{semantic_id}->{node_id}"))
        for label_id, bounds in rendered_label_bounds:
            if _segments_intersect_rect(points, bounds):
                diagnostics.append(Diagnostic("Q5", "communication-path-label-collision", "Communication path intersects a diagram, node, or contained-item label", subject=f"{semantic_id}->{label_id}"))

    for (first_id, first_points), (second_id, second_points) in combinations(path_points.items(), 2):
        for first_start, first_end in zip(first_points, first_points[1:]):
            for second_start, second_end in zip(second_points, second_points[1:]):
                if _segments_intersect(first_start, first_end, second_start, second_end):
                    shared = set((first_start, first_end)) & set((second_start, second_end))
                    if not shared:
                        diagnostics.append(Diagnostic("Q5", "communication-path-crossing", "Communication paths cross away from node boundaries", subject=f"{first_id}<->{second_id}"))
    return diagnostics


def validate_deployment_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root = ET.parse(svg_path).getroot()
    nodes = _nodes(root, "deployment-node")
    paths = _nodes(root, "communication-path")
    selected = {item.id: item for item in model.elements if item.id in view.include}
    relations = {item.id: item for item in model.relations if item.id in view.relations}
    expected_nodes = {item.id: item for item in selected.values() if item.type == "deployment_node"}
    expected_paths = {item.id: item for item in relations.values() if item.type == "communication_path"}

    if root.attrib.get("data-diagram-id") != "DEP-01":
        diagnostics.append(Diagnostic("Q4", "diagram-id", "Rendered Deployment Diagram ID must be DEP-01"))
    title = next((node.text for node in root.iter() if node.attrib.get("id") == "diagram-title"), "")
    if title != view.title:
        diagnostics.append(Diagnostic("Q4", "title", "Rendered title does not match the ViewSpec"))
    if len(nodes) != _expected_count(view, "deploymentNodes", len(expected_nodes)):
        diagnostics.append(Diagnostic("Q4", "deployment-node-count", "Rendered deployment-node count does not match the reviewed inventory"))
    if {node.attrib.get("data-semantic-id") for node in nodes} != set(expected_nodes):
        diagnostics.append(Diagnostic("Q4", "deployment-node-inventory", "Rendered deployment-node inventory does not match selected semantic records"))
    if len(paths) != _expected_count(view, "communicationPaths", len(expected_paths)):
        diagnostics.append(Diagnostic("Q4", "communication-path-count", "Rendered communication-path count does not match the reviewed inventory"))
    if {node.attrib.get("data-semantic-id") for node in paths} != set(expected_paths):
        diagnostics.append(Diagnostic("Q4", "communication-path-inventory", "Rendered communication-path inventory does not match selected semantic records"))

    rendered_node_ids = [node.attrib.get("data-semantic-id") for node in nodes]
    rendered_path_ids = [node.attrib.get("data-semantic-id") for node in paths]
    if len(rendered_node_ids) != len(set(rendered_node_ids)) or len(rendered_path_ids) != len(set(rendered_path_ids)):
        diagnostics.append(Diagnostic("Q4", "duplicate-rendered-id", "Rendered deployment nodes and communication paths must be unique"))

    for node_id, item in expected_nodes.items():
        rendered = next((candidate for candidate in nodes if candidate.attrib.get("data-semantic-id") == node_id), None)
        if rendered is None:
            continue
        if rendered.attrib.get("data-node-name") != item.name or rendered.attrib.get("data-node-symbol") != "uml-deployment-node-3d":
            diagnostics.append(Diagnostic("Q4", "deployment-node-notation", "Deployment node name or UML deployment-node notation is incorrect", subject=node_id))
        expected_items = list(item.metadata.get("containedItems", []))
        actual_items = [candidate.attrib.get("data-item-name") for candidate in _nodes(rendered, "deployed-item")]
        if actual_items != expected_items:
            diagnostics.append(Diagnostic("Q4", "contained-item-inventory", "Contained runtime/component inventory does not match node metadata", subject=node_id))
        if not item.source_refs:
            diagnostics.append(Diagnostic("Q4", "node-source-refs", "Deployment node requires source references", subject=node_id))

    selected_node_ids = set(expected_nodes)
    for relation_id, relation in expected_paths.items():
        rendered = next((candidate for candidate in paths if candidate.attrib.get("data-semantic-id") == relation_id), None)
        if rendered is None:
            continue
        if rendered.attrib.get("data-source-id") != relation.source or rendered.attrib.get("data-target-id") != relation.target:
            diagnostics.append(Diagnostic("Q4", "communication-path-endpoints", "Rendered path endpoints do not match the semantic relation", subject=relation_id))
        if relation.source not in selected_node_ids or relation.target not in selected_node_ids:
            diagnostics.append(Diagnostic("Q4", "communication-path-hidden-endpoint", "Communication path endpoint is not a visible selected deployment node", subject=relation_id))
        if rendered.attrib.get("data-arrowheads") != "none" or rendered.attrib.get("marker-end") or rendered.attrib.get("marker-start"):
            diagnostics.append(Diagnostic("Q4", "communication-path-arrowhead", "Communication paths must be solid and unarrowed", subject=relation_id))
        if not relation.source_refs:
            diagnostics.append(Diagnostic("Q4", "communication-path-source-refs", "Communication path requires source references", subject=relation_id))

    map_id = "node.dep01.map-service"
    if any(map_id in {relation.source, relation.target} for relation in expected_paths.values()):
        diagnostics.append(Diagnostic("Q4", "map-service-has-path", "Map Service must remain intentionally unconnected"))
    if any(node.attrib.get("data-kind") in FORBIDDEN_KINDS for node in root.iter()):
        diagnostics.append(Diagnostic("Q4", "forbidden-uml-construct", "Non-Deployment UML notation is present"))
    source = svg_path.read_text(encoding="utf-8")
    for forbidden in FORBIDDEN_VISIBLE:
        if forbidden in source:
            diagnostics.append(Diagnostic("Q4", "forbidden-content", f"Forbidden visible content: {forbidden}"))
    if "marker-end" in source or "marker-start" in source:
        diagnostics.append(Diagnostic("Q4", "communication-path-arrowhead", "Communication paths must be solid and unarrowed"))
    diagnostics.extend(_geometry_diagnostics(root, nodes, paths))
    return diagnostics
