from __future__ import annotations

from pathlib import Path

from engine.core.io import ROOT, load_model, load_view, load_yaml, sha256_file, sha256_tree
from qa.diagnostics import Diagnostic
from qa.drawio_validation import validate_drawio
from qa.geometry import validate_geometry
from qa.semantic import validate_model, validate_view
from qa.uml import validate_uml


def validate_sources() -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for source in load_yaml(ROOT / "registry" / "sources.yaml")["sources"]:
        path = ROOT / source["path"]
        if not path.is_file():
            diagnostics.append(
                Diagnostic(
                    "Q0", "source-missing", "Immutable source is missing", subject=source["name"]
                )
            )
        elif sha256_file(path).lower() != source["sha256"].lower():
            diagnostics.append(
                Diagnostic(
                    "Q0", "source-changed", "Immutable source hash changed", subject=source["name"]
                )
            )
        tree_path = source.get("tree_path")
        if tree_path and sha256_tree(ROOT / tree_path).lower() != source["tree_sha256"].lower():
            diagnostics.append(
                Diagnostic(
                    "Q0",
                    "source-tree-changed",
                    "Immutable source tree hash changed",
                    subject=source["name"],
                )
            )
    return diagnostics


def validate_inputs(model_path: Path, view_path: Path) -> tuple[object, object, list[Diagnostic]]:
    model = load_model(model_path)
    view = load_view(view_path)
    diagnostics = validate_sources() + validate_model(model) + validate_view(model, view)
    if not any(item.severity == "error" and item.gate in {"Q0", "Q1"} for item in diagnostics):
        diagnostics += validate_uml(model, view)
    return model, view, diagnostics


def validate_artifact(path: Path) -> list[Diagnostic]:
    diagnostics = validate_drawio(path)
    if any(item.code == "malformed-xml" for item in diagnostics):
        return diagnostics
    return diagnostics + validate_geometry(str(path))
