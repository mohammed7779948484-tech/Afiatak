#!/usr/bin/env python3
"""Run deterministic semantic and geometry regression checks for CD-01 through CD-06."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.pipeline import model_path_for, render
from engine.core.io import load_model, load_view
from qa.collaboration_svg_validation import validate_collaboration_svg

VIEWS = (
    "aafiatak-cd01-patient-registration-otp",
    "aafiatak-cd02-book-appointment-full-payment",
    "aafiatak-cd03-cancel-appointment-full-refund",
    "aafiatak-cd04-reschedule-appointment",
    "aafiatak-cd05-checkin-queue-call-next",
    "aafiatak-cd06-operational-exception",
)


def verify(view_id: str, output_dir: Path) -> dict:
    view_path = ROOT / "views" / "collaboration" / f"{view_id}.yaml"
    view = load_view(view_path)
    model = load_model(model_path_for(view_path, view.model))
    svg = output_dir / f"{view_id}.svg"
    render(view_path, svg)
    diagnostics = validate_collaboration_svg(svg, model, view)
    errors = [str(item) for item in diagnostics if item.severity == "error"]
    root = ET.parse(svg).getroot()
    messages = [node for node in root.iter() if node.attrib.get("data-kind") == "message"]
    links = [node for node in root.iter() if node.attrib.get("data-kind") == "structural-link"]
    participants = [node for node in root.iter() if node.attrib.get("data-kind") == "participant"]
    loops = [node for node in messages if node.attrib.get("data-self-message") == "true"]
    loop_bounds = [node.attrib.get("data-loop-bounds") for node in loops]
    required_geometry = all(
        node.attrib.get("data-label-bounds") and (node.attrib.get("data-self-message") == "true" or node.attrib.get("data-arrow-segment"))
        for node in messages
    ) and all(node.attrib.get("data-points") for node in links) and all(node.attrib.get("data-participant-bounds") for node in participants)
    return {
        "view": view_id,
        "svg": str(svg.relative_to(ROOT)),
        "participantCount": len(participants),
        "linkCount": len(links),
        "messageCount": len(messages),
        "selfMessageSequences": [int(node.attrib["data-sequence"]) for node in loops],
        "geometryMetadataComplete": required_geometry,
        "distinctSelfLoopBounds": len(loop_bounds) == len(set(loop_bounds)),
        "layoutIssueCount": int(root.attrib.get("data-layout-issue-count", "-1")),
        "q4q5Errors": errors,
        "passed": not errors and required_geometry and len(loop_bounds) == len(set(loop_bounds)) and int(root.attrib.get("data-layout-issue-count", "-1")) == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output_dir = ROOT / "build" / "work" / "geometry-regression"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = [verify(view_id, output_dir) for view_id in VIEWS]
    report = {"results": results, "passed": all(item["passed"] for item in results)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
