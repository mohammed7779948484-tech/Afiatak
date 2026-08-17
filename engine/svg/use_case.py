from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions import (
    ACTORS,
    BOUNDARY,
    CANVAS,
    DEPENDENCY_LABELS,
    FIELDS,
    ROUTES,
    USE_CASES,
    Box,
)
from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticElement, SemanticModel, SemanticRelation, ViewSpec

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def _tag(name: str) -> str:
    return f"{{{SVG}}}{name}"


def _wrap(text: str, limit: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:3]


def _text(parent: ET.Element, value: str, x: float, y: float, role: str, *, limit: int) -> None:
    lines = _wrap(value, limit)
    node = ET.SubElement(parent, _tag("text"), {"x": str(x), "y": str(y), "class": role})
    line_height = 17 if role in {"use-case-label", "actor-label"} else 15
    start = y - (len(lines) - 1) * line_height / 2
    for index, line in enumerate(lines):
        span = ET.SubElement(
            node,
            _tag("tspan"),
            {"x": str(x), "y": f"{start + index * line_height:g}"},
        )
        span.text = line


def _bounds_attributes(box: Box) -> dict[str, str]:
    return {
        "data-x": str(box.x),
        "data-y": str(box.y),
        "data-width": str(box.width),
        "data-height": str(box.height),
    }


def _actor(parent: ET.Element, item: SemanticElement, box: Box) -> None:
    group = ET.SubElement(
        parent,
        _tag("g"),
        {
            "id": item.id.replace(".", "-"),
            "data-semantic-id": item.id,
            "data-kind": "actor",
            **_bounds_attributes(box),
        },
    )
    centre = box.x + box.width / 2
    head_y = box.y + 19
    ET.SubElement(group, _tag("circle"), {"cx": str(centre), "cy": str(head_y), "r": "10", "class": "actor"})
    ET.SubElement(group, _tag("path"), {"d": f"M {centre} {head_y + 10} V {box.y + 58} M {centre - 25} {box.y + 42} H {centre + 25} M {centre} {box.y + 58} L {centre - 23} {box.y + 82} M {centre} {box.y + 58} L {centre + 23} {box.y + 82}", "class": "actor"})
    _text(group, item.name, centre, box.y + 101, "actor-label", limit=28)


def _use_case(parent: ET.Element, item: SemanticElement, box: Box, role: str) -> None:
    group = ET.SubElement(
        parent,
        _tag("g"),
        {
            "id": item.id.replace(".", "-"),
            "data-semantic-id": item.id,
            "data-kind": "use_case",
            **_bounds_attributes(box),
        },
    )
    ET.SubElement(
        group,
        _tag("ellipse"),
        {
            "cx": str(box.x + box.width / 2),
            "cy": str(box.y + box.height / 2),
            "rx": str(box.width / 2),
            "ry": str(box.height / 2),
            "class": f"use-case {role}",
        },
    )
    _text(
        group,
        item.name,
        box.x + box.width / 2,
        box.y + box.height / 2 + 5,
        "use-case-label",
        limit=29,
    )


def _path_data(points: tuple[tuple[float, float], ...]) -> str:
    return "M " + " L ".join(f"{x:g} {y:g}" for x, y in points)


def _points_data(points: tuple[tuple[float, float], ...]) -> str:
    return " ".join(f"{x:g},{y:g}" for x, y in points)


def _role(item_id: str) -> str:
    number = int(item_id.rsplit("-", 1)[1])
    if number <= 5:
        return "access"
    if number in {6, 9, 11, 12, 13, 14}:
        return "patient"
    if number in {15, 16}:
        return "facility"
    if number in {19, 20, 21, 22}:
        return "operations"
    if number in {25, 26}:
        return "doctor"
    return "platform"


def _css(theme: dict) -> str:
    colors = theme["colors"]
    type_ = theme["typography"]
    geometry = theme["geometry"]
    return f"""
text {{ font-family: {type_["family"]}; fill: {colors["ink"]}; text-anchor: middle; }}
.page-title {{ font-size: {type_["page_title"]}px; font-weight: 700; }}
.boundary-title {{ font-size: {type_["boundary_title"]}px; font-weight: 700; text-anchor: start; }}
.section-label {{ font-size: {type_["section"]}px; font-weight: 700; letter-spacing: 1.2px; text-anchor: start; text-transform: uppercase; }}
.use-case-label {{ font-size: {type_["use_case"]}px; }}
.actor-label {{ font-size: {type_["actor"]}px; font-weight: 600; }}
.stereotype {{ font-size: {type_["stereotype"]}px; font-style: italic; }}
.condition {{ font-size: {type_["condition"]}px; fill: {colors["muted"]}; }}
.boundary {{ fill: none; stroke: {colors["boundary"]}; stroke-width: {geometry["boundary_stroke"]}; }}
.field {{ fill: {colors["field"]}; opacity: .72; }}
.field-accent {{ stroke-width: 4; stroke-linecap: round; }}
.actor {{ fill: none; stroke: {colors["ink"]}; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }}
.use-case {{ stroke: {colors["boundary"]}; stroke-width: {geometry["use_case_stroke"]}; }}
.access {{ fill: {colors["access"]}; }} .patient {{ fill: {colors["patient"]}; }}
.facility {{ fill: {colors["facility"]}; }} .operations {{ fill: {colors["operations"]}; }}
.doctor {{ fill: {colors["doctor"]}; }} .platform {{ fill: {colors["platform"]}; }}
.association {{ fill: none; stroke: {colors["association"]}; stroke-width: {geometry["association_stroke"]}; stroke-linecap: round; stroke-linejoin: round; }}
.dependency {{ fill: none; stroke: {colors["dependency"]}; stroke-width: {geometry["dependency_stroke"]}; stroke-dasharray: 7 5; marker-end: url(#dependency-arrow); stroke-linecap: round; stroke-linejoin: round; }}
.label-backdrop {{ fill: {theme["canvas"]["background"]}; opacity: .94; }}
""".strip()


def render_use_case_svg(model: SemanticModel, view: ViewSpec, output: Path) -> Path:
    if view.id != "aafiatak-main-use-case":
        raise ValueError(f"no curated SVG composition for {view.id}")
    selected = set(view.include)
    expected = set(ACTORS) | set(USE_CASES)
    if selected != expected:
        missing = sorted(expected - selected)
        extra = sorted(selected - expected)
        raise ValueError(f"composition/view mismatch; missing={missing}, extra={extra}")
    relation_ids = set(view.relations)
    if relation_ids != set(ROUTES):
        missing = sorted(set(ROUTES) - relation_ids)
        extra = sorted(relation_ids - set(ROUTES))
        raise ValueError(f"route/view mismatch; missing={missing}, extra={extra}")

    theme = load_yaml(ROOT / "design" / "use_case_theme.yaml")
    elements = model.by_id
    relations = {item.id: item for item in model.relations}
    root = ET.Element(
        _tag("svg"),
        {
            "width": str(CANVAS[0]),
            "height": str(CANVAS[1]),
            "viewBox": f"0 0 {CANVAS[0]} {CANVAS[1]}",
            "role": "img",
            "aria-labelledby": "diagram-title diagram-description",
        },
    )
    title = ET.SubElement(root, _tag("title"), {"id": "diagram-title"})
    title.text = view.title
    description = ET.SubElement(root, _tag("desc"), {"id": "diagram-description"})
    description.text = "System-level UML use case overview for the Aafiatak medical appointment booking system."
    defs = ET.SubElement(root, _tag("defs"))
    style = ET.SubElement(defs, _tag("style"))
    style.text = _css(theme)
    marker = ET.SubElement(
        defs,
        _tag("marker"),
        {"id": "dependency-arrow", "viewBox": "0 0 10 10", "refX": "9", "refY": "5", "markerWidth": "8", "markerHeight": "8", "orient": "auto-start-reverse"},
    )
    ET.SubElement(marker, _tag("path"), {"d": "M 0 0 L 10 5 L 0 10", "fill": "none", "stroke": theme["colors"]["dependency"], "stroke-width": "1.4"})
    ET.SubElement(root, _tag("rect"), {"width": str(CANVAS[0]), "height": str(CANVAS[1]), "fill": theme["canvas"]["background"]})
    _text(root, view.title, CANVAS[0] / 2, 42, "page-title", limit=80)
    ET.SubElement(root, _tag("rect"), {"x": str(BOUNDARY.x), "y": str(BOUNDARY.y), "width": str(BOUNDARY.width), "height": str(BOUNDARY.height), "rx": "4", "class": "boundary", "id": "system-boundary", **_bounds_attributes(BOUNDARY)})
    _text(root, view.options.get("systemName", "Aafiatak"), BOUNDARY.x + 24, BOUNDARY.y + 31, "boundary-title", limit=80)

    field_group = ET.SubElement(root, _tag("g"), {"aria-label": "Presentation-only visual neighborhoods"})
    accent_by_role = {key: theme["colors"][key] for key in ("access", "patient", "facility", "operations", "platform")}
    for label, box, role in FIELDS:
        ET.SubElement(field_group, _tag("rect"), {"x": str(box.x), "y": str(box.y), "width": str(box.width), "height": str(box.height), "rx": "20", "class": "field"})
        ET.SubElement(field_group, _tag("line"), {"x1": str(box.x + 1), "y1": str(box.y + 18), "x2": str(box.x + 38), "y2": str(box.y + 18), "class": "field-accent", "stroke": accent_by_role[role]})
        _text(field_group, label.upper(), box.x + 48, box.y + 23, "section-label", limit=60)

    relation_group = ET.SubElement(root, _tag("g"), {"aria-label": "UML relationships"})
    for relation_id in view.relations:
        relation = relations[relation_id]
        dependency = relation.type in {"include", "extend"}
        ET.SubElement(
            relation_group,
            _tag("path"),
            {
                "id": relation_id.replace(".", "-"),
                "data-relation-id": relation_id,
                "data-source": relation.source,
                "data-target": relation.target,
                "data-points": _points_data(ROUTES[relation_id]),
                "d": _path_data(ROUTES[relation_id]),
                "class": "dependency" if dependency else "association",
            },
        )
        if dependency:
            stereotype_position, condition_position = DEPENDENCY_LABELS[relation_id]
            _text(relation_group, f"<<{relation.type}>>", *stereotype_position, "stereotype", limit=30)
            condition = relation.metadata.get("condition")
            if condition and condition_position:
                _text(relation_group, str(condition), *condition_position, "condition", limit=48)

    node_group = ET.SubElement(root, _tag("g"), {"aria-label": "Use cases"})
    for item_id, box in USE_CASES.items():
        _use_case(node_group, elements[item_id], box, _role(item_id))
    actor_group = ET.SubElement(root, _tag("g"), {"aria-label": "Actors outside the system boundary"})
    for item_id, box in ACTORS.items():
        _actor(actor_group, elements[item_id], box)

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="  ")
    output.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
    return output
