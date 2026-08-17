from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

from engine import __version__
from engine.core.io import ROOT, load_model, load_view, load_yaml
from engine.export import export_svg_png, find_edge
from engine.manifests import stale_reasons
from engine.pipeline import build, model_path_for, qa, render
from engine.use_case_modeling import render_markdown
from qa.pipeline import validate_inputs, validate_sources
from qa.semantic import validate_model


def _print_diagnostics(items) -> int:
    for item in items:
        print(item)
    errors = [item for item in items if getattr(item, "severity", "error") == "error"]
    if not items:
        print("PASS")
    return 1 if errors else 0


def command_validate(args) -> int:
    diagnostics = validate_sources()
    if args.view:
        view_path = Path(args.view).resolve()
        view = load_view(view_path)
        model_path = model_path_for(view_path, view.model)
        _, _, more = validate_inputs(model_path, view_path)
        diagnostics.extend(more)
    return _print_diagnostics(diagnostics)


def command_validate_view(args) -> int:
    view_path = Path(args.view).resolve()
    view = load_view(view_path)
    model_path = model_path_for(view_path, view.model)
    _, _, diagnostics = validate_inputs(model_path, view_path)
    return _print_diagnostics(diagnostics)


def command_validate_model(args) -> int:
    return _print_diagnostics(validate_model(load_model(Path(args.model))))


def command_traceability(args) -> int:
    model = load_model(Path(args.model))
    diagnostics = [item for item in validate_model(model) if item.gate == "Q2"]
    covered = sum(bool(item.source_refs) for item in model.elements) + sum(
        bool(item.source_refs) for item in model.relations
    )
    total = len(model.elements) + len(model.relations)
    print(f"Traceability: {covered}/{total} records covered")
    return _print_diagnostics(diagnostics)


def command_render(args) -> int:
    path = render(Path(args.view).resolve(), Path(args.output).resolve() if args.output else None)
    print(path)
    return 0


def command_preview(args) -> int:
    svg = render(Path(args.view).resolve())
    output = (
        Path(args.output).resolve()
        if args.output
        else ROOT / "build" / "preview" / f"{svg.stem}.png"
    )
    print(export_svg_png(svg, output))
    return 0


def command_qa(args) -> int:
    report, diagnostics = qa(Path(args.view).resolve())
    print(report)
    report_data = json.loads(report.read_text(encoding="utf-8"))
    blocked = report_data["gates"]["Q4"] == "fail" or report_data["gates"]["Q5"] == "fail"
    return 1 if blocked else 0


def command_build(args) -> int:
    for path in build(Path(args.view).resolve()):
        print(path)
    return 0


def command_doctor(args) -> int:
    checks = {
        "engine": __version__,
        "python": platform.python_version(),
        "python_ok": sys.version_info >= (3, 11),
        "svg_rasterizer": find_edge(),
        "source_files": not bool(validate_sources()),
        "root_writable": os.access(ROOT, os.W_OK),
    }
    print(json.dumps(checks, indent=2))
    required = (
        checks["python_ok"]
        and bool(checks["svg_rasterizer"])
        and checks["source_files"]
        and checks["root_writable"]
    )
    return 0 if required else 1


def command_types(args) -> int:
    for item in load_yaml(ROOT / "registry/diagram-types.yaml")["types"]:
        print(item)
    return 0


def command_stale(args) -> int:
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    reasons = stale_reasons(manifest)
    print("STALE: " + "; ".join(reasons) if reasons else "CURRENT")
    return 1 if reasons else 0


def command_use_case_model(args) -> int:
    source = Path(args.source).resolve()
    output = Path(args.output).resolve() if args.output else source.with_suffix(".md")
    print(render_markdown(source, output))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="diagram-engine")
    commands = root.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("view", nargs="?")
    validate.set_defaults(func=command_validate)
    commands.add_parser("validate-sources").set_defaults(
        func=lambda args: _print_diagnostics(validate_sources())
    )
    validate_view = commands.add_parser("validate-view")
    validate_view.add_argument("view")
    validate_view.set_defaults(func=command_validate_view)
    model = commands.add_parser("validate-model")
    model.add_argument("model")
    model.set_defaults(func=command_validate_model)
    trace = commands.add_parser("traceability")
    trace.add_argument("model")
    trace.set_defaults(func=command_traceability)
    render_cmd = commands.add_parser("render")
    render_cmd.add_argument("view")
    render_cmd.add_argument("-o", "--output")
    render_cmd.set_defaults(func=command_render)
    preview = commands.add_parser("preview")
    preview.add_argument("view")
    preview.add_argument("-o", "--output")
    preview.set_defaults(func=command_preview)
    qa_cmd = commands.add_parser("qa")
    qa_cmd.add_argument("view")
    qa_cmd.set_defaults(func=command_qa)
    build_cmd = commands.add_parser("build")
    build_cmd.add_argument("view")
    build_cmd.set_defaults(func=command_build)
    commands.add_parser("doctor").set_defaults(func=command_doctor)
    commands.add_parser("list-diagram-types").set_defaults(func=command_types)
    stale = commands.add_parser("stale")
    stale.add_argument("manifest")
    stale.set_defaults(func=command_stale)
    use_case_model = commands.add_parser("render-use-case-model")
    use_case_model.add_argument("source")
    use_case_model.add_argument("-o", "--output")
    use_case_model.set_defaults(func=command_use_case_model)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
