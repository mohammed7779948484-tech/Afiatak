#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from engine.collaboration_drawio_export import export_collaboration_drawio
from engine.core.io import load_view, load_yaml
from engine.core.models import SemanticModel


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a collaboration View to editable diagrams.net XML.")
    parser.add_argument("view", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    view = load_view(args.view.resolve())
    if view.diagram_type != "communication":
        raise ValueError("This exporter accepts only communication Views")
    model_path = (args.view.parent / view.model).resolve()
    model = SemanticModel.from_dict(load_yaml(model_path))
    export_collaboration_drawio(model, view, args.output.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()
