#!/usr/bin/env python3
"""Audit one Activity Diagram model/view against its generated authoritative checklist."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from PIL import Image

from engine.core.io import ROOT


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('Usage: audit_activity_diagram.py <AD-XX>', file=sys.stderr)
        return 2
    diagram_id = argv[1].upper()
    if not diagram_id.startswith('AD-'):
        print('Diagram ID must use AD-XX form', file=sys.stderr)
        return 2
    digits = diagram_id.replace('AD-', '')
    checklist_path = ROOT / 'docs' / 'activity-checklists' / f'AD{digits}_CHECKLIST.json'
    model_path = ROOT / 'model' / 'catalog' / 'activities' / f'aafiatak-ad{digits}-' 
    candidates = sorted((ROOT / 'model' / 'catalog' / 'activities').glob(f'aafiatak-ad{digits}-*.yaml'))
    views = sorted((ROOT / 'views' / 'activity').glob(f'aafiatak-ad{digits}-*.yaml'))
    if len(candidates) != 1 or len(views) != 1:
        raise SystemExit(f'Expected exactly one model and View for {diagram_id}')
    checklist = json.loads(checklist_path.read_text(encoding='utf-8'))
    model = yaml.safe_load(candidates[0].read_text(encoding='utf-8'))
    view = yaml.safe_load(views[0].read_text(encoding='utf-8'))
    errors: list[str] = []

    expected_nodes = {item['id']: item for item in checklist['nodes']}
    actual_nodes = {item['id'].split('.')[-1].upper() if item['id'].split('.')[-1] != 'initial' and item['id'].split('.')[-1] != 'final' else ('I' if item['id'].endswith('.initial') else 'F'): item for item in model['elements'] if item['type'] != 'note'}
    aliases = {'MEND': 'mend'}
    actual_nodes = {}
    for item in model['elements']:
        if item['type'] == 'note':
            continue
        suffix = item['id'].split('.')[-1]
        key = 'I' if suffix == 'initial' else 'F' if suffix == 'final' else suffix.upper()
        actual_nodes[key] = item
    if set(actual_nodes) != set(expected_nodes):
        fail(errors, f'Node IDs mismatch: expected {sorted(expected_nodes)}, got {sorted(actual_nodes)}')
    for key, expected in expected_nodes.items():
        actual = actual_nodes.get(key)
        if not actual:
            continue
        expected_type = expected['type'].lower().replace(' node', '').replace(' / activity', '').replace('activity', 'action')
        type_map = {'initial': 'initial', 'final': 'final', 'action': 'action', 'decision': 'decision', 'merge': 'merge'}
        if actual['type'] != type_map.get(expected_type, expected_type):
            fail(errors, f'{key}: expected type {expected_type}, got {actual["type"]}')
        if key not in {'I', 'F', 'MEND'} and actual['name'] != expected['label']:
            fail(errors, f'{key}: name differs from checklist')

    expected_edges = checklist['edges']
    if len(model['relations']) != len(expected_edges):
        fail(errors, f'Control-flow count mismatch: expected {len(expected_edges)}, got {len(model["relations"])}')
    element_key_by_id = {}
    for key, item in actual_nodes.items():
        element_key_by_id[item['id']] = key
    actual_edges = [(element_key_by_id.get(rel['source']), element_key_by_id.get(rel['target']), rel.get('name', '')) for rel in model['relations']]
    expected_edge_values = [(edge['from'], edge['to'], '' if edge['guard'] == '—' else edge['guard']) for edge in expected_edges]
    if actual_edges != expected_edge_values:
        fail(errors, 'Control-flow order/endpoints/guards differ from authoritative Edge Table')
    for rel in model['relations']:
        source = next(item for item in model['elements'] if item['id'] == rel['source'])
        if source['type'] == 'decision' and not rel.get('name'):
            fail(errors, f'Decision flow {rel["id"]} lacks a guard')
    if any(item['type'] in {'fork', 'join'} for item in model['elements']):
        fail(errors, 'Unsupported Fork/Join rendered')
    if view['title'] != checklist['title']:
        fail(errors, 'View title differs from exact MD title')
    if view['visualReview']['status'] != 'awaiting-user-approval':
        fail(errors, 'Visual review status must remain awaiting-user-approval')
    if set(view['include']) != {item['id'] for item in model['elements']}:
        fail(errors, 'View include set differs from model element set')
    if set(view['relations']) != {item['id'] for item in model['relations']}:
        fail(errors, 'View relation set differs from model relation set')
    preview = ROOT / 'build' / 'preview' / f'{view["id"]}.png'
    if preview.exists():
        with Image.open(preview) as image:
            if image.width < 3000 or image.height < 3000:
                fail(errors, f'PNG preview unexpectedly small: {image.size}')
    else:
        fail(errors, 'PNG preview missing')
    result = {'diagram': diagram_id, 'result': 'pass' if not errors else 'fail', 'errors': errors, 'checklist': str(checklist_path.relative_to(ROOT)), 'model': str(candidates[0].relative_to(ROOT)), 'view': str(views[0].relative_to(ROOT))}
    output = ROOT / 'build' / 'qa' / f'{view["id"]}-semantic-audit.json'
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
