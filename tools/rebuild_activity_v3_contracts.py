#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = ROOT / 'build' / 'work' / 'activity-v3-specs'
MODEL_DIR = ROOT / 'model' / 'catalog' / 'activities'
VIEW_DIR = ROOT / 'views' / 'activity'

NODE_RE = re.compile(r"^- `(?P<code>[A-Z]\d\d|D\d\d|I|F|MEND)` — \*\*(?P<kind>[^*:]+):\*\* (?P<name>.+)$")
LABEL_RE = re.compile(r"^\| `(?P<code>[A-Z]\d\d|D\d\d)` \| [^|]+ \| `(?P<label>.+)` \|$")
EDGE_RE = re.compile(r"^\| `(?P<src>[A-Z]\d\d|D\d\d|I|F|MEND)` \| `(?P<tgt>[A-Z]\d\d|D\d\d|I|F|MEND)` \| (?P<guard>[^|]+) \|")
OBJECTS = {
    '04': [('O01', 'PaymentIntent', 'A01', 'A02', False)],
    '13': [('O01', 'OperationalException', 'A02', 'D01', False)],
    '15': [('O01', 'FacilityOnboardingRequest', None, 'A01', True)],
}
NOTES = {
    '04': [('receipt', 'Patient receipt is evidence for verification/escalation only; ordinary facility users cannot overwrite PaymentIntent truth.')],
}


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def dump(path: Path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000), encoding='utf-8')


def code_for_element(identifier: str) -> str | None:
    suffix = identifier.rsplit('.', 1)[-1]
    if suffix == 'initial': return 'I'
    if suffix == 'final': return 'F'
    if suffix == 'mend': return 'MEND'
    return suffix.upper() if re.fullmatch(r'[ad]\d\d', suffix) else None


def parse_spec(path: Path):
    text = path.read_text(encoding='utf-8')
    title = re.search(r'^# Activity Diagram — (?P<title>.+)$', text, re.M).group('title').strip()
    nodes, labels, edges = {}, {}, []
    in_inventory = False
    in_edges = False
    for line in text.splitlines():
        if line.startswith('## 7. Exact Node Inventory'): in_inventory = True; in_edges = False
        elif line.startswith('## 7A.'): in_inventory = False
        elif line.startswith('## 8. Exact Control-Flow'): in_edges = True
        elif line.startswith('## 9.'): in_edges = False
        if in_inventory:
            match = NODE_RE.match(line)
            if match: nodes[match['code']] = (match['kind'].strip().lower().replace(' ', '_'), match['name'].strip())
        match = LABEL_RE.match(line)
        if match: labels[match['code']] = match['label'].strip()
        if in_edges:
            match = EDGE_RE.match(line)
            if match:
                guard = match['guard'].strip()
                edges.append((match['src'], match['tgt'], None if guard == '—' else guard))
    return title, nodes, labels, edges


def main():
    for number in range(1, 17):
        nn = f'{number:02d}'
        spec = next(SPEC_DIR.glob(f'Aafiatak_AD{nn}_*_v3.md'))
        title, nodes, labels, edges = parse_spec(spec)
        model_path = next(MODEL_DIR.glob(f'aafiatak-ad{nn}-*.yaml'))
        view_path = next(VIEW_DIR.glob(f'aafiatak-ad{nn}-*.yaml'))
        model, view = load(model_path), load(view_path)
        prefix = f'activity.ad{nn}'
        by_code = {}
        retained = []
        for element in model['elements']:
            if element['type'] == 'note':
                continue
            code = code_for_element(element['id'])
            if code in nodes:
                node_kind, semantic_name = nodes[code]
                kind_map = {'initial_node': 'initial', 'final_node': 'final', 'action': 'action', 'decision': 'decision', 'merge': 'merge'}
                element['type'] = kind_map.get(node_kind, element['type'])
                element['name'] = semantic_name
                element.setdefault('metadata', {})
                if code in labels: element['metadata']['visibleLabel'] = labels[code]
                elif element['type'] == 'merge': element['metadata']['visibleLabel'] = False
                by_code[code] = element['id']
                retained.append(element)
        for code, label, source, target, external in OBJECTS.get(nn, []):
            object_id = f'{prefix}.o01'
            by_code[code] = object_id
            retained.append({
                'id': object_id, 'name': label, 'type': 'object', 'description': f'{title} required Object Node',
                'tags': [f'ad{nn}', 'activity', 'object'],
                'sourceRefs': [{'source': 'aafiatak-product-specification', 'section': '7B'}],
                'metadata': {'visibleLabel': label, **({'externalInput': True} if external else {})},
            })
        for note_id, note_text in NOTES.get(nn, []):
            retained.append({
                'id': f'{prefix}.note-{note_id}', 'name': note_text, 'type': 'note', 'description': f'{title} source-supported lecturer note',
                'tags': [f'ad{nn}', 'activity', 'note'], 'sourceRefs': [{'source': 'aafiatak-product-specification', 'section': '9'}],
                'metadata': {'visibleLabel': note_text},
            })
        model['elements'] = retained
        relations = []
        count = 1
        for source, target, guard in edges:
            if source not in by_code or target not in by_code:
                raise ValueError(f'Unknown edge token in AD-{nn}: {source}->{target}')
            relations.append({
                'id': f'relation.ad{nn}.f{count:02d}', 'type': 'control_flow', 'source': by_code[source], 'target': by_code[target],
                'sourceRefs': [{'source': 'aafiatak-product-specification', 'section': '8'}],
                'metadata': {'visibleLabel': bool(guard), **({'guard': guard} if guard else {})},
                **({'name': guard} if guard else {}),
            })
            count += 1
        for code, label, source, target, external in OBJECTS.get(nn, []):
            object_id = by_code[code]
            if source:
                relations.append({'id': f'relation.ad{nn}.object{count:02d}', 'type': 'object_flow', 'source': by_code[source], 'target': object_id, 'sourceRefs': [{'source': 'aafiatak-product-specification', 'section': '8A'}], 'metadata': {'visibleLabel': False}}); count += 1
            relations.append({'id': f'relation.ad{nn}.object{count:02d}', 'type': 'object_flow', 'source': object_id, 'target': by_code[target], 'sourceRefs': [{'source': 'aafiatak-product-specification', 'section': '8A'}], 'metadata': {'visibleLabel': False}}); count += 1
        model['relations'] = relations
        model['version'] = '3.0'
        view['title'] = f'Activity Diagram — {title}'
        view['include'] = [element['id'] for element in model['elements']]
        view['relations'] = [relation['id'] for relation in relations]
        view.setdefault('options', {})['useCase'] = title
        view['options']['v3Spec'] = spec.name
        view['options']['approvedNoteCount'] = len(NOTES.get(nn, []))
        view['approval'] = 'reviewed'
        view.setdefault('visualReview', {})['status'] = 'awaiting-user-approval'
        view['visualReview'].setdefault('previewHash', '0' * 64)
        dump(model_path, model); dump(view_path, view)
        print(f'AD-{nn}: {model_path.name}')


if __name__ == '__main__':
    main()
