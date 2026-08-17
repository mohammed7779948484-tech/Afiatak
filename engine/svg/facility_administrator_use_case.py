from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticModel, ViewSpec
from engine.svg.use_case import SVG, _actor, _bounds_attributes, _css, _path_data, _points_data, _tag, _text, _use_case

def _actor_duplicate(parent, item, box, duplicate_index):
    group = ET.SubElement(parent, _tag("g"), {
        "id": f"{item.id.replace('.', '-')}-duplicate-{duplicate_index}",
        "data-actor-duplicate-of": item.id,
        "data-kind": "actor-duplicate",
        **_bounds_attributes(box),
    })
    centre = box.x + box.width / 2
    head_y = box.y + 19
    ET.SubElement(group, _tag("circle"), {"cx": str(centre), "cy": str(head_y), "r": "10", "class": "actor"})
    ET.SubElement(group, _tag("path"), {"d": f"M {centre} {head_y + 10} V {box.y + 58} M {centre - 25} {box.y + 42} H {centre + 25} M {centre} {box.y + 58} L {centre - 23} {box.y + 82} M {centre} {box.y + 58} L {centre + 23} {box.y + 82}", "class": "actor"})
    if getattr(parent, "_unused", False):
        pass

def render_facility_administrator_svg(model: SemanticModel, view: ViewSpec, output: Path, composition, description: str) -> Path:
    selected = set(view.include)
    expected = set(composition.ACTORS) | set(composition.USE_CASES)
    if selected != expected:
        raise ValueError(f"composition/view mismatch; missing={sorted(expected-selected)}, extra={sorted(selected-expected)}")
    relation_ids = set(view.relations)
    if relation_ids != set(composition.ROUTES):
        raise ValueError(f"route/view mismatch; missing={sorted(set(composition.ROUTES)-relation_ids)}, extra={sorted(relation_ids-set(composition.ROUTES))}")
    theme = load_yaml(ROOT / "design" / "use_case_theme.yaml")
    elements = model.by_id
    relations = {item.id: item for item in model.relations}
    root = ET.Element(_tag("svg"), {"width": str(composition.CANVAS[0]), "height": str(composition.CANVAS[1]), "viewBox": f"0 0 {composition.CANVAS[0]} {composition.CANVAS[1]}", "role": "img", "aria-labelledby": "diagram-title diagram-description"})
    title = ET.SubElement(root, _tag("title"), {"id": "diagram-title"}); title.text = view.title
    desc = ET.SubElement(root, _tag("desc"), {"id": "diagram-description"}); desc.text = description
    defs = ET.SubElement(root, _tag("defs")); style = ET.SubElement(defs, _tag("style"))
    style.text = _css(theme) + f"\n.package {{ fill: none; stroke: {theme['colors']['boundary']}; stroke-width: 1.8; }}\n.package-tab {{ fill: {theme['colors']['field']}; stroke: {theme['colors']['boundary']}; stroke-width: 1.8; }}\n.helper {{ fill: {theme['colors']['helper']}; }}"
    marker = ET.SubElement(defs, _tag("marker"), {"id": "dependency-arrow", "viewBox": "0 0 10 10", "refX": "9", "refY": "5", "markerWidth": "8", "markerHeight": "8", "orient": "auto-start-reverse"})
    ET.SubElement(marker, _tag("path"), {"d": "M 0 0 L 10 5 L 0 10", "fill": "none", "stroke": theme["colors"]["dependency"], "stroke-width": "1.4"})
    ET.SubElement(root, _tag("rect"), {"width": str(composition.CANVAS[0]), "height": str(composition.CANVAS[1]), "fill": theme["canvas"]["background"]})
    _text(root, view.title, composition.CANVAS[0]/2, 48, "page-title", limit=100)
    b = composition.BOUNDARY
    ET.SubElement(root, _tag("rect"), {"x": str(b.x), "y": str(b.y), "width": str(b.width), "height": str(b.height), "rx": "4", "class": "boundary", "id": "system-boundary", **_bounds_attributes(b)})
    _text(root, view.options.get("systemName", "Aafiatak"), b.x+24, b.y+31, "boundary-title", limit=80)
    p = composition.PACKAGE; group = ET.SubElement(root, _tag("g"), {"aria-label": "Facility Administrator Package UML container"})
    path = f"M {p.x:g} {p.y+24:g} H {p.x+220:g} V {p.y:g} H {p.x+p.width:g} V {p.y+p.height:g} H {p.x:g} Z"
    ET.SubElement(group, _tag("path"), {"id": "facility-administrator-package", "d": path, "class": "package", **_bounds_attributes(p)})
    ET.SubElement(group, _tag("rect"), {"x": str(p.x), "y": str(p.y), "width": "220", "height": "34", "class": "package-tab"})
    _text(group, view.options.get("packageName", "Facility Administrator Package"), p.x+110, p.y+22, "boundary-title", limit=34)
    field_group = ET.SubElement(root, _tag("g"), {"aria-label": "Presentation-only neighborhoods"})
    accent = {key: theme["colors"][key] for key in ("access", "patient", "facility", "operations", "doctor", "platform")}
    for label, box, role in composition.FIELDS:
        ET.SubElement(field_group, _tag("rect"), {"x": str(box.x), "y": str(box.y), "width": str(box.width), "height": str(box.height), "rx": "18", "class": "field"})
        ET.SubElement(field_group, _tag("line"), {"x1": str(box.x+1), "y1": str(box.y+18), "x2": str(box.x+38), "y2": str(box.y+18), "class": "field-accent", "stroke": accent[role]})
        _text(field_group, label.upper(), box.x+48, box.y+23, "section-label", limit=60)
    relation_group = ET.SubElement(root, _tag("g"), {"aria-label": "UML relationships"})
    for relation_id in view.relations:
        relation = relations[relation_id]; dependency = relation.type in {"include", "extend"}
        ET.SubElement(relation_group, _tag("path"), {"id": relation_id.replace(".", "-"), "data-relation-id": relation_id, "data-source": relation.source, "data-target": relation.target, "data-points": _points_data(composition.ROUTES[relation_id]), "d": _path_data(composition.ROUTES[relation_id]), "class": "dependency" if dependency else "association"})
        if dependency:
            pos, condition = composition.DEPENDENCY_LABELS[relation_id]
            _text(relation_group, f"<<{relation.type}>>", *pos, "stereotype", limit=30)
            if relation.metadata.get("condition") and condition:
                _text(relation_group, str(relation.metadata["condition"]), *condition, "condition", limit=48)
    nodes = ET.SubElement(root, _tag("g"), {"aria-label": "Facility Administrator use cases"})
    for item_id, box in composition.USE_CASES.items(): _use_case(nodes, elements[item_id], box, composition.CASE_ROLES[item_id])
    actors = ET.SubElement(root, _tag("g"), {"aria-label": "Actors outside the system boundary"})
    for item_id, box in composition.ACTORS.items():
        _actor(actors, elements[item_id], box)
        for duplicate_index, duplicate_box in enumerate(getattr(composition, "ACTOR_DUPLICATES", {}).get(item_id, ()), start=1):
            _actor_duplicate(actors, elements[item_id], duplicate_box, duplicate_index)
            if getattr(composition, "DUPLICATE_ACTOR_LABELS", False):
                _text(actors, elements[item_id].name, duplicate_box.x + duplicate_box.width / 2, duplicate_box.y + 101, "actor-label", limit=28)
    output.parent.mkdir(parents=True, exist_ok=True); ET.indent(root, space="  "); output.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True)); return output
