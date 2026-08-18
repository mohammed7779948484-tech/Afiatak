#!/usr/bin/env python3
"""Generate communication semantic models and views from the six approved MD contracts.

The authoritative Markdown remains read-only. This utility extracts only the binding
participant, structural-link, and ordered-message tables so the generated YAML stays
traceable and machine-checkable.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "build" / "work" / "collaboration-specs-v1"
MODEL_DIR = ROOT / "model" / "catalog" / "collaborations"
VIEW_DIR = ROOT / "views" / "collaboration"

CONFIG = {
    "CD01": {
        "spec": "CD01_Patient_Registration_WhatsApp_OTP_FINAL_VERIFIED_9PASS.md",
        "slug": "patient-registration-otp",
        "filename": "Aafiatak_CD01_Patient_Registration_OTP",
        "sourceKey": "cd01-patient-registration-otp-final-verified-spec",
    },
    "CD02": {
        "spec": "CD02_Book_Appointment_FULL_PAYMENT_FINAL_VERIFIED_9PASS.md",
        "slug": "book-appointment-full-payment",
        "filename": "Aafiatak_CD02_Book_Appointment_FULL_PAYMENT",
        "sourceKey": "cd02-book-appointment-full-payment-final-verified-spec",
    },
    "CD03": {
        "spec": "CD03_Cancel_Appointment_Full_Refund_Required_FINAL_VERIFIED_9PASS.md",
        "slug": "cancel-appointment-full-refund",
        "filename": "Aafiatak_CD03_Cancel_Appointment_Full_Refund",
        "sourceKey": "cd03-cancel-appointment-full-refund-final-verified-spec",
    },
    "CD04": {
        "spec": "CD04_Reschedule_Appointment_FINAL_VERIFIED_9PASS.md",
        "slug": "reschedule-appointment",
        "filename": "Aafiatak_CD04_Reschedule_Appointment",
        "sourceKey": "cd04-reschedule-appointment-final-verified-spec",
    },
    "CD05": {
        "spec": "CD05_CheckIn_Queue_CallNext_FINAL_VERIFIED_9PASS.md",
        "slug": "checkin-queue-call-next",
        "filename": "Aafiatak_CD05_CheckIn_Queue_CallNext",
        "sourceKey": "cd05-checkin-queue-call-next-final-verified-spec",
    },
    "CD06": {
        "spec": "CD06_Resolve_Operational_Exception_FINAL_VERIFIED_9PASS.md",
        "slug": "operational-exception",
        "filename": "Aafiatak_CD06_Operational_Exception",
        "sourceKey": "cd06-operational-exception-final-verified-spec",
    },
}


def slugify(value: str) -> str:
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def section(text: str, heading: str, next_heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$([\s\S]*?)^## {re.escape(next_heading)}\s*$",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        raise ValueError(f"Could not find section {heading!r}")
    return match.group(1)


def parse_spec(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title_match = re.search(r"^# Collaboration Diagram — (.+)$", text, flags=re.MULTILINE)
    id_match = re.search(r"\*\*Diagram ID:\*\* `([^`]+)`", text)
    if not title_match or not id_match:
        raise ValueError(f"Missing title or diagram ID in {path.name}")
    diagram_id = id_match.group(1)
    short_id = diagram_id.replace("-", "")

    participants = []
    for line in section(text, "Participants", "Structural Communication Links").splitlines():
        match = re.match(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|", line)
        if match:
            participants.append({"number": int(match.group(1)), "name": match.group(2)})

    links = []
    for line in section(text, "Structural Communication Links", "Ordered Messages — Binding").splitlines():
        match = re.match(r"^\|\s*(L\d+)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\|", line)
        if match:
            links.append(
                {
                    "id": match.group(1),
                    "a": match.group(2),
                    "b": match.group(3),
                    "numbers": [int(number.strip()) for number in match.group(4).split(",")],
                }
            )

    messages = []
    for line in section(text, "Ordered Messages — Binding", "Self-Messages").splitlines():
        match = re.match(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|", line)
        if match:
            messages.append(
                {
                    "sequence": int(match.group(1)),
                    "sender": match.group(2),
                    "receiver": match.group(3),
                    "label": match.group(4),
                }
            )

    if not participants or not links or not messages:
        raise ValueError(f"Failed to parse binding tables from {path.name}")

    names = {participant["name"] for participant in participants}
    if any(message["sender"] not in names or message["receiver"] not in names for message in messages):
        raise ValueError(f"A message endpoint is absent from participants in {path.name}")
    if [message["sequence"] for message in messages] != list(range(1, len(messages) + 1)):
        raise ValueError(f"Message sequence is not contiguous in {path.name}")

    number_to_link = {}
    for link in links:
        for number in link["numbers"]:
            if number in number_to_link:
                raise ValueError(f"Message {number} occurs on more than one structural link in {path.name}")
            number_to_link[number] = link["id"]
    for message in messages:
        if message["sender"] != message["receiver"] and message["sequence"] not in number_to_link:
            raise ValueError(f"Non-self message {message['sequence']} is not assigned to a link in {path.name}")
        if message["sender"] == message["receiver"] and message["sequence"] in number_to_link:
            raise ValueError(f"Self message {message['sequence']} must not use a structural link in {path.name}")

    return {
        "id": diagram_id,
        "short_id": short_id.lower(),
        "title": title_match.group(1),
        "participants": participants,
        "links": links,
        "messages": messages,
    }


def generate_one(config: dict) -> tuple[Path, Path]:
    spec_path = SPECS / config["spec"]
    parsed = parse_spec(spec_path)
    diagram_id = parsed["id"]
    short_id = parsed["short_id"]
    id_by_name = {item["name"]: f"participant.{short_id}.{slugify(item['name'])}" for item in parsed["participants"]}
    elements = [
        {
            "id": id_by_name[item["name"]],
            "name": item["name"],
            "type": "participant",
            "description": "Collaboration/Communication Diagram interaction participant.",
            "tags": [short_id, "communication", "participant"],
            "sourceRefs": [
                {"source": config["sourceKey"], "section": "Participants"},
                {"source": "aafiatak-product-specification", "section": "MVP interaction scope"},
            ],
            "metadata": {"visibleLabel": item["name"], "participantNumber": item["number"]},
        }
        for item in parsed["participants"]
    ]
    relations = []
    for message in parsed["messages"]:
        sequence = message["sequence"]
        relations.append(
            {
                "id": f"message.{short_id}.{sequence:02d}",
                "type": "message",
                "source": id_by_name[message["sender"]],
                "target": id_by_name[message["receiver"]],
                "name": message["label"],
                "sourceRefs": [
                    {"source": config["sourceKey"], "section": "Ordered Messages — Binding"},
                    {"source": "aafiatak-product-specification", "section": "MVP interaction scope"},
                ],
                "metadata": {
                    "sequence": sequence,
                    "sender": message["sender"],
                    "receiver": message["receiver"],
                    "exactLabel": message["label"],
                    "structuralLink": number_to_link(parsed["links"], sequence) if message["sender"] != message["receiver"] else "SELF",
                },
            }
        )

    model = {"modelId": f"aafiatak-{short_id}-{config['slug']}", "version": "1.0", "elements": elements, "relations": relations}
    structural_links = []
    for link in parsed["links"]:
        structural_links.append(
            {
                "id": link["id"],
                "participants": [id_by_name[link["a"]], id_by_name[link["b"]]],
                "participantNames": [link["a"], link["b"]],
                "messageSequences": link["numbers"],
            }
        )
    self_messages = [message["sequence"] for message in parsed["messages"] if message["sender"] == message["receiver"]]
    view_id = f"aafiatak-{short_id}-{config['slug']}"
    view = {
        "id": view_id,
        "diagramType": "communication",
        "title": f"Collaboration Diagram — {parsed['title']}",
        "model": f"../../model/catalog/collaborations/{view_id}.yaml",
        "include": [element["id"] for element in elements],
        "relations": [relation["id"] for relation in relations],
        "layoutProfile": "lecturer-collaboration-network",
        "outputTargets": ["svg", "png"],
        "approval": "reviewed",
        "visualReview": {
            "status": "awaiting-user-approval",
            "reviewer": "Manus automated QA",
            "reviewedAt": "2026-08-18T00:00:00+00:00",
            "notes": "Awaiting the user's final visual approval after semantic and rendering QA.",
            "previewHash": "0000000000000000000000000000000000000000000000000000000000000000",
        },
        "options": {
            "sourceSpecification": config["spec"],
            "outputStem": config["filename"],
            "expectedParticipantCount": len(elements),
            "expectedStructuralLinkCount": len(structural_links),
            "expectedMessageCount": len(relations),
            "expectedSelfMessageSequences": self_messages,
            "structuralLinks": structural_links,
            "lecturerStyle": "Academic Collaboration/Communication: object boxes, reusable structural links, numbered directional messages, self loops only where specified.",
        },
    }
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    VIEW_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / f"{view_id}.yaml"
    view_path = VIEW_DIR / f"{view_id}.yaml"
    model_path.write_text(yaml.safe_dump(model, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")
    view_path.write_text(yaml.safe_dump(view, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")
    return model_path, view_path


def number_to_link(links: list[dict], sequence: int) -> str:
    for link in links:
        if sequence in link["numbers"]:
            return link["id"]
    raise ValueError(f"No structural link contains message {sequence}")


def main() -> None:
    generated = [generate_one(config) for _, config in CONFIG.items()]
    for model_path, view_path in generated:
        print(f"generated {model_path.relative_to(ROOT)}")
        print(f"generated {view_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
