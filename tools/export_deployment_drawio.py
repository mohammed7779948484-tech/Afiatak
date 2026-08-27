"""Export the DEP-01 deployment diagram to editable diagrams.net XML."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.core.io import load_model, load_view
from engine.deployment_drawio_export import export_deployment_drawio
from engine.pipeline import model_path_for


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python tools/export_deployment_drawio.py <view.yaml> <output.drawio>")
    view_path = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    view = load_view(view_path)
    if view.diagram_type != "deployment":
        raise SystemExit("DEP-01 draw.io export requires a deployment ViewSpec")
    model = load_model(model_path_for(view_path, view.model))
    export_deployment_drawio(model, view, output)
    print(output)


if __name__ == "__main__":
    main()
