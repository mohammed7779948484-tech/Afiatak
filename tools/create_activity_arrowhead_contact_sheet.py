#!/usr/bin/env python3
"""Create a labeled contact sheet of all control-flow arrow endpoints in an Activity SVG preview."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

SVG_NS = "{http://www.w3.org/2000/svg}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    parser.add_argument("png", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--crop-size", type=int, default=520)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = ET.parse(args.svg).getroot()
    _, _, logical_width, logical_height = map(float, root.attrib["viewBox"].split())
    source = Image.open(args.png).convert("RGB")
    scale_x = source.width / logical_width
    scale_y = source.height / logical_height
    half = args.crop_size // 2
    font = ImageFont.load_default()

    endpoints: list[tuple[str, float, float]] = []
    for group in root.findall(f".//{SVG_NS}g"):
        if group.attrib.get("data-kind") != "control-flow":
            continue
        relation_id = group.attrib["id"]
        polyline = group.find(f"{SVG_NS}polyline")
        if polyline is None:
            continue
        points = re.findall(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", polyline.attrib["points"])
        x, y = map(float, points[-1])
        endpoints.append((relation_id, x, y))

    cols = 4
    rows = (len(endpoints) + cols - 1) // cols
    tile_h = args.crop_size + 34
    sheet = Image.new("RGB", (cols * args.crop_size, rows * tile_h), "white")
    draw = ImageDraw.Draw(sheet)

    for index, (relation_id, logical_x, logical_y) in enumerate(endpoints):
        centre_x = round(logical_x * scale_x)
        centre_y = round(logical_y * scale_y)
        left = centre_x - half
        top = centre_y - half
        right = centre_x + half
        bottom = centre_y + half
        crop = Image.new("RGB", (args.crop_size, args.crop_size), "white")
        crop_box = (max(0, left), max(0, top), min(source.width, right), min(source.height, bottom))
        pixels = source.crop(crop_box)
        crop.paste(pixels, (max(0, -left), max(0, -top)))
        col = index % cols
        row = index // cols
        x = col * args.crop_size
        y = row * tile_h
        sheet.paste(crop, (x, y + 34))
        draw.text((x + 8, y + 8), f"{relation_id} @ ({logical_x:g}, {logical_y:g})", fill="black", font=font)
        marker_x = x + args.crop_size // 2
        marker_y = y + 34 + args.crop_size // 2
        draw.line((marker_x - 16, marker_y, marker_x + 16, marker_y), fill="#d62728", width=2)
        draw.line((marker_x, marker_y - 16, marker_x, marker_y + 16), fill="#d62728", width=2)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"{len(endpoints)} endpoint crops written to {args.output}")


if __name__ == "__main__":
    main()
