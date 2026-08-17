from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml

from engine.core.io import ROOT, load_view, load_yaml, sha256_file
from engine.export import export_svg_png
from engine.manifests import create_manifest, write_manifest
from engine.svg import render_use_case_svg
from qa.pipeline import validate_inputs
from qa.svg_validation import validate_svg


def model_path_for(view_path: Path, model_value: str) -> Path:
    candidate = Path(model_value)
    return candidate if candidate.is_absolute() else (view_path.parent / candidate).resolve()


def _validated(view_path: Path):
    view = load_view(view_path)
    model_path = model_path_for(view_path, view.model)
    model, _, diagnostics = validate_inputs(model_path, view_path)
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        raise ValueError("\n".join(map(str, errors)))
    if view.diagram_type != "use_case":
        raise ValueError("the simplified renderer currently supports the Aafiatak use-case view")
    return model, view, model_path, diagnostics


def render(view_path: Path, output: Path | None = None) -> Path:
    model, view, _, _ = _validated(view_path.resolve())
    output = output or ROOT / "build" / "work" / f"{view.id}.svg"
    render_use_case_svg(model, view, output)
    errors = [item for item in validate_svg(output, model, view) if item.severity == "error"]
    if errors:
        raise ValueError("\n".join(map(str, errors)))
    return output


def _qa_data(model, view, input_diagnostics, svg: Path, preview: Path) -> tuple[dict, list[str]]:
    artifact_diagnostics = validate_svg(svg, model, view)
    diagnostics = [str(item) for item in [*input_diagnostics, *artifact_diagnostics]]
    export_svg_png(svg, preview)
    preview_hash = sha256_file(preview)
    review = view.visual_review or {}
    hash_matches = review.get("previewHash") == preview_hash
    declared = review.get("status", "generated")
    effective_status = declared if hash_matches else "awaiting-user-approval"
    q6 = {
        "status": effective_status,
        "declaredStatus": declared,
        "preview": str(preview.relative_to(ROOT)),
        "previewHash": preview_hash,
        "hashMatchesRecordedPreview": hash_matches,
        "reviewer": review.get("reviewer"),
        "reviewedAt": review.get("reviewedAt"),
        "notes": review.get("notes"),
        "hashPurpose": "Identifies the reviewed artifact; it does not prove visual quality.",
    }
    gates = {
        "Q4": "fail" if any(item.gate == "Q4" and item.severity == "error" for item in artifact_diagnostics) else "pass",
        "Q5": "fail" if any(item.gate == "Q5" and item.severity == "error" for item in artifact_diagnostics) else "pass",
        "Q6": q6,
    }
    return {
        "artifact": str(svg.relative_to(ROOT)),
        "diagnostics": diagnostics,
        "gates": gates,
        "visualReview": {"preview": q6["preview"], "previewHash": preview_hash, "status": effective_status},
    }, diagnostics


def qa(view_path: Path) -> tuple[Path, list[str]]:
    view_path = view_path.resolve()
    model, view, _, input_diagnostics = _validated(view_path)
    svg = ROOT / "build" / "work" / f"{view.id}.svg"
    render_use_case_svg(model, view, svg)
    preview = ROOT / "build" / "preview" / f"{view.id}.png"
    report_data, diagnostics = _qa_data(model, view, input_diagnostics, svg, preview)
    report = ROOT / "build" / "qa" / f"{view.id}.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(report_data, indent=2) + "\n", encoding="utf-8")
    return report, diagnostics


def _register_artifact(view_id: str, manifest_path: Path) -> None:
    path = ROOT / "registry" / "artifact-registry.yaml"
    registry = load_yaml(path)
    registry["artifacts"] = [
        item for item in registry.get("artifacts", []) if item.get("diagramId") != view_id
    ]
    registry["artifacts"].append(
        {"diagramId": view_id, "manifest": str(manifest_path.relative_to(ROOT))}
    )
    path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")


def build(view_path: Path) -> list[Path]:
    view_path = view_path.resolve()
    model, view, model_path, input_diagnostics = _validated(view_path)
    if view.approval != "approved":
        raise ValueError("the semantic view must be approved before building")
    if model.test_data:
        raise ValueError("release forbids models marked testData")
    if set(view.output_targets) != {"svg", "png"}:
        raise ValueError("the simplified Main Use Case build produces exactly SVG and PNG")

    work_svg = ROOT / "build" / "work" / f"{view.id}.svg"
    render_use_case_svg(model, view, work_svg)
    work_png = ROOT / "build" / "work" / f"{view.id}.png"
    report_data, diagnostics = _qa_data(model, view, input_diagnostics, work_svg, work_png)
    if report_data["gates"]["Q4"] == "fail" or report_data["gates"]["Q5"] == "fail":
        raise ValueError("structural QA contains blocking errors")
    final = ROOT / "build" / "final"
    final.mkdir(parents=True, exist_ok=True)
    final_svg = final / f"{view.id}.svg"
    final_png = final / f"{view.id}.png"
    for source, destination in ((work_svg, final_svg), (work_png, final_png)):
        temporary = destination.with_name(f"{destination.stem}.tmp{destination.suffix}")
        shutil.copy2(source, temporary)
        temporary.replace(destination)
    report_data["artifact"] = str(final_svg.relative_to(ROOT))
    report_data["gates"]["Q6"]["preview"] = str(final_png.relative_to(ROOT))
    report_data["visualReview"]["preview"] = str(final_png.relative_to(ROOT))
    report = ROOT / "build" / "qa" / f"{view.id}.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(report_data, indent=2) + "\n", encoding="utf-8")

    visual_status = report_data["gates"]["Q6"]["status"]
    manifest = create_manifest(
        diagram_id=view.id,
        diagram_type=view.diagram_type,
        model_data=load_yaml(model_path),
        outputs=[final_svg, final_png],
        qa={
            "result": "pass" if report_data["gates"]["Q4"] == report_data["gates"]["Q5"] == "pass" else "fail",
            "report": str(report.relative_to(ROOT)),
            "gates": report_data["gates"],
            "Q7": "approved" if visual_status == "approved" else "awaiting-user-approval",
        },
        model_path=model_path,
        view_path=view_path,
        requested_targets=view.output_targets,
    )
    manifest_path = final / f"{view.id}.manifest.json"
    write_manifest(manifest_path, manifest)
    _register_artifact(view.id, manifest_path)
    return [final_svg, final_png, manifest_path]
