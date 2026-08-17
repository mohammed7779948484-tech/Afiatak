from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "model/catalog/use-cases/aafiatak-patient-package-use-case.yaml"
VIEW_PATH = ROOT / "views/use-case/aafiatak-patient-package-use-case.yaml"

EXPECTED_ACTORS = {
    "Patient",
    "WhatsApp Authentication Provider",
    "Map Service",
    "Payment Gateway",
    "Notification Service",
}
EXPECTED_PATIENT_TARGETS = {
    f"uc.puc-{number:02d}"
    for number in (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29)
}
EXPECTED_EXTERNAL = {
    ("actor.whatsapp-auth-provider", "uc.puc-02"),
    ("actor.map-service", "uc.puc-08"),
    ("actor.payment-gateway", "uc.puc-21"),
    ("actor.payment-gateway", "uc.puc-22"),
    ("actor.notification-service", "uc.puc-28"),
    ("actor.notification-service", "uc.puc-29"),
}
EXPECTED_INCLUDES = {
    ("uc.puc-01", "uc.puc-02"),
    ("uc.puc-11", "uc.puc-12"),
    ("uc.puc-11", "uc.puc-13"),
    ("uc.puc-21", "uc.puc-22"),
}
EXPECTED_EXTENDS = {
    ("uc.puc-21", "uc.puc-11", "[Booking policy = FULL_PAYMENT_REQUIRED]"),
    ("uc.puc-15", "uc.puc-12", "[No bookable capacity available]"),
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    model = yaml.safe_load(MODEL_PATH.read_text(encoding="utf-8"))
    view = yaml.safe_load(VIEW_PATH.read_text(encoding="utf-8"))
    elements = model["elements"]
    actors = [item for item in elements if item["type"] == "actor"]
    cases = [item for item in elements if item["type"] == "use_case"]
    if len(cases) != 29:
        fail(f"expected 29 use cases, found {len(cases)}")
    if {item["name"] for item in actors} != EXPECTED_ACTORS:
        fail("actor set differs from reviewed specification")
    if any(item["type"] == "generalization" for item in model["relations"]):
        fail("generalization is forbidden")

    associations = [item for item in model["relations"] if item["type"] == "association"]
    patient_targets = {item["target"] for item in associations if item["source"] == "actor.patient"}
    if patient_targets != EXPECTED_PATIENT_TARGETS:
        fail("Patient association matrix differs from reviewed specification")
    external = {(item["source"], item["target"]) for item in associations if item["source"] != "actor.patient"}
    if external != EXPECTED_EXTERNAL:
        fail("external association matrix differs from reviewed specification")

    includes = {(item["source"], item["target"]) for item in model["relations"] if item["type"] == "include"}
    if includes != EXPECTED_INCLUDES:
        fail("include relationship set or direction differs from reviewed specification")
    extends = {(item["source"], item["target"], item.get("metadata", {}).get("condition")) for item in model["relations"] if item["type"] == "extend"}
    if extends != EXPECTED_EXTENDS:
        fail("extend relationship set, direction, or condition differs from reviewed specification")

    selected = set(view["include"])
    if selected != {item["id"] for item in elements}:
        fail("view does not contain every approved Patient Package element exactly once")
    if set(view["relations"]) != {item["id"] for item in model["relations"]}:
        fail("view does not contain every approved Patient Package relationship exactly once")
    print("PASS: 29 use cases, 5 actors, 31 associations, 4 includes, and 2 extends match the reviewed Patient Package specification")


if __name__ == "__main__":
    main()
