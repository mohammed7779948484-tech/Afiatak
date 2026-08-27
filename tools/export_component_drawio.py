from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.component_drawio_export import export_component_drawio
from engine.core.io import load_model, load_view
from engine.pipeline import model_path_for


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a Component ViewSpec to editable diagrams.net XML.")
    parser.add_argument("view", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    view_path = args.view.resolve()
    view = load_view(view_path)
    model = load_model(model_path_for(view_path, view.model))
    if view.diagram_type != "component":
        raise ValueError("Component draw.io export requires a component ViewSpec")
    export_component_drawio(model, view, args.output.resolve())
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
