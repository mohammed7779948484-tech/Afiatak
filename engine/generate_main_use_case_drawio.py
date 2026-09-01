from __future__ import annotations

import argparse
from pathlib import Path

from engine.core.io import ROOT, load_view
from engine.main_use_case_drawio_export import export_main_use_case_drawio
from qa.pipeline import validate_inputs


DEFAULT_VIEW = ROOT / "views" / "use-case" / "aafiatak-main-use-case.yaml"
DEFAULT_OUTPUT = ROOT / "build" / "final" / "Aafiatak_Main_Use_Case.drawio"


def _model_path(view_path: Path, model_value: str) -> Path:
    candidate = Path(model_value)
    return candidate if candidate.is_absolute() else (view_path.parent / candidate).resolve()


def generate(view_path: Path = DEFAULT_VIEW, output: Path = DEFAULT_OUTPUT) -> Path:
    view_path = view_path.resolve()
    raw_view = load_view(view_path)
    model_path = _model_path(view_path, raw_view.model)
    model, view, diagnostics = validate_inputs(model_path, view_path)
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        raise ValueError("\n".join(map(str, errors)))
    if view.approval != "approved":
        raise ValueError("the semantic view must be approved before native draw.io generation")
    return export_main_use_case_drawio(model, view, output.resolve())


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="aafiatak-main-use-case-drawio",
        description="Generate the editable native draw.io XML master for the approved Aafiatak Main Use Case view.",
    )
    root.add_argument("--view", type=Path, default=DEFAULT_VIEW)
    root.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        print(generate(args.view, args.output))
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
