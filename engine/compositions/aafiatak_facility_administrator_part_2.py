from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float

CANVAS = (1920, 1080)
BOUNDARY = Box(220, 120, 1480, 900)
PACKAGE = Box(250, 180, 1420, 790)

ACTORS = {
    "actor.facility-administrator": Box(875, 180, 170, 80),
}
USE_CASES = {
    "uc.fauc-15": Box(320, 285, 220, 54),
    "uc.fauc-16": Box(570, 285, 220, 54),
    "uc.fauc-17": Box(320, 380, 220, 54),
    "uc.fauc-18": Box(570, 380, 220, 54),
    "uc.fauc-19": Box(900, 285, 260, 54),
    "uc.fauc-20": Box(1210, 285, 260, 54),
    "uc.fauc-21": Box(900, 380, 260, 54),
    "uc.fauc-22": Box(1210, 380, 260, 54),
    "uc.fauc-23": Box(900, 475, 260, 54),
    "uc.fauc-24": Box(1210, 475, 260, 54),
    "uc.fauc-25": Box(900, 570, 260, 54),
    "uc.fauc-26": Box(1210, 570, 260, 54),
    "uc.fauc-27": Box(900, 665, 260, 54),
    "uc.fauc-28": Box(1210, 665, 260, 54),
}
FIELDS = (
    ("Policies", Box(290, 240, 520, 250), "patient"),
    ("Schedules & Digital Availability", Box(850, 240, 720, 540), "facility"),
)
CASE_ROLES = {
    **{f"uc.fauc-{i:02d}": "patient" for i in range(15, 19)},
    **{f"uc.fauc-{i:02d}": "facility" for i in range(19, 29)},
}
STAFF_TARGETS = {
    "relation.facility-admin-fauc-15": (320, 312),
    "relation.facility-admin-fauc-16": (570, 312),
    "relation.facility-admin-fauc-17": (320, 407),
    "relation.facility-admin-fauc-18": (570, 407),
    "relation.facility-admin-fauc-19": (900, 312),
    "relation.facility-admin-fauc-20": (1210, 312),
    "relation.facility-admin-fauc-21": (900, 407),
    "relation.facility-admin-fauc-22": (1210, 407),
    "relation.facility-admin-fauc-23": (900, 502),
    "relation.facility-admin-fauc-24": (1210, 502),
    "relation.facility-admin-fauc-25": (900, 597),
    "relation.facility-admin-fauc-26": (1210, 597),
    "relation.facility-admin-fauc-27": (900, 692),
    "relation.facility-admin-fauc-28": (1210, 692),
}
ROUTES = {}
for relation_id, target in STAFF_TARGETS.items():
    number = int(relation_id.rsplit("-", 1)[1])
    ROUTES[relation_id] = (((110, 272) if number <= 18 else (110, 597)), target)
ROUTES["relation.facility-admin-fauc-26"] = ((110, 613), (110, 760), (1500, 760), (1500, 597), (1210, 597))
DEPENDENCY_LABELS = {}
