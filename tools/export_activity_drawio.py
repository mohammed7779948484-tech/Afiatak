#!/usr/bin/env python3
"""Export an Activity Diagram View as editable diagrams.net XML."""
from __future__ import annotations

import sys
from pathlib import Path

from engine.activity_drawio_export import export_activity_drawio
from engine.core.io import load_model, load_view


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print('Usage: export_activity_drawio.py <view.yaml> <output.drawio>', file=sys.stderr)
        return 2
    view_path = Path(argv[1]).resolve()
    output_path = Path(argv[2]).resolve()
    view = load_view(view_path)
    model_path = Path(view.model)
    if not model_path.is_absolute():
        model_path = (view_path.parent / model_path).resolve()
    model = load_model(model_path)
    if view.diagram_type != 'activity':
        raise ValueError(f'Expected activity view, got {view.diagram_type}')
    export_activity_drawio(model, view, output_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
