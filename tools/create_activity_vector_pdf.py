#!/usr/bin/env python3
"""Place one activity SVG as a vector graphic on an A3 portrait PDF page."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from weasyprint import HTML


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print('Usage: create_activity_vector_pdf.py INPUT_SVG [OUTPUT_PDF]', file=sys.stderr)
        return 2
    svg = Path(argv[1]).resolve()
    output = Path(argv[2]).resolve() if len(argv) == 3 else svg.with_suffix('.pdf')
    svg_text = svg.read_text(encoding='utf-8')
    match = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', svg_text)
    if not match:
        raise ValueError(f'Missing SVG viewBox: {svg}')
    width, height = (float(match.group(1)), float(match.group(2)))
    landscape = width > height
    page_size = 'A3 landscape' if landscape else 'A3 portrait'
    page_width, page_height = ('16.535in', '11.693in') if landscape else ('11.693in', '16.535in')
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
    @page {{ size: {page_size}; margin: 0; }}
    html, body {{ margin: 0; padding: 0; background: #fff; }}
    section {{ width: {page_width}; height: {page_height}; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
    img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
    </style></head><body><section><img src="{svg.as_uri()}" alt="Aafiatak Activity Diagram" /></section></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(svg.parent)).write_pdf(str(output))
    print(output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
