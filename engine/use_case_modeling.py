from __future__ import annotations

from pathlib import Path

from engine.core.io import ROOT, load_yaml, validate_schema
from qa.pipeline import validate_sources


def render_markdown(source: Path, output: Path) -> Path:
    data = load_yaml(source)
    errors = validate_schema(data, "use-case-model.schema.json")
    if errors:
        raise ValueError("\n".join(errors))
    source_errors = validate_sources()
    if source_errors:
        raise ValueError("\n".join(map(str, source_errors)))
    registered = {item["name"] for item in load_yaml(ROOT / "registry" / "sources.yaml")["sources"]}
    fixture_root = (ROOT / "tests" / "fixtures").resolve()
    is_fixture = fixture_root in source.resolve().parents
    for ref in data["sourceRefs"]:
        synthetic = is_fixture and ref["source"].startswith("synthetic-")
        if ref["source"] not in registered and not synthetic:
            raise ValueError(f"unknown source reference: {ref['source']}")
    if not is_fixture and not any(
        ref["source"] == "aafiatak-product-specification" for ref in data["sourceRefs"]
    ):
        raise ValueError("production use-case models require product-spec provenance")
    steps = [item["step"] for item in data["mainFlow"]]
    if steps != list(range(1, len(steps) + 1)):
        raise ValueError("mainFlow steps must be unique and sequential from 1")
    lines = [f"# {data['name']}", "", f"**ID:** `{data['id']}`", "", data["briefDescription"], ""]
    lines.extend(["## Actors", "", f"- Primary: `{data['primaryActor']}`"])
    lines.extend(f"- Secondary: `{item}`" for item in data.get("secondaryActors", []))
    for title, key in (("Preconditions", "preconditions"), ("Postconditions", "postconditions")):
        lines.extend(["", f"## {title}", ""])
        lines.extend(f"- {item}" for item in data[key])
    lines.extend(["", "## Main Flow", "", "| Step | Actor | Action |", "| ---: | --- | --- |"])
    lines.extend(
        f"| {item['step']} | {item['actor']} | {item['action']} |" for item in data["mainFlow"]
    )
    lines.extend(["", "## Alternate Flows", ""])
    for item in data["alternateFlows"]:
        lines.extend(
            [
                f"### {item['name']}",
                "",
                f"**Condition:** {item['condition']}",
                "",
                *(f"{index}. {step}" for index, step in enumerate(item["steps"], 1)),
                "",
                f"**Outcome:** {item['outcome']}",
                "",
            ]
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
