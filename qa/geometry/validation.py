from __future__ import annotations

from xml.etree import ElementTree as ET

from engine.core.io import ROOT, load_yaml
from qa.diagnostics import Diagnostic
from qa.visual import analyze_visual_metrics


def _gap(a, b) -> tuple[float, float]:
    horizontal = max(0.0, max(a[0], b[0]) - min(a[0] + a[2], b[0] + b[2]))
    vertical = max(0.0, max(a[1], b[1]) - min(a[1] + a[3], b[1] + b[3]))
    return horizontal, vertical


def validate_geometry(path: str) -> list[Diagnostic]:
    root = ET.parse(path).getroot()
    quality = load_yaml(ROOT / "design" / "geometry.yaml")["quality"]
    minimum_gap = float(quality["minimum_node_gap"])
    actor_gap = float(quality["minimum_actor_boundary_gap"])
    page_margin = float(quality["minimum_page_margin"])
    occupancy = quality["occupancy_target"]
    maximum_crossings = int(quality["maximum_edge_crossings"])
    connector_clearance = float(quality["minimum_connector_clearance"])
    model = root.find(".//mxGraphModel")
    page_width = float(model.get("pageWidth", 0)) if model is not None else 0
    page_height = float(model.get("pageHeight", 0)) if model is not None else 0
    diagnostics: list[Diagnostic] = []
    boxes: list[dict] = []
    for wrapper in root.findall(".//object"):
        cell = wrapper.find("mxCell")
        geometry = cell.find("mxGeometry") if cell is not None else None
        if cell is None or geometry is None or cell.get("vertex") != "1":
            continue
        rect = (
            float(geometry.get("x", 0)),
            float(geometry.get("y", 0)),
            float(geometry.get("width", 0)),
            float(geometry.get("height", 0)),
        )
        item = {
            "id": wrapper.get("id", "?"),
            "rect": rect,
            "parent": cell.get("parent", ""),
            "semantic": wrapper.get("semanticId"),
            "type": wrapper.get("semanticType"),
            "collision_candidate": not any(
                wrapper.get(key) is not None
                for key in ("compartment", "deployedOn", "activationFor")
            ),
        }
        boxes.append(item)
        x, y, width, height = rect
        if width <= 0 or height <= 0:
            diagnostics.append(
                Diagnostic(
                    "Q5", "nonpositive-size", "Node size must be positive", subject=item["id"]
                )
            )
        if item["parent"].startswith("layer-"):
            if x < page_margin or y < page_margin:
                diagnostics.append(
                    Diagnostic(
                        "Q5",
                        "page-margin",
                        "Top-level node violates minimum page margin",
                        severity="warning",
                        subject=item["id"],
                    )
                )
            if (
                page_width
                and page_height
                and (x + width > page_width - page_margin or y + height > page_height - page_margin)
            ):
                diagnostics.append(
                    Diagnostic(
                        "Q5",
                        "page-bounds",
                        "Top-level node exceeds usable page bounds",
                        subject=item["id"],
                    )
                )
    semantic_boxes = [item for item in boxes if item["collision_candidate"]]
    for index, first in enumerate(semantic_boxes):
        for second in semantic_boxes[index + 1 :]:
            if first["parent"] != second["parent"]:
                continue
            horizontal, vertical = _gap(first["rect"], second["rect"])
            if horizontal == 0 and vertical == 0:
                diagnostics.append(
                    Diagnostic("Q5", "overlap", f"Nodes overlap: {first['id']} and {second['id']}")
                )
            elif (horizontal == 0 and vertical < minimum_gap) or (
                vertical == 0 and horizontal < minimum_gap
            ):
                diagnostics.append(
                    Diagnostic(
                        "Q5",
                        "node-gap",
                        f"Nodes too close: {first['id']} and {second['id']}",
                        severity="warning",
                    )
                )
    boundary = next((item for item in boxes if item["id"] == "system-boundary"), None)
    if boundary:
        for actor in (item for item in boxes if item["type"] == "actor"):
            horizontal, vertical = _gap(boundary["rect"], actor["rect"])
            if max(horizontal, vertical) < actor_gap:
                diagnostics.append(
                    Diagnostic(
                        "Q5",
                        "actor-boundary-gap",
                        "Actor is too close to the system boundary",
                        severity="warning",
                        subject=actor["id"],
                    )
                )
    top = [item["rect"] for item in boxes if item["parent"].startswith("layer-")]
    if top and page_width and page_height:
        min_x, min_y = min(item[0] for item in top), min(item[1] for item in top)
        max_x = max(item[0] + item[2] for item in top)
        max_y = max(item[1] + item[3] for item in top)
        ratio = ((max_x - min_x) * (max_y - min_y)) / (page_width * page_height)
        if ratio < float(occupancy["min"]) or ratio > float(occupancy["max"]):
            diagnostics.append(
                Diagnostic(
                    "Q5",
                    "canvas-occupancy",
                    f"Canvas occupancy {ratio:.2f} is outside target",
                    severity="warning",
                )
            )
    metrics = analyze_visual_metrics(path)
    crossings = metrics["routing"]["crossings"]
    route_through = metrics["routing"]["routeThroughNodes"]
    clearance_violations = metrics["routing"]["clearanceViolations"]
    if crossings > maximum_crossings:
        diagnostics.append(
            Diagnostic(
                "Q5",
                "edge-crossings",
                f"Edge crossings {crossings} exceed maximum {maximum_crossings}",
                severity="warning",
            )
        )
    for violation in route_through:
        diagnostics.append(
            Diagnostic(
                "Q5",
                "connector-through-node",
                "Connector routes through an unrelated node",
                subject=f"{violation['edge']} -> {violation['node']}",
            )
        )
    route_through_pairs = {(item["edge"], item["node"]) for item in route_through}
    for violation in clearance_violations:
        if (violation["edge"], violation["node"]) in route_through_pairs:
            continue
        diagnostics.append(
            Diagnostic(
                "Q5",
                "connector-clearance",
                f"Connector violates {connector_clearance:g}px node clearance",
                severity="warning",
                subject=f"{violation['edge']} -> {violation['node']}",
            )
        )
    routing = metrics["routing"]
    edge_length = routing["edgeLength"]
    bends = routing["bends"]
    warning_checks = (
        (
            edge_length["average"] > float(quality["maximum_average_edge_length"]),
            "average-edge-length",
            f"Average edge length {edge_length['average']:.1f}px exceeds the visual target",
        ),
        (
            edge_length["maximum"] > float(quality["maximum_edge_length"]),
            "maximum-edge-length",
            f"Maximum edge length {edge_length['maximum']:.1f}px exceeds the visual target",
        ),
        (
            bends["averagePerEdge"] > float(quality["maximum_average_bends"]),
            "average-edge-bends",
            f"Average bends per routed edge {bends['averagePerEdge']:.2f} exceeds the visual target",
        ),
        (
            bends["maximumPerEdge"] > int(quality["maximum_bends_per_edge"]),
            "maximum-edge-bends",
            f"Maximum bends on one edge {bends['maximumPerEdge']} exceeds the visual target",
        ),
    )
    for failed, code, message in warning_checks:
        if failed:
            diagnostics.append(Diagnostic("Q5", code, message, severity="warning"))
    internal_occupancy = metrics["occupancy"]["internalNodeAreaRatio"]
    internal_target = quality["internal_occupancy_target"]
    if internal_occupancy is not None and not (
        float(internal_target["min"]) <= internal_occupancy <= float(internal_target["max"])
    ):
        diagnostics.append(
            Diagnostic(
                "Q5",
                "internal-occupancy",
                f"Internal boundary occupancy {internal_occupancy:.2f} is outside target",
                severity="warning",
            )
        )
    imbalance = metrics["zoneBalance"]["imbalance"]
    if imbalance is not None and imbalance > float(quality["maximum_zone_imbalance"]):
        diagnostics.append(
            Diagnostic(
                "Q5",
                "zone-imbalance",
                f"Zone occupancy imbalance {imbalance:.2f} exceeds the visual target",
                severity="warning",
            )
        )
    actor_average = metrics["actorAssociationProximity"]["averageRouteLength"]
    if actor_average is not None and actor_average > float(
        quality["maximum_actor_association_average_length"]
    ):
        diagnostics.append(
            Diagnostic(
                "Q5",
                "actor-association-distance",
                f"Average actor association length {actor_average:.1f}px exceeds the visual target",
                severity="warning",
            )
        )
    for warning in metrics["labelAndSizeWarnings"]:
        diagnostics.append(
            Diagnostic(
                "Q5",
                warning["code"],
                warning["message"],
                severity="warning",
                subject=warning.get("subject"),
            )
        )
    if metrics["congestion"]["maximumSegmentsPerCell"] > int(
        quality["maximum_corridor_segments"]
    ):
        diagnostics.append(
            Diagnostic(
                "Q5",
                "routing-congestion",
                f"Maximum corridor density is {metrics['congestion']['maximumSegmentsPerCell']} segments",
                severity="warning",
            )
        )
    return diagnostics
