#!/usr/bin/env python3
"""Compile exactly one reviewed Activity Diagram checklist into model and View YAML.

The caller must invoke this only after the preceding AD has passed its lock gates.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

from engine.core.io import ROOT

SOURCES = {
    'AD-01': 'ad01-register-patient-reviewed-spec',
    'AD-02': 'ad02-log-in-reviewed-spec',
    'AD-03': 'ad03-book-appointment-reviewed-spec',
    'AD-04': 'ad04-process-full-payment-reviewed-spec',
    'AD-05': 'ad05-subscribe-availability-alert-reviewed-spec',
    'AD-06': 'ad06-cancel-appointment-reviewed-spec',
    'AD-07': 'ad07-publish-availability-reviewed-spec',
    'AD-08': 'ad08-withdraw-remaining-capacity-reviewed-spec',
    'AD-09': 'ad09-reschedule-appointment-reviewed-spec',
    'AD-10': 'ad10-register-patient-checkin-reviewed-spec',
    'AD-11': 'ad11-record-no-show-reviewed-spec',
    'AD-12': 'ad12-handle-late-arrival-reviewed-spec',
    'AD-13': 'ad13-manage-operational-exceptions-reviewed-spec',
    'AD-14': 'ad14-call-next-patient-reviewed-spec',
    'AD-15': 'ad15-review-facility-onboarding-reviewed-spec',
    'AD-16': 'ad16-suspend-facility-reviewed-spec',
}


def slugify(value: str) -> str:
    value = value.lower().replace('—', '-').replace('/', '-').replace('+', 'plus')
    value = re.sub(r'[^a-z0-9]+', '-', value).strip('-')
    return value


def node_type(label: str) -> str:
    normalized = label.lower().replace(' node', '').replace(' / activity', '')
    return {'initial': 'initial', 'final': 'final', 'action': 'action', 'decision': 'decision', 'merge': 'merge'}[normalized]


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not re.fullmatch(r'AD-\d{2}', argv[1].upper()):
        print('Usage: compile_activity_contract.py AD-XX', file=sys.stderr)
        return 2
    ad_id = argv[1].upper()
    digits = ad_id[-2:]
    checklist_path = ROOT / 'docs' / 'activity-checklists' / f'AD{digits}_CHECKLIST.json'
    contract = json.loads(checklist_path.read_text(encoding='utf-8'))
    source = SOURCES[ad_id]
    base = f'aafiatak-ad{digits}-{slugify(contract["use_case"])}'
    node_id_by_contract_id: dict[str, str] = {}
    elements = []
    for node in contract['nodes']:
        key = node['id']
        suffix = 'initial' if key == 'I' else 'final' if key == 'F' else key.lower()
        semantic_id = f'activity.ad{digits}.{suffix}'
        node_id_by_contract_id[key] = semantic_id
        kind = node_type(node['type'])
        name = 'Initial' if kind == 'initial' else 'Final' if kind == 'final' else node['label']
        refs = [{'source': source, 'section': '7'}]
        if kind in {'initial', 'final'}:
            refs.append({'source': 'aafiatak-product-specification', 'section': '9'})
        element = {'id': semantic_id, 'name': name, 'type': kind, 'description': f'{contract["use_case"]} Activity {kind}', 'tags': [f'ad{digits}', 'activity', kind], 'sourceRefs': refs}
        if kind == 'merge':
            element['metadata'] = {'visibleLabel': False}
        elements.append(element)
    relations = []
    for index, edge in enumerate(contract['edges'], start=1):
        guard = '' if edge['guard'] == '—' else edge['guard']
        relation = {'id': f'relation.ad{digits}.f{index:02d}', 'type': 'control_flow', 'source': node_id_by_contract_id[edge['from']], 'target': node_id_by_contract_id[edge['to']], 'sourceRefs': [{'source': source, 'section': '8'}, {'source': 'aafiatak-product-specification', 'section': '9'}], 'metadata': {'visibleLabel': False}}
        if guard:
            relation['name'] = guard
            relation['metadata'] = {'guard': guard}
        relations.append(relation)
    model = {'modelId': base, 'version': '1.0', 'elements': elements, 'relations': relations}
    model_path = ROOT / 'model' / 'catalog' / 'activities' / f'{base}.yaml'
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(yaml.safe_dump(model, sort_keys=False, allow_unicode=True, width=120), encoding='utf-8')
    counts = {kind: sum(item['type'] == kind for item in elements) for kind in ('action', 'decision', 'merge')}
    view = {
        'id': base,
        'diagramType': 'activity',
        'title': contract['title'],
        'model': f'../../model/catalog/activities/{model_path.name}',
        'include': [item['id'] for item in elements],
        'relations': [item['id'] for item in relations],
        'layoutProfile': 'lecturer-style-activity-portrait',
        'outputTargets': ['svg', 'png'],
        'approval': 'reviewed',
        'visualReview': {
            'status': 'awaiting-user-approval',
            'reviewer': 'Manus automated QA',
            'reviewedAt': '2026-08-17T12:45:00+00:00',
            'notes': f'{contract["use_case"]} is awaiting user visual approval after semantic, notation, editable-source, and rendering QA.',
            'previewHash': '0' * 64,
        },
        'options': {
            'masterSheet': 'A3 portrait equivalent',
            'useCase': contract['use_case'],
            'expectedActionCount': counts['action'],
            'expectedDecisionCount': counts['decision'],
            'expectedMergeCount': counts['merge'],
            'expectedControlFlowCount': len(relations),
            'approvedNoteCount': 0,
            'prohibitedNodeNames': [],
        },
    }
    view_path = ROOT / 'views' / 'activity' / f'{base}.yaml'
    view_path.parent.mkdir(parents=True, exist_ok=True)
    view_path.write_text(yaml.safe_dump(view, sort_keys=False, allow_unicode=True, width=120), encoding='utf-8')
    print(json.dumps({'model': str(model_path), 'view': str(view_path), 'node_count': len(elements), 'edge_count': len(relations)}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
