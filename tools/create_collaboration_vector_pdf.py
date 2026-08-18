#!/usr/bin/env python3
"""Create one or more A0-landscape vector PDF pages from Collaboration SVG files."""
from __future__ import annotations

import sys
from pathlib import Path

from weasyprint import HTML


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: create_collaboration_vector_pdf.py OUTPUT_PDF INPUT_SVG [INPUT_SVG ...]", file=sys.stderr)
        return 2
    output = Path(argv[1]).resolve()
    svgs = [Path(value).resolve() for value in argv[2:]]
    for svg in svgs:
        if not svg.is_file() or svg.suffix.lower() != ".svg":
            raise ValueError(f"Expected an existing SVG: {svg}")
    sections = "\n".join(f'<section><img src="{svg.as_uri()}" alt="Aafiatak Collaboration Diagram" /></section>' for svg in svgs)
    html = f"""<!doctype html><html><head><meta charset=\"utf-8\"><style>
    @page {{ size: A0 landscape; margin: 0; }}
    html, body {{ margin: 0; padding: 0; background: #fff; }}
    section {{ width: 46.811in; height: 33.111in; display: flex; align-items: center; justify-content: center; overflow: hidden; break-after: page; }}
    section:last-child {{ break-after: auto; }}
    img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
    </style></head><body>{sections}</body></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(output.parent)).write_pdf(str(output))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
