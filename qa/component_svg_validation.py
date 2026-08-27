from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import hypot
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


FORBIDDEN_KINDS = {
    "actor", "lifeline", "activation", "message", "state", "transition", "action", "decision",
    "merge", "fork", "join", "class", "attribute", "operation", "deployment-node",
}
FORBIDDEN_VISIBLE = (
    "<<include>>", "<<extend>>", "Doctor Application", "Reception Application",
    "Facility Administrator Application", "Authentication Service", "Booking Service", "Queue Service",
    "Payment Service", "Notification Microservice", "API Gateway", "SMS Provider", "HIS", "EHR",
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


def _segments_intersect_rect(points: list[tuple[float, float]], rect: Rect) -> bool:
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        steps = max(2, int(max(abs(x2 - x1), abs(y2 - y1)) / 20) + 1)
        for step in range(steps + 1):
            fraction = step / steps
            x = x1 + (x2 - x1) * fraction
            y = y1 + (y2 - y1) * fraction
            if rect.x < x < rect.right and rect.y < y < rect.bottom:
                return True
    return False


def _expected_count(view: ViewSpec, key: str, fallback: int) -> int:
    counts = view.options.get("expectedCounts", {})
    return int(counts.get(key, fallback))


def _geometry_diagnostics(root, components, interfaces, connectors) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        page = _rect(root.attrib["data-page-bounds"])
    except (KeyError, ValueError):
        return [Diagnostic("Q5", "geometry-metadata-missing", "Component SVG must expose data-page-bounds")]

    component_bounds: dict[str, Rect] = {}
    for node in components:
        semantic_id = node.attrib.get("data-semantic-id", "unknown")
        try:
            bounds = _rect(node.attrib["data-bounds"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "component-geometry-missing", "Component has no parseable bounds", subject=semantic_id))
            continue
        component_bounds[semantic_id] = bounds
        if not bounds.within(page, 80):
            diagnostics.append(Diagnostic("Q5", "component-page-bounds", "Component exceeds safe page bounds", subject=semantic_id))
    for (first_id, first), (second_id, second) in combinations(component_bounds.items(), 2):
        if first.intersects(second):
            diagnostics.append(Diagnostic("Q5", "component-overlap", "Component bodies overlap", subject=f"{first_id}<->{second_id}"))

    glyph_centers: dict[str, tuple[float, float]] = {}
    label_bounds: dict[str, Rect] = {}
    interface_owners: dict[str, str] = {}
    for node in interfaces:
        semantic_id = node.attrib.get("data-semantic-id", "unknown")
        try:
            center = _point(node.attrib["data-center"])
            label = _rect(node.attrib["data-label-bounds"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "interface-geometry-missing", "Interface has incomplete geometry metadata", subject=semantic_id))
            continue
        glyph_centers[semantic_id] = center
        label_bounds[semantic_id] = label
        owner = node.attrib.get("data-owner-component", "")
        interface_owners[semantic_id] = owner
        if not label.within(page, 80):
            diagnostics.append(Diagnostic("Q5", "interface-label-page-bounds", "Interface label exceeds safe page bounds", subject=semantic_id))
        for component_id, box in component_bounds.items():
            if component_id != owner and label.intersects(box):
                diagnostics.append(Diagnostic("Q5", "interface-label-component-intersection", "Interface label intersects an unrelated component", subject=f"{semantic_id}->{component_id}"))
            if component_id != owner and box.x < center[0] < box.right and box.y < center[1] < box.bottom:
                diagnostics.append(Diagnostic("Q5", "interface-glyph-component-intersection", "Interface glyph is inside an unrelated component", subject=f"{semantic_id}->{component_id}"))
    for (first_id, first), (second_id, second) in combinations(label_bounds.items(), 2):
        if first.intersects(second):
            diagnostics.append(Diagnostic("Q5", "interface-label-overlap", "Interface labels overlap", subject=f"{first_id}<->{second_id}"))

    for node in connectors:
        semantic_id = node.attrib.get("data-semantic-id", "unknown")
        required_id = node.attrib.get("data-required-interface", "")
        provided_id = node.attrib.get("data-provided-interface", "")
        try:
            points = _points(node.attrib["data-points"])
        except (KeyError, ValueError):
            diagnostics.append(Diagnostic("Q5", "connector-geometry-missing", "Assembly connector has no parseable points", subject=semantic_id))
            continue
        if len(points) < 2:
            diagnostics.append(Diagnostic("Q5", "connector-route-short", "Assembly connector requires at least two route points", subject=semantic_id))
            continue
        for endpoint, interface_id in ((points[0], required_id), (points[-1], provided_id)):
            target = glyph_centers.get(interface_id)
            if target is not None and hypot(endpoint[0] - target[0], endpoint[1] - target[1]) > 260:
                diagnostics.append(Diagnostic("Q5", "connector-detached-interface", "Assembly connector is detached from its interface glyph", subject=f"{semantic_id}->{interface_id}"))
        owner_components = {interface_owners.get(required_id), interface_owners.get(provided_id)}
        for component_id, box in component_bounds.items():
            if component_id not in owner_components and _segments_intersect_rect(points, box):
                diagnostics.append(Diagnostic("Q5", "connector-unrelated-component-intersection", "Assembly connector crosses an unrelated component body", subject=f"{semantic_id}->{component_id}"))
    return diagnostics


def validate_component_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root = ET.parse(svg_path).getroot()
    components = _nodes(root, "component")
    provided = _nodes(root, "provided-interface")
    required = _nodes(root, "required-interface")
    interfaces = [*provided, *required]
    connectors = _nodes(root, "assembly-connector")

    selected = {item.id: item for item in model.elements if item.id in view.include}
    relations = {item.id: item for item in model.relations if item.id in view.relations}
    expected_components = {item.id: item for item in selected.values() if item.type == "component"}
    expected_provided = {item.id: item for item in selected.values() if item.type == "provided_interface"}
    expected_required = {item.id: item for item in selected.values() if item.type == "required_interface"}
    expected_realizations = {item.id: item for item in relations.values() if item.type == "realization"}
    expected_connectors = {item.id: item for item in relations.values() if item.type == "connector"}
    expected_dependencies = [item for item in relations.values() if item.type == "dependency"]

    if root.attrib.get("data-diagram-id") != "CMP-01":
        diagnostics.append(Diagnostic("Q4", "diagram-id", "Rendered Component Diagram ID must be CMP-01"))
    title = next((node.text for node in root.iter() if node.attrib.get("id") == "diagram-title"), "")
    if title != view.title:
        diagnostics.append(Diagnostic("Q4", "title", "Rendered title does not match the ViewSpec"))

    groups = (("component", components, expected_components, "components"), ("provided-interface", provided, expected_provided, "providedInterfaces"), ("required-interface", required, expected_required, "requiredInterfaces"), ("assembly-connector", connectors, expected_connectors, "assemblyConnectors"))
    for kind, rendered, expected, count_key in groups:
        if len(rendered) != _expected_count(view, count_key, len(expected)):
            diagnostics.append(Diagnostic("Q4", f"{kind}-count", f"Unexpected rendered {kind} count: {len(rendered)}"))
        rendered_ids = {node.attrib.get("data-semantic-id") for node in rendered}
        if rendered_ids != set(expected):
            diagnostics.append(Diagnostic("Q4", f"{kind}-inventory", f"Rendered {kind} inventory does not match selected semantic records"))

    if len(expected_realizations) != _expected_count(view, "providedInterfaceRealizations", len(expected_realizations)):
        diagnostics.append(Diagnostic("Q4", "realization-count", "Provided-interface realization count does not match the reviewed inventory"))
    if len(expected_dependencies) != _expected_count(view, "componentDependencies", len(expected_dependencies)):
        diagnostics.append(Diagnostic("Q4", "dependency-count", "Component dependency count does not match the reviewed inventory"))

    for interface_id, item in expected_provided.items():
        node = next((candidate for candidate in provided if candidate.attrib.get("data-semantic-id") == interface_id), None)
        owner = item.metadata.get("providerComponent")
        if node is None or node.attrib.get("data-owner-component") != owner or node.attrib.get("data-glyph") != "lollipop":
            diagnostics.append(Diagnostic("Q4", "provided-interface-ownership", "Provided interface provider or lollipop notation is incorrect", subject=interface_id))
        realization = [relation for relation in expected_realizations.values() if relation.target == interface_id]
        if len(realization) != 1 or realization[0].source != owner:
            diagnostics.append(Diagnostic("Q4", "provided-interface-realization", "Provided interface must have exactly one realization from its provider component", subject=interface_id))

    for interface_id, item in expected_required.items():
        node = next((candidate for candidate in required if candidate.attrib.get("data-semantic-id") == interface_id), None)
        owner = item.metadata.get("ownerComponent")
        matching = item.metadata.get("matchingProvidedInterface")
        if node is None or node.attrib.get("data-owner-component") != owner or node.attrib.get("data-matching-provided-interface") != matching or node.attrib.get("data-glyph") != "socket":
            diagnostics.append(Diagnostic("Q4", "required-interface-ownership", "Required interface owner, matching provider, or socket notation is incorrect", subject=interface_id))

    for relation_id, relation in expected_connectors.items():
        node = next((candidate for candidate in connectors if candidate.attrib.get("data-semantic-id") == relation_id), None)
        if node is None:
            continue
        if node.attrib.get("data-required-interface") != relation.source or node.attrib.get("data-provided-interface") != relation.target:
            diagnostics.append(Diagnostic("Q4", "assembly-connector-endpoints", "Assembly connector endpoints do not match semantic relation", subject=relation_id))
        source = selected.get(relation.source)
        target = selected.get(relation.target)
        if source is None or target is None or source.type != "required_interface" or target.type != "provided_interface":
            diagnostics.append(Diagnostic("Q4", "assembly-connector-types", "Assembly connector must run Required Interface to Provided Interface", subject=relation_id))

    map_interface = "component.cmp01.pi.map-location-interface"
    map_connectors = [relation for relation in expected_connectors.values() if map_interface in {relation.source, relation.target}]
    if map_connectors:
        diagnostics.append(Diagnostic("Q4", "map-service-consumer-invented", "Map Service interface must remain intentionally unconnected"))
    forbidden = [node for node in root.iter() if node.attrib.get("data-kind") in FORBIDDEN_KINDS]
    if forbidden:
        diagnostics.append(Diagnostic("Q4", "forbidden-uml-construct", "Non-Component UML notation is present"))
    source_text = svg_path.read_text(encoding="utf-8")
    for forbidden_text in FORBIDDEN_VISIBLE:
        if forbidden_text in source_text:
            diagnostics.append(Diagnostic("Q4", "forbidden-content", f"Forbidden visible content: {forbidden_text}"))

    diagnostics.extend(_geometry_diagnostics(root, components, interfaces, connectors))
    return diagnostics
