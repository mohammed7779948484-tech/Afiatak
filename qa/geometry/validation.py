from __future__ import annotations

import importlib.util
import re
from copy import deepcopy
from xml.etree import ElementTree as ET

from engine.core.io import ROOT, load_yaml
from qa.diagnostics import Diagnostic


def _routing_warnings(root, clearance: float) -> list[str]:
    validator = ROOT / ".agents" / "skills" / "drawio" / "scripts" / "validate.py"
    spec = importlib.util.spec_from_file_location("vendored_drawio_validate", validator)
    if spec is None or spec.loader is None:
        return ["vendored route validator could not be loaded"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expanded = deepcopy(root)
    for geometry in expanded.findall(".//mxCell[@vertex='1']/mxGeometry"):
        if geometry.get("relative") == "1" or geometry.get("width") is None:
            continue
        geometry.set("x", str(float(geometry.get("x", 0)) - clearance))
        geometry.set("y", str(float(geometry.get("y", 0)) - clearance))
        geometry.set("width", str(float(geometry.get("width", 0)) + 2 * clearance))
        geometry.set("height", str(float(geometry.get("height", 0)) + 2 * clearance))
    warnings: list[str] = []
    for diagram in expanded.findall("diagram"):
        _, page_warnings = module.check_page(diagram)
        warnings.extend(page_warnings)
    edges = {
        item.get("id"): {item.get("source"), item.get("target")}
        for item in root.findall(".//mxCell[@edge='1']")
    }
    filtered = []
    pattern = re.compile(r"edge '([^']+)' routes through vertex '([^']+)'")
    for warning in warnings:
        match = pattern.search(warning)
        if match and any(
            match.group(2).startswith(f"{endpoint}-")
            for endpoint in edges.get(match.group(1), set())
            if endpoint
        ):
            continue
        filtered.append(warning)
    return filtered


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
                        "Q5", "node-gap", f"Nodes too close: {first['id']} and {second['id']}"
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
    route_warnings = _routing_warnings(root, connector_clearance)
    crossings = sum(" cross" in item for item in route_warnings)
    through = [item for item in route_warnings if "routes through" in item]
    if crossings > maximum_crossings:
        diagnostics.append(
            Diagnostic(
                "Q5",
                "edge-crossings",
                f"Edge crossings {crossings} exceed maximum {maximum_crossings}",
            )
        )
    for warning in through:
        diagnostics.append(
            Diagnostic(
                "Q5",
                "connector-clearance",
                f"Connector violates {connector_clearance:g}px node clearance: {warning}",
            )
        )
    return diagnostics
