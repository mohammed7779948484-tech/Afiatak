from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.aafiatak_patient_package_use_case import (
    ACTORS,
    BOUNDARY,
    CANVAS,
    CASE_ROLES,
    DEPENDENCY_LABELS,
    FIELDS,
    PACKAGE,
    ROUTES,
    USE_CASES,
)
from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticModel, ViewSpec
from engine.svg.use_case import (
    SVG,
    _actor,
    _bounds_attributes,
    _css,
    _path_data,
    _points_data,
    _tag,
    _text,
    _use_case,
)


def render_patient_package_use_case_svg(model: SemanticModel, view: ViewSpec, output: Path) -> Path:
    if view.id != "aafiatak-patient-package-use-case":
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
    description.text = "Detailed UML Patient Package Use Case Diagram for the Aafiatak medical appointment booking system."
    defs = ET.SubElement(root, _tag("defs"))
    style = ET.SubElement(defs, _tag("style"))
    style.text = _css(theme) + f"""
    .package {{ fill: none; stroke: {theme['colors']['boundary']}; stroke-width: 1.8; }}
    .package-tab {{ fill: {theme['colors']['field']}; stroke: {theme['colors']['boundary']}; stroke-width: 1.8; }}
    .helper {{ fill: {theme['colors']['helper']}; }}
    """
    marker = ET.SubElement(
        defs,
        _tag("marker"),
        {"id": "dependency-arrow", "viewBox": "0 0 10 10", "refX": "9", "refY": "5", "markerWidth": "8", "markerHeight": "8", "orient": "auto-start-reverse"},
    )
    ET.SubElement(marker, _tag("path"), {"d": "M 0 0 L 10 5 L 0 10", "fill": "none", "stroke": theme["colors"]["dependency"], "stroke-width": "1.4"})
    ET.SubElement(root, _tag("rect"), {"width": str(CANVAS[0]), "height": str(CANVAS[1]), "fill": theme["canvas"]["background"]})
    _text(root, view.title, CANVAS[0] / 2, 48, "page-title", limit=84)

    ET.SubElement(root, _tag("rect"), {"x": str(BOUNDARY.x), "y": str(BOUNDARY.y), "width": str(BOUNDARY.width), "height": str(BOUNDARY.height), "rx": "4", "class": "boundary", "id": "system-boundary", **_bounds_attributes(BOUNDARY)})
    _text(root, view.options.get("systemName", "Aafiatak"), BOUNDARY.x + 24, BOUNDARY.y + 31, "boundary-title", limit=80)

    package_group = ET.SubElement(root, _tag("g"), {"aria-label": "Patient Package UML container"})
    package_path = f"M {PACKAGE.x:g} {PACKAGE.y + 24:g} H {PACKAGE.x + 220:g} V {PACKAGE.y:g} H {PACKAGE.x + PACKAGE.width:g} V {PACKAGE.y + PACKAGE.height:g} H {PACKAGE.x:g} Z"
    ET.SubElement(package_group, _tag("path"), {"id": "patient-package", "d": package_path, "class": "package", **_bounds_attributes(PACKAGE)})
    ET.SubElement(package_group, _tag("rect"), {"x": str(PACKAGE.x), "y": str(PACKAGE.y), "width": "220", "height": "34", "class": "package-tab"})
    _text(package_group, view.options.get("packageName", "Patient Package"), PACKAGE.x + 110, PACKAGE.y + 22, "boundary-title", limit=32)

    field_group = ET.SubElement(root, _tag("g"), {"aria-label": "Presentation-only Patient Package neighborhoods"})
    accent_by_role = {key: theme["colors"][key] for key in ("access", "patient", "facility", "operations", "platform")}
    for label, box, role in FIELDS:
        ET.SubElement(field_group, _tag("rect"), {"x": str(box.x), "y": str(box.y), "width": str(box.width), "height": str(box.height), "rx": "18", "class": "field"})
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

    node_group = ET.SubElement(root, _tag("g"), {"aria-label": "Patient Package use cases"})
    for item_id, box in USE_CASES.items():
        _use_case(node_group, elements[item_id], box, CASE_ROLES[item_id])
    actor_group = ET.SubElement(root, _tag("g"), {"aria-label": "Actors outside the system boundary"})
    for item_id, box in ACTORS.items():
        _actor(actor_group, elements[item_id], box)

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="  ")
    output.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
    return output
