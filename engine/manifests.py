from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from engine import __version__
from engine.core.io import ROOT, canonical_hash, load_yaml, sha256_file, sha256_tree


def tree_hash(path: Path, pattern: str) -> str:
    files = sorted(path.rglob(pattern))
    return canonical_hash({str(item.relative_to(ROOT)): sha256_file(item) for item in files})


def design_hash() -> str:
    return tree_hash(ROOT / "design", "*.yaml")


def governance_hash() -> str:
    return tree_hash(ROOT / "governance", "*.yaml")


def compiler_hash() -> str:
    sources = {
        **{
            str(item.relative_to(ROOT)): sha256_file(item)
            for item in (ROOT / "engine").rglob("*.py")
        },
        **{str(item.relative_to(ROOT)): sha256_file(item) for item in (ROOT / "qa").rglob("*.py")},
        **{
            str(item.relative_to(ROOT)): sha256_file(item)
            for item in (ROOT / "engine" / "schemas").rglob("*.json")
        },
    }
    return canonical_hash(sources)


def _manifest_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _resolve_manifest_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def create_manifest(
    *,
    diagram_id: str,
    diagram_type: str,
    model_data: dict[str, Any],
    outputs: list[Path],
    qa: dict[str, Any],
    model_path: Path | None = None,
    view_path: Path | None = None,
    requested_targets: tuple[str, ...] = ("drawio",),
    exporter_version: str | None = None,
) -> dict[str, Any]:
    sources = {
        item["name"]: item for item in load_yaml(ROOT / "registry" / "sources.yaml")["sources"]
    }
    manifest = {
        "diagramId": diagram_id,
        "diagramType": diagram_type,
        "semanticModelHash": canonical_hash(model_data),
        "projectSpecHash": sources["aafiatak-product-specification"]["sha256"],
        "lecturerRulesHash": sources["lecturer-uml-rules"]["sha256"],
        "drawioSkillHash": sources["local-drawio-skill"]["tree_sha256"],
        "drawioSkillVersion": sources["local-drawio-skill"].get("version"),
        "drawioExporterVersion": exporter_version,
        "designSystemHash": design_hash(),
        "governanceHash": governance_hash(),
        "compilerHash": compiler_hash(),
        "rendererVersion": __version__,
        "generatedAt": datetime.now(UTC).isoformat(),
        "requestedTargets": list(requested_targets),
        "qa": qa,
        "outputs": {_manifest_path(path): sha256_file(path) for path in outputs},
    }
    if model_path:
        manifest["semanticModelPath"] = _manifest_path(model_path)
    if view_path:
        manifest["viewPath"] = _manifest_path(view_path)
        manifest["viewHash"] = canonical_hash(load_yaml(view_path))
    return manifest


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def stale_reasons(manifest: dict[str, Any]) -> list[str]:
    source_records = load_yaml(ROOT / "registry" / "sources.yaml")["sources"]
    sources = {
        item["name"]: (
            sha256_tree(ROOT / item["tree_path"])
            if item.get("tree_path")
            else sha256_file(ROOT / item["path"])
        )
        for item in source_records
    }
    reasons = []
    checks = (
        ("projectSpecHash", sources["aafiatak-product-specification"], "product specification"),
        ("lecturerRulesHash", sources["lecturer-uml-rules"], "lecturer rules"),
        ("drawioSkillHash", sources["local-drawio-skill"], "draw.io skill"),
        ("designSystemHash", design_hash(), "design system"),
        ("governanceHash", governance_hash(), "governance"),
        ("compilerHash", compiler_hash(), "compiler code"),
        ("rendererVersion", __version__, "renderer version"),
    )
    for key, current, label in checks:
        if manifest.get(key) != current:
            reasons.append(f"{label} changed")
    model_value = manifest.get("semanticModelPath")
    if model_value:
        model_path = _resolve_manifest_path(model_value)
        if not model_path.is_file():
            reasons.append("semantic model missing")
        elif manifest.get("semanticModelHash") != canonical_hash(load_yaml(model_path)):
            reasons.append("semantic model changed")
    view_value = manifest.get("viewPath")
    if view_value:
        view_path = _resolve_manifest_path(view_value)
        if not view_path.is_file():
            reasons.append("view missing")
        elif manifest.get("viewHash") != canonical_hash(load_yaml(view_path)):
            reasons.append("view changed")
    for value, expected in manifest.get("outputs", {}).items():
        output = _resolve_manifest_path(value)
        if not output.is_file():
            reasons.append(f"output missing: {value}")
        elif sha256_file(output) != expected:
            reasons.append(f"output changed: {value}")
    return reasons
