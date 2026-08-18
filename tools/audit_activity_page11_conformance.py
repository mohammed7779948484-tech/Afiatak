#!/usr/bin/env python3
"""Audit Aafiatak Activity Diagrams against the lecturer page-11 UML activity example."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "build" / "final"
VIEW_DIR = ROOT / "views" / "activity"

VIEWS = [
    "aafiatak-ad01-register-patient",
    "aafiatak-ad02-log-in",
    "aafiatak-ad03-book-appointment",
    "aafiatak-ad04-process-full-payment",
    "aafiatak-ad05-subscribe-to-availability-alert",
    "aafiatak-ad06-cancel-appointment",
    "aafiatak-ad07-publish-availability",
    "aafiatak-ad08-withdraw-remaining-capacity",
    "aafiatak-ad09-reschedule-appointment",
    "aafiatak-ad10-register-patient-check-in",
    "aafiatak-ad11-record-no-show",
    "aafiatak-ad12-handle-late-arrival",
    "aafiatak-ad13-manage-operational-exceptions",
    "aafiatak-ad14-call-next-patient",
    "aafiatak-ad15-review-facility-onboarding-request",
    "aafiatak-ad16-suspend-facility",
]

# Explicitly permitted Object Nodes/Object Flows from v3 contracts.
EXPECTED_OBJECT_FLOWS = {
    "aafiatak-ad04-process-full-payment": 2,
    "aafiatak-ad13-manage-operational-exceptions": 2,
    "aafiatak-ad15-review-facility-onboarding-request": 1,
}


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def data_kind_count(svg: str, kind: str) -> int:
    return len(re.findall(rf'data-kind="{re.escape(kind)}"', svg))


def audit_view(view_id: str) -> dict:
    errors: list[str] = []
    checks: dict[str, bool] = {}
    view_path = VIEW_DIR / f"{view_id}.yaml"
    view = load_yaml(view_path)
    model = load_yaml((view_path.parent / view["model"]).resolve())
    elements = model.get("elements", [])
    relations = model.get("relations", [])
    by_id = {element["id"]: element for element in elements}
    element_types = [element.get("type") for element in elements]
    relation_types = [relation.get("type") for relation in relations]
    svg_path = FINAL / f"{view_id}.svg"
    drawio_path = FINAL / f"{view_id}.drawio"
    png_path = FINAL / f"{view_id}.png"

    # 1. Core Activity notation used in the lecturer sample.
    checks["one_initial_node"] = element_types.count("initial") == 1
    checks["one_activity_final"] = element_types.count("final") == 1
    checks["actions_are_present"] = element_types.count("action") > 0
    checks["decisions_use_decision_or_merge_nodes"] = all(t in {"initial", "final", "action", "decision", "merge", "object", "note"} for t in element_types)
    if not checks["one_initial_node"]:
        errors.append("model must contain exactly one Initial Node")
    if not checks["one_activity_final"]:
        errors.append("model must contain exactly one Activity Final")
    if not checks["actions_are_present"]:
        errors.append("model has no Action nodes")
    if not checks["decisions_use_decision_or_merge_nodes"]:
        errors.append("model includes a non-page-11 activity node type")

    # 2. Fork/Join only when required: no v3 Aafiatak contract authorises concurrency.
    checks["no_unrequired_fork_join"] = "fork" not in element_types and "join" not in element_types
    if not checks["no_unrequired_fork_join"]:
        errors.append("contains unrequired Fork/Join notation")

    # 3. Control and Object Flow rules.
    object_flows = [relation for relation in relations if relation.get("type") == "object_flow"]
    expected_object_flows = EXPECTED_OBJECT_FLOWS.get(view_id, 0)
    checks["object_flow_count_matches_v3"] = len(object_flows) == expected_object_flows
    if not checks["object_flow_count_matches_v3"]:
        errors.append(f"Object Flow count {len(object_flows)} differs from v3 contract {expected_object_flows}")
    checks["object_flows_touch_object_node"] = all(
        "object" in {by_id.get(flow.get("source"), {}).get("type"), by_id.get(flow.get("target"), {}).get("type")}
        for flow in object_flows
    )
    if not checks["object_flows_touch_object_node"]:
        errors.append("an Object Flow does not connect to an Object Node")
    checks["only_control_and_object_flows"] = set(relation_types) <= {"control_flow", "object_flow"}
    if not checks["only_control_and_object_flows"]:
        errors.append("non-Activity-flow relation found")

    # 4. Guards appear on direct outgoing decision control flows only.
    decisions = {element["id"] for element in elements if element.get("type") == "decision"}
    guarded = [relation for relation in relations if relation.get("guard")]
    checks["guards_leave_decisions_directly"] = all(
        relation.get("type") == "control_flow" and relation.get("source") in decisions for relation in guarded
    )
    if not checks["guards_leave_decisions_directly"]:
        errors.append("a guard is not attached to a direct outgoing Decision control flow")

    # 5. SVG notation and page-11 visual grammar.
    if not svg_path.exists():
        errors.append("missing final SVG")
        svg = ""
    else:
        svg = svg_path.read_text(encoding="utf-8")
    checks["rounded_process_frame"] = svg.count('class="process-frame"') == 1
    checks["monochrome_technical_style"] = all(token not in svg.lower() for token in ["lineargradient", "radialgradient", "#0b3a", "#ffd"])
    checks["initial_symbol_rendered"] = data_kind_count(svg, "initial") == 1
    checks["activity_final_symbol_rendered"] = data_kind_count(svg, "final") == 1
    checks["actions_are_rounded_rectangles"] = data_kind_count(svg, "action") == element_types.count("action") and "action-box" in svg
    checks["decisions_are_diamonds"] = data_kind_count(svg, "decision") == element_types.count("decision") and "decision-box" in svg
    checks["merges_are_diamonds"] = data_kind_count(svg, "merge") == element_types.count("merge") and "merge-box" in svg
    checks["control_flows_have_arrowheads"] = svg.count('marker-end="url(#activity-arrow)"') >= relation_types.count("control_flow")
    checks["guard_labels_rendered"] = all(f'data-relation-id="{flow["id"]}"' in svg for flow in guarded)
    checks["object_nodes_square_when_required"] = (
        data_kind_count(svg, "object") == element_types.count("object")
        and (not object_flows or "object-box" in svg)
    )
    for check, message in [
        ("rounded_process_frame", "SVG lacks exactly one rounded Activity/Process frame"),
        ("monochrome_technical_style", "SVG uses a prohibited decorative legacy style"),
        ("initial_symbol_rendered", "SVG Initial Node count does not match model"),
        ("activity_final_symbol_rendered", "SVG Activity Final count does not match model"),
        ("actions_are_rounded_rectangles", "SVG Actions are not rendered as compact rounded rectangles"),
        ("decisions_are_diamonds", "SVG Decisions are not rendered as diamonds"),
        ("merges_are_diamonds", "SVG Merges are not rendered as diamonds"),
        ("control_flows_have_arrowheads", "SVG Control Flows lack directed arrowheads"),
        ("guard_labels_rendered", "one or more specified guards are absent from SVG"),
        ("object_nodes_square_when_required", "Object Nodes are absent or not rendered in square-cornered style"),
    ]:
        if not checks[check]:
            errors.append(message)

    # 6. Editable source and preview are present and parseable.
    checks["editable_drawio_source"] = drawio_path.exists()
    if drawio_path.exists():
        try:
            ET.parse(drawio_path)
        except ET.ParseError:
            checks["editable_drawio_source"] = False
    checks["high_resolution_preview"] = png_path.exists() and png_path.stat().st_size > 0
    if not checks["editable_drawio_source"]:
        errors.append("editable diagrams.net source is missing or malformed")
    if not checks["high_resolution_preview"]:
        errors.append("high-resolution PNG preview is missing")

    return {
        "diagram": view_id,
        "result": "pass" if not errors else "fail",
        "checks": checks,
        "counts": {
            "actions": element_types.count("action"),
            "decisions": element_types.count("decision"),
            "merges": element_types.count("merge"),
            "objects": element_types.count("object"),
            "controlFlows": relation_types.count("control_flow"),
            "objectFlows": len(object_flows),
            "guardedDecisionFlows": len(guarded),
        },
        "errors": errors,
    }


def main() -> int:
    results = [audit_view(view_id) for view_id in VIEWS]
    failed = [result for result in results if result["result"] != "pass"]
    payload = {
        "reference": "Lecturer UML handout, page 11, Process Order Activity Diagram",
        "criteria": [
            "Rounded Activity/Process frame with label inside upper-left",
            "Monochrome technical linework and compact rounded Action nodes",
            "Initial Node and Activity Final symbols",
            "Decision/Merge diamonds with guards on direct outgoing flows",
            "Directed Control Flows with arrowheads",
            "Fork/Join only for explicitly required concurrency",
            "Square-cornered Object Nodes/Object Flows only where the v3 contract requires them",
            "Editable diagrams.net source and rendered final SVG/PNG present",
        ],
        "diagramCount": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "results": results,
    }
    output = FINAL / "Aafiatak_Activity_Diagrams_AD01-AD16_Page11_UML_Conformance_Audit.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"Report: {output.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
