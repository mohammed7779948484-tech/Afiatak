#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from pprint import pformat

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / 'model' / 'catalog' / 'activities'
VIEW_DIR = ROOT / 'views' / 'activity'
OUT = ROOT / 'engine' / 'compositions' / 'activity_diagram_layouts_v3.py'


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def node_dimensions(kind: str, layout):
    if kind == 'action': return layout['action_width'], layout['action_height']
    if kind in {'decision', 'merge'}: return layout['decision_width'], layout['decision_height']
    if kind == 'initial': return 64, 64
    if kind == 'final': return 100, 100
    if kind == 'object': return 1100, 240
    return 0, 0


def create_layout(model, view):
    elements = {item['id']: item for item in model['elements']}
    controls = [item for item in model['relations'] if item['id'] in view['relations'] and item['type'] == 'control_flow']
    objects = [item for item in model['relations'] if item['id'] in view['relations'] and item['type'] == 'object_flow']
    initial = next(item['id'] for item in model['elements'] if item['type'] == 'initial')
    adjacency = defaultdict(list)
    merge_ids = {item['id'] for item in model['elements'] if item['type'] == 'merge'}
    final_ids = {item['id'] for item in model['elements'] if item['type'] == 'final'}
    for relation in controls:
        if relation['target'] not in merge_ids and relation['target'] not in final_ids:
            adjacency[relation['source']].append(relation['target'])
    depths = {initial: 0}; queue = deque([initial])
    while queue:
        source = queue.popleft()
        for target in adjacency[source]:
            if target not in depths:
                depths[target] = depths[source] + 1; queue.append(target)
    for index, item in enumerate(model['elements']):
        if item['id'] not in merge_ids and item['id'] not in final_ids and item['type'] not in {'object', 'note'}:
            depths.setdefault(item['id'], index + 1)
    main_max = max(depths.values())
    for merge_id in merge_ids: depths[merge_id] = main_max + 1
    for final_id in final_ids: depths[final_id] = main_max + 2
    levels = defaultdict(list)
    for item in model['elements']:
        if item['type'] not in {'note', 'object'}:
            levels[depths[item['id']]].append(item['id'])
    max_nodes = max(len(value) for value in levels.values())
    max_depth = max(levels)
    layout = {'width': max(9000, 2500 + max_nodes * 2600), 'height': max(6500, 2100 + (max_depth + 1) * 720), 'title_y': 120, 'action_width': 1900, 'action_height': 320, 'decision_width': 840, 'decision_height': 520, 'note_width': 1500, 'note_height': 280}
    frame = {'x': 220, 'y': 260, 'width': layout['width'] - 440, 'height': layout['height'] - 480}
    composition = {'frame': frame, 'initial': {}, 'actions': {}, 'objects': {}, 'decisions': {}, 'merges': {}, 'forks': {}, 'joins': {}, 'notes': {}, 'final': {}, 'routes': {}}
    centres = {}
    for level in sorted(levels):
        ids = levels[level]
        slots = len(ids)
        side_margin = 1250
        gap = (frame['width'] - side_margin * 2) / max(1, slots - 1) if slots > 1 else 0
        y = frame['y'] + 260 + level * 720
        for slot, identifier in enumerate(ids):
            item = elements[identifier]; kind = item['type']; width, height = node_dimensions(kind, layout)
            centre_x = frame['x'] + frame['width'] / 2 if slots == 1 else frame['x'] + side_margin + slot * gap
            centres[identifier] = (centre_x, y + height / 2, width, height)
            if kind == 'initial': composition['initial'][identifier] = (centre_x, y + height / 2)
            elif kind == 'final': composition['final'][identifier] = (centre_x, y + height / 2)
            elif kind == 'action': composition['actions'][identifier] = (centre_x - width / 2, y)
            elif kind == 'decision': composition['decisions'][identifier] = (centre_x - width / 2, y)
            elif kind == 'merge': composition['merges'][identifier] = (centre_x - width / 2, y)
    for index, item in enumerate(node for node in model['elements'] if node['type'] == 'note'):
        composition['notes'][item['id']] = (frame['x'] + frame['width'] - layout['note_width'] - 180, frame['y'] + 1180 + index * (layout['note_height'] + 120))
    object_links = defaultdict(dict)
    for relation in objects:
        if elements[relation['target']]['type'] == 'object': object_links[relation['target']]['before'] = relation['source']
        if elements[relation['source']]['type'] == 'object': object_links[relation['source']]['after'] = relation['target']
    for object_id, links in object_links.items():
        before, after = links.get('before'), links.get('after')
        external = elements[object_id].get('metadata', {}).get('externalInput')
        if external:
            ox, oy, _, _ = centres[after]
            # Keep an incoming object node at the visible left edge of the process frame.
            centre_x, centre_y = frame['x'] + 650, oy
        elif before and after:
            bx, by, _, _ = centres[before]; ax, ay, _, _ = centres[after]
            centre_x, centre_y = (bx + ax) / 2, (by + ay) / 2
        else:
            ox, oy, _, _ = centres[before or after]
            centre_x, centre_y = ox, oy - 430
        centres[object_id] = (centre_x, centre_y, 1100, 240)
        composition['objects'][object_id] = (centre_x - 550, centre_y - 120, 1100, 240)
    def point(identifier, direction):
        x, y, width, height = centres[identifier]
        if direction == 'top': return (x, y - height / 2)
        if direction == 'bottom': return (x, y + height / 2)
        return (x - width / 2, y) if direction == 'left' else (x + width / 2, y)
    for relation in [item for item in model['relations'] if item['id'] in view['relations']]:
        source, target = relation['source'], relation['target']
        sx, sy, _, _ = centres[source]; tx, ty, _, _ = centres[target]
        if relation['type'] == 'object_flow' and elements[source]['type'] == 'object':
            start, end = point(source, 'right'), point(target, 'left'); points = [start, (end[0] - 160, start[1]), (end[0] - 160, end[1]), end]
        elif relation['type'] == 'object_flow':
            start, end = point(source, 'bottom'), point(target, 'top'); mid = (start[1] + end[1]) / 2; points = [start, (start[0], mid), (end[0], mid), end]
        elif elements[target]['type'] == 'merge':
            start = point(source, 'bottom')
            corridor = frame['x'] + 130 if sx < frame['x'] + frame['width'] / 2 else frame['x'] + frame['width'] - 130
            end = point(target, 'left' if corridor < tx else 'right')
            points = [start, (corridor, start[1]), (corridor, end[1]), end]
        elif ty > sy:
            start, end = point(source, 'bottom'), point(target, 'top'); mid = (start[1] + end[1]) / 2; points = [start, (start[0], mid), (end[0], mid), end]
        elif abs(ty - sy) < 180:
            start, end = (point(source, 'right'), point(target, 'left')) if tx > sx else (point(source, 'left'), point(target, 'right')); points = [start, end]
        else:
            start, end = point(source, 'bottom'), point(target, 'top'); corridor = frame['x'] + 120 if tx <= sx else frame['x'] + frame['width'] - 120; points = [start, (corridor, start[1]), (corridor, end[1]), end]
        label = ((points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2 - 45)
        composition['routes'][relation['id']] = {'points': [(round(x), round(y)) for x, y in points], 'label': (round(label[0]), round(label[1]))}
    return layout, composition


def create_ad13_layout(model, view):
    """Landscape lanes for the exception workflow's semantically independent branches."""
    layout = {
        'width': 15000, 'height': 12000, 'title_y': 120,
        'action_width': 1700, 'action_height': 320,
        'decision_width': 720, 'decision_height': 520,
        'note_width': 1500, 'note_height': 280,
    }
    frame = {'x': 220, 'y': 260, 'width': 14560, 'height': 11500}
    c = {'frame': frame, 'initial': {}, 'actions': {}, 'objects': {}, 'decisions': {},
         'merges': {}, 'forks': {}, 'joins': {}, 'notes': {}, 'final': {}, 'routes': {}}
    p = 'activity.ad13.'
    def action(name, cx, y): c['actions'][p + name] = (cx - 850, y)
    def decision(name, cx, y): c['decisions'][p + name] = (cx - 360, y)
    def route(name, points, label=None):
        c['routes']['relation.ad13.' + name] = {'points': points, 'label': label or ((points[0][0] + points[1][0]) // 2, (points[0][1] + points[1][1]) // 2 - 45)}

    c['initial'][p + 'initial'] = (7500, 900)
    action('a01', 7500, 1200); action('a02', 7500, 1700)
    c['objects'][p + 'o01'] = (6950, 2150, 1100, 240)
    decision('d01', 7500, 2550)
    action('a03', 4000, 3200); action('a04', 7500, 3900); action('a05', 7500, 4350); action('a06', 7500, 4800)
    decision('d02', 7500, 5250)
    action('a07', 3300, 6000); action('a08', 7500, 6000); action('a11', 11700, 6000)
    decision('d03', 7500, 6500); action('a17', 11700, 6500)
    action('a09', 6050, 7100); action('a10', 8950, 7100); action('a12', 7500, 7700)
    decision('d04', 7500, 8200); action('a13', 7500, 8750); action('a14', 7500, 9200)
    decision('d05', 7500, 9650); action('a15', 3300, 10200); action('a16', 7500, 10200)
    c['merges'][p + 'mend'] = (7298, 10800)
    c['final'][p + 'final'] = (7500, 11450)

    route('f01', [(7500, 932), (7500, 1200)])
    route('f02', [(7500, 1520), (7500, 1700)])
    route('object30', [(7500, 2020), (7500, 2150)])
    route('object31', [(7500, 2390), (7500, 2550)])
    route('f03', [(7140, 2810), (4000, 2810), (4000, 3200)], (5450, 2765))
    route('f04', [(4000, 3520), (4000, 3740), (7500, 3740), (7500, 3900)])
    route('f05', [(7500, 3070), (7500, 3900)], (7560, 3440))
    route('f06', [(7500, 4220), (7500, 4350)])
    route('f07', [(7500, 4670), (7500, 4800)])
    route('f08', [(7500, 5120), (7500, 5250)])
    route('f09', [(7500, 5770), (3300, 5770), (3300, 6000)], (5400, 5725))
    route('f10', [(3300, 6320), (3300, 6800), (7500, 6800), (7500, 7700)])
    route('f11', [(7500, 5770), (7500, 6000)], (7560, 5835))
    route('f12', [(7500, 6320), (7500, 6500)])
    route('f13', [(7500, 7020), (6050, 7020), (6050, 7100)], (6750, 6975))
    route('f14', [(6050, 7420), (6050, 7550), (7500, 7550), (7500, 7700)])
    route('f15', [(7500, 7020), (8950, 7020), (8950, 7100)], (8250, 6975))
    route('f16', [(8950, 7420), (8950, 7550), (7500, 7550), (7500, 7700)])
    route('f17', [(7500, 5770), (11700, 5770), (11700, 6000)], (9600, 5725))
    route('f18', [(11700, 6320), (11700, 6500)])
    route('f19', [(12550, 6660), (14610, 6660), (14610, 10945), (7702, 10945)])
    route('f20', [(7500, 8020), (7500, 8200)])
    route('f21', [(7140, 8460), (450, 8460), (450, 4960), (6650, 4960)], (4450, 8415))
    route('f22', [(7500, 8720), (7500, 8750)], (7560, 8790))
    route('f23', [(7500, 9070), (7500, 9200)])
    route('f24', [(7500, 9520), (7500, 9650)])
    route('f25', [(7500, 10170), (3300, 10170), (3300, 10200)], (5400, 10125))
    route('f26', [(3300, 10520), (450, 10520), (450, 4960), (6650, 4960)])
    route('f27', [(7500, 10170), (7500, 10200)], (7560, 10245))
    route('f28', [(7500, 10520), (7500, 10800)])
    route('f29', [(7500, 11091), (7500, 11400)])
    return layout, c


def main():
    registered = {}
    for number in range(1, 17):
        nn = f'{number:02d}'
        model = load(next(MODEL_DIR.glob(f'aafiatak-ad{nn}-*.yaml')))
        view = load(next(VIEW_DIR.glob(f'aafiatak-ad{nn}-*.yaml')))
        registered[view['id']] = create_ad13_layout(model, view) if view['id'] == 'aafiatak-ad13-manage-operational-exceptions' else create_layout(model, view)
    lines = ['from __future__ import annotations', '', 'from dataclasses import dataclass', '', '@dataclass(frozen=True)', 'class ActivityLayout:', '    width: int', '    height: int', '    title_y: int', '    action_width: int', '    action_height: int', '    decision_width: int', '    decision_height: int', '    note_width: int', '    note_height: int', '', 'LAYOUTS = {}', '']
    for view_id, (layout, composition) in registered.items():
        lines.append(f"LAYOUTS[{view_id!r}] = (ActivityLayout(**{pformat(layout, width=160)}), {pformat(composition, width=180, sort_dicts=False)})")
        lines.append('')
    lines += ['def layout_for(view_id: str):', '    return LAYOUTS[view_id]', '']
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(OUT)

if __name__ == '__main__': main()
