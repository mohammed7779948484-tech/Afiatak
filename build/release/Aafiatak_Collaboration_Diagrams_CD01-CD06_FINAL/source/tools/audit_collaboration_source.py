#!/usr/bin/env python3
"""Machine-audit a generated Collaboration model/view against its binding Markdown contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engine.core.io import load_yaml
from tools.generate_collaboration_models import CONFIG, parse_spec

ROOT = Path(__file__).resolve().parents[1]


def audit(key: str) -> dict:
    config = CONFIG[key]
    parsed = parse_spec(ROOT / "build" / "work" / "collaboration-specs-v1" / config["spec"])
    short_id = parsed["short_id"]
    view_id = f"aafiatak-{short_id}-{config['slug']}"
    model_path = ROOT / "model" / "catalog" / "collaborations" / f"{view_id}.yaml"
    view_path = ROOT / "views" / "collaboration" / f"{view_id}.yaml"
    model = load_yaml(model_path)
    view = load_yaml(view_path)
    participants = model["elements"]
    messages = model["relations"]
    by_id = {item["id"]: item for item in participants}
    actual_participant_names = [item["name"] for item in participants]
    expected_participant_names = [item["name"] for item in parsed["participants"]]
    expected_links = [{"id": item["id"], "participantNames": [item["a"], item["b"]], "messageSequences": item["numbers"]} for item in parsed["links"]]
    actual_links = [{"id": item["id"], "participantNames": item["participantNames"], "messageSequences": item["messageSequences"]} for item in view["options"]["structuralLinks"]]
    message_matches = []
    for expected, actual in zip(parsed["messages"], messages, strict=False):
        message_matches.append(
            actual.get("metadata", {}).get("sequence") == expected["sequence"]
            and actual.get("name") == expected["label"]
            and by_id.get(actual.get("source"), {}).get("name") == expected["sender"]
            and by_id.get(actual.get("target"), {}).get("name") == expected["receiver"]
        )
    expected_self = [item["sequence"] for item in parsed["messages"] if item["sender"] == item["receiver"]]
    actual_self = [item["metadata"]["sequence"] for item in messages if item["source"] == item["target"]]
    results = {
        "spec": config["spec"],
        "view": str(view_path.relative_to(ROOT)),
        "model": str(model_path.relative_to(ROOT)),
        "diagramType": view.get("diagramType") == "communication",
        "participants": actual_participant_names == expected_participant_names,
        "participantCount": len(participants) == len(parsed["participants"]),
        "structuralLinks": actual_links == expected_links,
        "messageCount": len(messages) == len(parsed["messages"]),
        "messageNumbering": [message["metadata"].get("sequence") for message in messages] == list(range(1, len(parsed["messages"]) + 1)),
        "messageSourceMatch": all(message_matches) and len(message_matches) == len(parsed["messages"]),
        "selfMessages": sorted(actual_self) == sorted(expected_self),
        "status": view.get("visualReview", {}).get("status") == "awaiting-user-approval",
    }
    results["passed"] = all(results[key] for key in ("diagramType", "participants", "participantCount", "structuralLinks", "messageCount", "messageNumbering", "messageSourceMatch", "selfMessages", "status"))
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("key", choices=CONFIG)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.key)
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
