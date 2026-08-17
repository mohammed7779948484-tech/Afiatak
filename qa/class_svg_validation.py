from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.models import SemanticModel, ViewSpec
from qa.diagnostics import Diagnostic


def validate_class_svg(svg_path: Path, model: SemanticModel, view: ViewSpec) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root = ET.parse(svg_path).getroot()
    classes = [node for node in root.iter() if node.attrib.get('data-kind') == 'class']
    notes = [node for node in root.iter() if node.attrib.get('data-kind') == 'note']
    relations = [node for node in root.iter() if node.attrib.get('data-kind') == 'relation']
    expected_classes = [e for e in model.elements if e.id in view.include and e.type == 'class']
    expected_notes = [e for e in model.elements if e.id in view.include and e.type == 'note']
    expected_relations = [r for r in model.relations if r.id in view.relations]
    if len(classes) != len(expected_classes):
        diagnostics.append(Diagnostic('Q4', 'class-count', f'Expected {len(expected_classes)} class boxes, found {len(classes)}'))
    if len(notes) != len(expected_notes):
        diagnostics.append(Diagnostic('Q4', 'note-count', f'Expected {len(expected_notes)} UML notes, found {len(notes)}'))
    if len(relations) != len(expected_relations):
        diagnostics.append(Diagnostic('Q4', 'relation-count', f'Expected {len(expected_relations)} relationships, found {len(relations)}'))
    rendered_class_ids = {n.attrib.get('data-semantic-id') for n in classes}
    rendered_note_ids = {n.attrib.get('data-semantic-id') for n in notes}
    rendered_relation_ids = {n.attrib.get('data-semantic-id') for n in relations}
    for item in expected_classes:
        if item.id not in rendered_class_ids:
            diagnostics.append(Diagnostic('Q4', 'missing-class', 'Class missing from SVG', subject=item.id))
    for item in expected_notes:
        if item.id not in rendered_note_ids:
            diagnostics.append(Diagnostic('Q4', 'missing-note', 'UML note missing from SVG', subject=item.id))
    for relation in expected_relations:
        if relation.id not in rendered_relation_ids:
            diagnostics.append(Diagnostic('Q4', 'missing-relation', 'Relationship missing from SVG', subject=relation.id))
    source = svg_path.read_text(encoding='utf-8')
    multiplicities = source.count('class="multiplicity"')
    if multiplicities != 2 * len(expected_relations):
        diagnostics.append(Diagnostic('Q4', 'multiplicity-count', f'Expected {2 * len(expected_relations)} multiplicities, found {multiplicities}'))
    compositions = [r for r in expected_relations if r.type == 'composition']
    aggregations = [r for r in expected_relations if r.type == 'aggregation']
    if source.count('marker-start="url(#filled-diamond)"') != len(compositions):
        diagnostics.append(Diagnostic('Q4', 'composition-diamond-count', 'Filled composition diamond count mismatch'))
    if source.count('marker-start="url(#hollow-diamond)"') != len(aggregations):
        diagnostics.append(Diagnostic('Q4', 'aggregation-diamond-count', 'Hollow aggregation diamond count mismatch'))
    if any(r.type in {'generalization', 'realization'} for r in expected_relations):
        diagnostics.append(Diagnostic('Q4', 'forbidden-inheritance', 'Generalization or realization was present'))
    return diagnostics
