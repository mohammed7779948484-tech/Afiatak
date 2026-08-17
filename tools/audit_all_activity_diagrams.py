#!/usr/bin/env python3
"""Cross-suite structural and delivery audit for Aafiatak AD-01 through AD-16."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
VIEW_DIR = ROOT / "views" / "activity"
FINAL_DIR = ROOT / "build" / "final"
SVG_NS = "{http://www.w3.org/2000/svg}"

EXPECTED = [
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

FINAL_BASES = {
    "aafiatak-ad01-register-patient": "Aafiatak_AD01_Register_Patient",
    "aafiatak-ad02-log-in": "Aafiatak_AD02_Log_In",
    "aafiatak-ad03-book-appointment": "Aafiatak_AD03_Book_Appointment",
    "aafiatak-ad04-process-full-payment": "Aafiatak_AD04_Process_Full_Payment",
    "aafiatak-ad05-subscribe-to-availability-alert": "Aafiatak_AD05_Subscribe_to_Availability_Alert",
    "aafiatak-ad06-cancel-appointment": "Aafiatak_AD06_Cancel_Appointment",
    "aafiatak-ad07-publish-availability": "Aafiatak_AD07_Publish_Availability",
    "aafiatak-ad08-withdraw-remaining-capacity": "Aafiatak_AD08_Withdraw_Remaining_Capacity",
    "aafiatak-ad09-reschedule-appointment": "Aafiatak_AD09_Reschedule_Appointment",
    "aafiatak-ad10-register-patient-check-in": "Aafiatak_AD10_Register_Patient_Check_In",
    "aafiatak-ad11-record-no-show": "Aafiatak_AD11_Record_No_Show",
    "aafiatak-ad12-handle-late-arrival": "Aafiatak_AD12_Handle_Late_Arrival",
    "aafiatak-ad13-manage-operational-exceptions": "Aafiatak_AD13_Manage_Operational_Exceptions",
    "aafiatak-ad14-call-next-patient": "Aafiatak_AD14_Call_Next_Patient",
    "aafiatak-ad15-review-facility-onboarding-request": "Aafiatak_AD15_Review_Facility_Onboarding_Request",
    "aafiatak-ad16-suspend-facility": "Aafiatak_AD16_Suspend_Facility",
}


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_one(view_id: str) -> dict:
    errors: list[str] = []
    view_path = VIEW_DIR / f"{view_id}.yaml"
    if not view_path.exists():
        return {"id": view_id, "result": "fail", "errors": [f"missing view: {view_path}"]}

    view = load_yaml(view_path)
    model_path = (view_path.parent / view["model"]).resolve()
    if not model_path.exists():
        errors.append(f"missing model: {model_path}")
        model = {"elements": [], "relations": []}
    else:
        model = load_yaml(model_path)

    elements = model.get("elements", [])
    relations = model.get("relations", [])
    element_types = [item.get("type") for item in elements]
    action_count = element_types.count("action")
    decision_count = element_types.count("decision")
    merge_count = element_types.count("merge")
    control_flow_count = sum(item.get("type") == "control_flow" for item in relations)

    options = view.get("options", {})
    for key, actual in [
        ("expectedActionCount", action_count),
        ("expectedDecisionCount", decision_count),
        ("expectedMergeCount", merge_count),
        ("expectedControlFlowCount", control_flow_count),
    ]:
        expected = options.get(key)
        if expected != actual:
            errors.append(f"{key}={expected!r}, model={actual}")

    if set(view.get("include", [])) != {item.get("id") for item in elements}:
        errors.append("view include set does not match model element set")
    if set(view.get("relations", [])) != {item.get("id") for item in relations}:
        errors.append("view relation set does not match model relation set")
    if any(item.get("type") != "control_flow" for item in relations):
        errors.append("non-control-flow relation found")
    forbidden_model_types = {"fork", "join", "object_flow", "association", "generalization", "aggregation"}
    if forbidden_model_types.intersection(element_types) or forbidden_model_types.intersection(item.get("type") for item in relations):
        errors.append("forbidden Activity notation found in semantic model")

    review = view.get("visualReview", {})
    if review.get("status") != "awaiting-user-approval":
        errors.append("visual review status is not awaiting-user-approval")
    preview_hash = review.get("previewHash", "")
    if len(preview_hash) != 64 or set(preview_hash) == {"0"}:
        errors.append("visual review previewHash is absent or placeholder")

    work_svg = ROOT / "build" / "work" / f"{view_id}.svg"
    if not work_svg.exists():
        errors.append(f"missing rendered SVG: {work_svg}")
    else:
        root = ET.parse(work_svg).getroot()
        kinds = [node.attrib.get("data-kind", "") for node in root.iter()]
        if "initial" not in kinds or "final" not in kinds:
            errors.append("SVG lacks initial or final node")
        if any(kind in {"fork", "join", "object-flow", "association", "generalization", "aggregation"} for kind in kinds):
            errors.append("SVG contains forbidden Activity notation")
        control_flows = kinds.count("control-flow")
        if control_flows != control_flow_count:
            errors.append(f"SVG control-flow count={control_flows}, model={control_flow_count}")

    base = FINAL_BASES[view_id]
    required = [
        FINAL_DIR / f"{base}.svg",
        FINAL_DIR / f"{base}.png",
        FINAL_DIR / f"{base}.drawio",
        FINAL_DIR / f"{base}.pdf",
        FINAL_DIR / f"{base}_QA.json",
        FINAL_DIR / f"{base}_Semantic_Audit.json",
    ]
    missing_delivery = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing_delivery:
        errors.append("missing final artifacts: " + ", ".join(missing_delivery))

    preview = ROOT / "build" / "preview" / f"{view_id}.png"
    if preview.exists() and preview_hash and set(preview_hash) != {"0"}:
        actual_hash = normalized_sha256(preview)
        if actual_hash != preview_hash:
            errors.append("recorded previewHash does not match current preview")
    else:
        errors.append(f"missing preview: {preview}")

    return {
        "id": view_id,
        "result": "pass" if not errors else "fail",
        "counts": {
            "actions": action_count,
            "decisions": decision_count,
            "merges": merge_count,
            "controlFlows": control_flow_count,
        },
        "status": review.get("status"),
        "errors": errors,
    }


def main() -> int:
    results = [audit_one(view_id) for view_id in EXPECTED]
    failures = [entry for entry in results if entry["result"] != "pass"]
    payload = {
        "suite": "Aafiatak Activity Diagrams AD-01 through AD-16",
        "diagramCount": len(results),
        "passed": len(results) - len(failures),
        "failed": len(failures),
        "statusExpectation": "awaiting-user-approval",
        "results": results,
    }
    output = ROOT / "build" / "final" / "Aafiatak_Activity_Diagrams_AD01-AD16_Cross_Suite_Audit.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"\nReport: {output.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
