from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticModel, ViewSpec
from engine.svg.use_case import SVG, _bounds_attributes, _css, _tag, _text, _use_case


def _embedded_actor(parent, item, box):
    group = ET.SubElement(parent, _tag("g"), {
        "id": item.id.replace(".", "-"),
        "data-semantic-id": item.id,
        "data-kind": "actor",
        "data-embedded-actor": "true",
        **_bounds_attributes(box),
    })
    centre = box.x + box.width / 2
    head_y = box.y + 14
    ET.SubElement(group, _tag("circle"), {"cx": str(centre), "cy": str(head_y), "r": "9", "class": "actor"})
    ET.SubElement(group, _tag("path"), {"d": f"M {centre} {head_y + 9} V {box.y + 43} M {centre - 22} {box.y + 28} H {centre + 22} M {centre} {box.y + 43} L {centre - 19} {box.y + 62} M {centre} {box.y + 43} L {centre + 19} {box.y + 62}", "class": "actor"})
    _text(group, item.name, centre + 115, box.y + 31, "actor-label", limit=28)


def render_embedded_actor_package_svg(model: SemanticModel, view: ViewSpec, output: Path, composition, description: str) -> Path:
    selected = set(view.include)
    expected = set(composition.ACTORS) | set(composition.USE_CASES)
    if selected != expected:
        raise ValueError(f"composition/view mismatch; missing={sorted(expected-selected)}, extra={sorted(selected-expected)}")
    if view.relations:
        raise ValueError("embedded actor presentation must not render relationships")
    theme = load_yaml(ROOT / "design" / "use_case_theme.yaml")
    elements = model.by_id
    root = ET.Element(_tag("svg"), {"width": str(composition.CANVAS[0]), "height": str(composition.CANVAS[1]), "viewBox": f"0 0 {composition.CANVAS[0]} {composition.CANVAS[1]}", "role": "img", "aria-labelledby": "diagram-title diagram-description"})
    title = ET.SubElement(root, _tag("title"), {"id": "diagram-title"}); title.text = view.title
    desc = ET.SubElement(root, _tag("desc"), {"id": "diagram-description"}); desc.text = description
    defs = ET.SubElement(root, _tag("defs")); style = ET.SubElement(defs, _tag("style"))
    style.text = _css(theme) + f"\n.package {{ fill: none; stroke: {theme['colors']['boundary']}; stroke-width: 1.8; }}\n.package-tab {{ fill: {theme['colors']['field']}; stroke: {theme['colors']['boundary']}; stroke-width: 1.8; }}\n.helper {{ fill: {theme['colors']['helper']}; }}\n.use-case-label {{ font-size: 16px; }}\n.section-label {{ font-size: 15px; letter-spacing: 0.8px; }}\n.boundary-title {{ font-size: 14px; }}"
    ET.SubElement(root, _tag("rect"), {"width": str(composition.CANVAS[0]), "height": str(composition.CANVAS[1]), "fill": theme["canvas"]["background"]})
    _text(root, view.title, composition.CANVAS[0] / 2, 48, "page-title", limit=100)
    b = composition.BOUNDARY
    ET.SubElement(root, _tag("rect"), {"x": str(b.x), "y": str(b.y), "width": str(b.width), "height": str(b.height), "rx": "4", "class": "boundary", "id": "system-boundary", **_bounds_attributes(b)})
    _text(root, view.options.get("systemName", "Aafiatak"), b.x + 24, b.y + 31, "boundary-title", limit=90)
    p = composition.PACKAGE
    group = ET.SubElement(root, _tag("g"), {"aria-label": "Embedded package actor and UML package container"})
    path = f"M {p.x:g} {p.y+24:g} H {p.x+220:g} V {p.y:g} H {p.x+p.width:g} V {p.y+p.height:g} H {p.x:g} Z"
    ET.SubElement(group, _tag("path"), {"id": "package-container", "d": path, "class": "package", **_bounds_attributes(p)})
    embedded_actor_id = next(iter(composition.ACTORS))
    tab_attributes = {
        "x": str(p.x),
        "y": str(p.y),
        "width": "220",
        "height": "34",
        "class": "package-tab",
        "data-semantic-id": embedded_actor_id,
        "data-kind": "actor",
        "data-embedded-actor": "true",
        **_bounds_attributes(p),
    }
    ET.SubElement(group, _tag("rect"), tab_attributes)
    _text(group, elements[embedded_actor_id].name, p.x + 110, p.y + 22, "boundary-title", limit=32)
    field_group = ET.SubElement(root, _tag("g"), {"aria-label": "Presentation-only neighborhoods"})
    accent = {key: theme["colors"][key] for key in ("access", "patient", "facility", "operations", "doctor", "platform")}
    for label, box, role in composition.FIELDS:
        ET.SubElement(field_group, _tag("rect"), {"x": str(box.x), "y": str(box.y), "width": str(box.width), "height": str(box.height), "rx": "18", "class": "field"})
        ET.SubElement(field_group, _tag("line"), {"x1": str(box.x+1), "y1": str(box.y+18), "x2": str(box.x+38), "y2": str(box.y+18), "class": "field-accent", "stroke": accent[role]})
        _text(field_group, label.upper(), box.x+48, box.y+23, "section-label", limit=60)
    nodes = ET.SubElement(root, _tag("g"), {"aria-label": "Use cases without displayed relationships"})
    for item_id, box in composition.USE_CASES.items():
        _use_case(nodes, elements[item_id], box, composition.CASE_ROLES[item_id])
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="  ")
    output.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
    return output
