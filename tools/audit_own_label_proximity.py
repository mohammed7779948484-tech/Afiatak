#!/usr/bin/env python3
"""Report shortest label-edge distance to each owning structural-link polyline.

This is a read-only evidence tool. The formal enforcement lives in
``qa.collaboration_svg_validation`` so normal ``engine.cli qa`` runs retain a
single quality gate.
"""
from __future__ import annotations

import argparse
import json
from math import hypot
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.collaboration_geometry import Point, Polyline, Rect, Segment, parse_polyline, parse_rect


def point_to_segment_distance(point: Point, segment: Segment) -> float:
    dx = segment.end.x - segment.start.x
    dy = segment.end.y - segment.start.y
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return hypot(point.x - segment.start.x, point.y - segment.start.y)
    projection = ((point.x - segment.start.x) * dx + (point.y - segment.start.y) * dy) / length_squared
    projection = min(1.0, max(0.0, projection))
    nearest = Point(segment.start.x + projection * dx, segment.start.y + projection * dy)
    return hypot(point.x - nearest.x, point.y - nearest.y)


def segment_to_segment_distance(first: Segment, second: Segment) -> float:
    from engine.collaboration_geometry import segments_intersect

    if segments_intersect(first, second):
        return 0.0
    return min(
        point_to_segment_distance(first.start, second),
        point_to_segment_distance(first.end, second),
        point_to_segment_distance(second.start, first),
        point_to_segment_distance(second.end, first),
    )


def rect_to_polyline_distance(rect: Rect, polyline: Polyline) -> float:
    corners = (
        Point(rect.left, rect.top),
        Point(rect.right, rect.top),
        Point(rect.right, rect.bottom),
        Point(rect.left, rect.bottom),
    )
    rect_edges = tuple(Segment(corners[index], corners[(index + 1) % 4]) for index in range(4))
    return min(segment_to_segment_distance(rect_edge, link_segment) for rect_edge in rect_edges for link_segment in polyline.segments)


def audit(svg_path: Path) -> dict:
    root = ET.parse(svg_path).getroot()
    links = {
        node.attrib["data-semantic-id"]: parse_polyline(node.attrib["data-points"])
        for node in root.iter()
        if node.attrib.get("data-kind") == "structural-link"
    }
    records = []
    for node in root.iter():
        if node.attrib.get("data-kind") != "message" or node.attrib.get("data-self-message") == "true":
            continue
        label = parse_rect(node.attrib["data-label-bounds"])
        link_id = node.attrib["data-structural-link"]
        distance = rect_to_polyline_distance(label, links[link_id])
        records.append(
            {
                "message": node.attrib["data-semantic-id"],
                "sequence": int(node.attrib["data-sequence"]),
                "structuralLink": link_id,
                "labelBounds": label.data(),
                "ownLinkDistance": round(distance, 2),
            }
        )
    records.sort(key=lambda item: (item["ownLinkDistance"], item["sequence"]), reverse=True)
    return {
        "svg": str(svg_path),
        "messageCount": len(records),
        "maxOwnLinkDistance": max((item["ownLinkDistance"] for item in records), default=0.0),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.svg)
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
