from __future__ import annotations

import json
import shutil
import struct
from pathlib import Path

import yaml

from engine.core.io import ROOT, load_view, load_yaml, sha256_file
from engine.export import export_drawio, find_drawio
from engine.manifests import create_manifest, write_manifest
from engine.renderers import get_renderer
from qa.pipeline import validate_artifact, validate_inputs
from qa.visual import analyze_visual_metrics


def model_path_for(view_path: Path, model_value: str) -> Path:
    candidate = Path(model_value)
    return candidate if candidate.is_absolute() else (view_path.parent / candidate).resolve()


def render(view_path: Path, output: Path | None = None) -> Path:
    view = load_view(view_path)
    model_path = model_path_for(view_path, view.model)
    model, _, diagnostics = validate_inputs(model_path, view_path)
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        raise ValueError("\n".join(map(str, errors)))
    output = output or ROOT / "build" / "drawio" / f"{view.id}.drawio"
    output.parent.mkdir(parents=True, exist_ok=True)
    get_renderer(view.diagram_type).render(model, view).write(str(output))
    artifact_errors = [item for item in validate_artifact(output) if item.severity == "error"]
    if artifact_errors:
        raise ValueError("\n".join(map(str, artifact_errors)))
    return output


def qa(view_path: Path) -> tuple[Path, list[str]]:
    view = load_view(view_path)
    drawio = render(view_path)
    artifact_diagnostics = validate_artifact(drawio)
    diagnostics = [str(item) for item in artifact_diagnostics]
    preview = ROOT / "build" / "preview" / f"{drawio.stem}.png"
    tool = find_drawio()
    metrics = analyze_visual_metrics(drawio)
    review = view.visual_review or {}
    q6: dict
    preview_record: dict
    if tool:
        export_drawio(drawio, preview, preview=True)
        preview_hash = sha256_file(preview)
        with preview.open("rb") as stream:
            header = stream.read(24)
        pixel_size = None
        if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) == 24:
            width, height = struct.unpack(">II", header[16:24])
            pixel_size = {"width": width, "height": height}
        hash_matches = review.get("previewHash") == preview_hash
        exporter_matches = review.get("exporterVersion") in {None, tool.version}
        human_approved = review.get("status") == "approved" and exporter_matches
        approved = human_approved and hash_matches
        preview_record = {
            "path": str(preview.relative_to(ROOT)),
            "sha256": preview_hash,
            "pixelSize": pixel_size,
        }
        q6 = {
            "applicable": True,
            "status": "pass" if approved else "awaiting_review",
            "preview": preview_record["path"],
            "previewHash": preview_record["sha256"],
            "previewSize": preview_record["pixelSize"],
            "humanReview": {
                "status": (
                    "approved_current_preview"
                    if approved
                    else "approved_stale_preview"
                    if human_approved
                    else "not_recorded"
                ),
                "declaredStatus": review.get("status"),
                "reviewer": review.get("reviewer"),
                "reviewedAt": review.get("reviewedAt"),
                "notes": review.get("notes"),
                "approvedPreviewHash": review.get("previewHash"),
                "hashMatchesCurrentPreview": hash_matches,
                "approvedExporterVersion": review.get("exporterVersion"),
                "currentExporterVersion": tool.version,
                "exporterVersionMatches": exporter_matches,
            },
            "hashPurpose": "Identifies the reviewed preview; it does not constitute visual review.",
        }
    else:
        preview_record = {"path": None, "sha256": None, "pixelSize": None}
        q6 = {
            "applicable": False,
            "status": "unavailable",
            "reason": "draw.io desktop CLI unavailable",
            "preview": None,
            "previewHash": None,
            "previewSize": None,
            "humanReview": {
                "status": "not_verifiable_without_preview",
                "declaredStatus": review.get("status"),
                "reviewer": review.get("reviewer"),
                "reviewedAt": review.get("reviewedAt"),
                "notes": review.get("notes"),
                "approvedPreviewHash": review.get("previewHash"),
                "hashMatchesCurrentPreview": None,
            },
            "hashPurpose": "No preview hash is available; visual QA is not claimed.",
        }
    gates = {
        "Q4": "pass"
        if not any(item.gate == "Q4" and item.severity == "error" for item in artifact_diagnostics)
        else "fail",
        "Q5": (
            "fail"
            if any(item.gate == "Q5" and item.severity == "error" for item in artifact_diagnostics)
            else "pass_with_warnings"
            if any(item.gate == "Q5" and item.severity == "warning" for item in artifact_diagnostics)
            else "pass"
        ),
        "Q6": q6,
    }
    report = ROOT / "build" / "qa" / f"{drawio.stem}.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        json.dumps(
            {
                "artifact": str(drawio.relative_to(ROOT)),
                "diagnostics": diagnostics,
                "gates": gates,
                "visualReview": {
                    "schemaVersion": 1,
                    "preview": preview_record,
                    "diagramCanvas": metrics["canvas"],
                    "metrics": metrics,
                    "humanReview": q6["humanReview"],
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
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
    view = load_view(view_path)
    if view.approval != "approved":
        raise ValueError("Q7 requires view.approval: approved")
    model_path = model_path_for(view_path, view.model)
    model, _, input_diagnostics = validate_inputs(model_path, view_path)
    if model.test_data:
        raise ValueError("Q7 forbids releasing models marked testData")
    if any(item.severity == "error" for item in input_diagnostics):
        raise ValueError("Q0-Q3 input gates contain blocking errors")
    unsupported = set(view.output_targets) - {"drawio", "png", "svg", "pdf", "jpg"}
    if unsupported:
        raise ValueError(f"unsupported visual output targets: {', '.join(sorted(unsupported))}")
    tool = find_drawio()
    image_targets = set(view.output_targets) & {"png", "svg", "pdf", "jpg"}
    if image_targets and not tool:
        raise RuntimeError("requested image export requires the draw.io desktop CLI")
    drawio = render(view_path)
    report, diagnostics = qa(view_path)
    report_data = json.loads(report.read_text(encoding="utf-8"))
    if any(" ERROR " in item for item in diagnostics):
        raise ValueError("QA contains blocking errors")
    q6 = report_data["gates"]["Q6"]
    if not q6["applicable"] or q6["status"] != "pass":
        raise ValueError(
            "Q6 requires an actual rendered preview and approved visualReview matching its hash"
        )
    final = ROOT / "build" / "final"
    final.mkdir(parents=True, exist_ok=True)
    final_drawio = final / drawio.name
    shutil.copy2(drawio, final_drawio)
    outputs = [final_drawio]
    for target in view.output_targets:
        if target in {"png", "svg", "pdf", "jpg"}:
            suffix = f".drawio.{target}" if target == "png" else f".{target}"
            outputs.append(export_drawio(final_drawio, final / f"{view.id}{suffix}"))
    manifest = create_manifest(
        diagram_id=view.id,
        diagram_type=view.diagram_type,
        model_data=load_yaml(model_path),
        outputs=outputs,
        qa={
            "result": "pass",
            "report": str(report.relative_to(ROOT)),
            "gates": report_data["gates"],
            "Q7": "pass",
        },
        model_path=model_path,
        view_path=view_path,
        requested_targets=view.output_targets,
        exporter_version=tool.version if tool else None,
    )
    manifest_path = final / f"{view.id}.manifest.json"
    write_manifest(manifest_path, manifest)
    _register_artifact(view.id, manifest_path)
    outputs.append(manifest_path)
    return outputs
