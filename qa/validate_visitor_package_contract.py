from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "model/catalog/use-cases/aafiatak-visitor-package-use-case.yaml"
VIEW_PATH = ROOT / "views/use-case/aafiatak-visitor-package-use-case.yaml"

EXPECTED_ACTORS = {"Visitor", "Map Service", "WhatsApp Authentication Provider"}
EXPECTED_VISITOR_TARGETS = {f"uc.vuc-{number:02d}" for number in range(1, 7)}
EXPECTED_EXTERNAL = {
    ("actor.map-service", "uc.vuc-04"),
    ("actor.whatsapp-auth-provider", "uc.vuc-07"),
}
EXPECTED_INCLUDES = {
    ("uc.vuc-05", "uc.vuc-07"),
    ("uc.vuc-06", "uc.vuc-07"),
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
    if len(cases) != 7:
        fail(f"expected 7 use cases, found {len(cases)}")
    if {item["name"] for item in actors} != EXPECTED_ACTORS:
        fail("actor set differs from reviewed specification")
    if any(item["type"] in {"extend", "generalization"} for item in model["relations"]):
        fail("extend and generalization are forbidden")

    associations = [item for item in model["relations"] if item["type"] == "association"]
    visitor_targets = {item["target"] for item in associations if item["source"] == "actor.visitor"}
    if visitor_targets != EXPECTED_VISITOR_TARGETS:
        fail("Visitor association matrix differs from reviewed specification")
    external = {(item["source"], item["target"]) for item in associations if item["source"] != "actor.visitor"}
    if external != EXPECTED_EXTERNAL:
        fail("external association matrix differs from reviewed specification")

    includes = {(item["source"], item["target"]) for item in model["relations"] if item["type"] == "include"}
    if includes != EXPECTED_INCLUDES:
        fail("include relationship set or direction differs from reviewed specification")
    if len(associations) != 8 or len(includes) != 2:
        fail("relationship counts differ from reviewed specification")
    if set(view["include"]) != {item["id"] for item in elements}:
        fail("view does not contain every approved Visitor Package element exactly once")
    if set(view["relations"]) != {item["id"] for item in model["relations"]}:
        fail("view does not contain every approved Visitor Package relationship exactly once")
    print("PASS: 7 use cases, 3 actors, 8 associations, and 2 includes match the reviewed Visitor Package specification")


if __name__ == "__main__":
    main()
