#!/usr/bin/env python3
"""Cross-suite v3 audit for Aafiatak Activity Diagrams AD-01 through AD-16."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VIEW_DIR = ROOT / "views" / "activity"
FINAL_DIR = ROOT / "build" / "final"

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

PDF_BASES = {
    "aafiatak-ad01-register-patient": "Aafiatak_AD01_Register_Patient",
    "aafiatak-ad02-log-in": "Aafiatak_AD02_Log_In",
    "aafiatak-ad03-book-appointment": "Aafiatak_AD03_Book_Appointment",
    "aafiatak-ad04-process-full-payment": "Aafiatak_AD04_Process_Full_Payment",
    "aafiatak-ad05-subscribe-to-availability-alert": "Aafiatak_AD05_Subscribe_Availability_Alert",
    "aafiatak-ad06-cancel-appointment": "Aafiatak_AD06_Cancel_Appointment",
    "aafiatak-ad07-publish-availability": "Aafiatak_AD07_Publish_Availability",
    "aafiatak-ad08-withdraw-remaining-capacity": "Aafiatak_AD08_Withdraw_Remaining_Capacity",
    "aafiatak-ad09-reschedule-appointment": "Aafiatak_AD09_Reschedule_Appointment",
    "aafiatak-ad10-register-patient-check-in": "Aafiatak_AD10_Register_Patient_Checkin",
    "aafiatak-ad11-record-no-show": "Aafiatak_AD11_Record_No_Show",
    "aafiatak-ad12-handle-late-arrival": "Aafiatak_AD12_Handle_Late_Arrival",
    "aafiatak-ad13-manage-operational-exceptions": "Aafiatak_AD13_Manage_Operational_Exceptions",
    "aafiatak-ad14-call-next-patient": "Aafiatak_AD14_Call_Next_Patient",
    "aafiatak-ad15-review-facility-onboarding-request": "Aafiatak_AD15_Review_Facility_Onboarding_Request",
    "aafiatak-ad16-suspend-facility": "Aafiatak_AD16_Suspend_Facility",
}


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_one(view_id: str) -> dict:
    errors: list[str] = []
    view_path = VIEW_DIR / f"{view_id}.yaml"
    if not view_path.exists():
        return {"id": view_id, "result": "fail", "errors": [f"missing view: {view_path}"]}

    view = load_yaml(view_path)
    model_path = (view_path.parent / view["model"]).resolve()
    model = load_yaml(model_path) if model_path.exists() else {"elements": [], "relations": []}
    if not model_path.exists():
        errors.append(f"missing model: {model_path}")
    elements, relations = model.get("elements", []), model.get("relations", [])
    element_by_id = {node.get("id"): node for node in elements}
    types = [node.get("type") for node in elements]
    relation_types = [edge.get("type") for edge in relations]
    options = view.get("options", {})

    counts = {
        "actions": types.count("action"),
        "decisions": types.count("decision"),
        "merges": types.count("merge"),
        "controlFlows": relation_types.count("control_flow"),
        "objectFlows": relation_types.count("object_flow"),
        "objectNodes": types.count("object"),
    }
    expected_counts = {
        "expectedActionCount": counts["actions"],
        "expectedDecisionCount": counts["decisions"],
        "expectedMergeCount": counts["merges"],
        "expectedControlFlowCount": counts["controlFlows"],
    }
    for key, actual in expected_counts.items():
        if options.get(key) != actual:
            errors.append(f"{key}={options.get(key)!r}, model={actual}")

    if set(view.get("include", [])) != set(element_by_id):
        errors.append("view include set does not match model element set")
    if set(view.get("relations", [])) != {edge.get("id") for edge in relations}:
        errors.append("view relation set does not match model relation set")
    if {"fork", "join", "association", "generalization", "aggregation"}.intersection(types + relation_types):
        errors.append("forbidden UML notation exists")
    for edge in relations:
        if edge.get("type") == "object_flow":
            source_kind = element_by_id.get(edge.get("source"), {}).get("type")
            target_kind = element_by_id.get(edge.get("target"), {}).get("type")
            if "object" not in {source_kind, target_kind}:
                errors.append(f"object flow {edge.get('id')} is not connected to an Object Node")
        elif edge.get("type") != "control_flow":
            errors.append(f"unsupported relation type: {edge.get('type')}")

    review = view.get("visualReview", {})
    recorded_hash = review.get("previewHash", "")
    if review.get("status") != "awaiting-user-approval":
        errors.append("visual review status is not awaiting-user-approval")
    if not re.fullmatch(r"[0-9a-f]{64}", recorded_hash or ""):
        errors.append("visual review previewHash is absent or invalid")
    if not str(options.get("v3Spec", "")).endswith("_LECTURER_PAGE11_v3.md"):
        errors.append("View does not identify its governing v3 lecturer-page-11 specification")

    work_svg = ROOT / "build" / "work" / f"{view_id}.svg"
    preview = ROOT / "build" / "preview" / f"{view_id}.png"
    if not work_svg.exists():
        errors.append(f"missing rendered SVG: {work_svg}")
    else:
        svg_text = work_svg.read_text(encoding="utf-8")
        root = ET.parse(work_svg).getroot()
        kinds = [node.attrib.get("data-kind", "") for node in root.iter()]
        if "initial" not in kinds or "final" not in kinds:
            errors.append("SVG lacks initial or final node")
        if kinds.count("control-flow") != counts["controlFlows"]:
            errors.append("SVG control-flow count disagrees with model")
        if kinds.count("object-flow") != counts["objectFlows"]:
            errors.append("SVG object-flow count disagrees with model")
        if 'class="process-frame"' not in svg_text:
            errors.append("SVG lacks lecturer-style Activity/Process frame")
        if "#0B3A" in svg_text or "#FFD" in svg_text or "gradient" in svg_text:
            errors.append("SVG contains prohibited legacy decorative theme")
        if "#111111" not in svg_text or "#F6F6F6" not in svg_text:
            errors.append("SVG does not contain expected monochrome lecturer style")
    if not preview.exists():
        errors.append(f"missing preview: {preview}")
    elif recorded_hash != sha256(preview):
        errors.append("recorded previewHash does not match current preview")

    base = PDF_BASES[view_id]
    required = [
        FINAL_DIR / f"{view_id}.svg",
        FINAL_DIR / f"{view_id}.png",
        FINAL_DIR / f"{view_id}.drawio",
        FINAL_DIR / f"{view_id}.qa.json",
        FINAL_DIR / f"{base}.pdf",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        errors.append("missing final artifacts: " + ", ".join(missing))
    return {
        "id": view_id,
        "result": "pass" if not errors else "fail",
        "counts": counts,
        "status": review.get("status"),
        "errors": errors,
    }


def main() -> int:
    results = [audit_one(view_id) for view_id in EXPECTED]
    failed = [entry for entry in results if entry["result"] != "pass"]
    payload = {
        "suite": "Aafiatak Activity Diagrams AD-01 through AD-16 — v3 Lecturer Page-11 Redesign",
        "diagramCount": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "statusExpectation": "awaiting-user-approval",
        "lecturerStyle": "rounded Activity/Process frame; monochrome technical UML notation",
        "results": results,
    }
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    suite_out = FINAL_DIR / "Aafiatak_Activity_Diagrams_AD01-AD16_Cross_Suite_Audit.json"
    suite_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for entry in results:
        (FINAL_DIR / f"{entry['id']}.semantic-audit.json").write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"Report: {suite_out.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
