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
    "actor.booking-reception-staff": Box(875, 180, 170, 80),
}
USE_CASES = {
    "uc.bruc-32": Box(320, 285, 270, 58),
    "uc.bruc-33": Box(750, 285, 270, 58),
    "uc.bruc-34": Box(1180, 285, 270, 58),
    "uc.bruc-35": Box(320, 390, 270, 58),
    "uc.bruc-36": Box(750, 390, 270, 58),
    "uc.bruc-37": Box(1180, 390, 270, 58),
    "uc.bruc-38": Box(320, 495, 270, 58),
    "uc.bruc-39": Box(750, 495, 270, 58),
    "uc.bruc-40": Box(1180, 495, 270, 58),
    "uc.bruc-41": Box(320, 600, 270, 58),
    "uc.bruc-42": Box(750, 600, 270, 58),
    "uc.bruc-43": Box(1180, 600, 270, 58),
}
FIELDS = (("Operational Exceptions", Box(285, 235, 1320, 560), "doctor"),)
CASE_ROLES = {**{f"uc.bruc-{i:02d}": "doctor" for i in range(32, 39)}, **{f"uc.bruc-{i:02d}": "operations" for i in range(40, 44)}, "uc.bruc-39": "platform"}
STAFF_TARGETS = {
    "relation.staff-bruc-32": (320, 314),
    "relation.staff-bruc-33": (750, 314),
    "relation.staff-bruc-34": (1180, 314),
    "relation.staff-bruc-35": (320, 419),
    "relation.staff-bruc-36": (750, 419),
    "relation.staff-bruc-37": (1180, 419),
    "relation.staff-bruc-38": (320, 524),
    "relation.staff-bruc-39": (750, 524),
    "relation.staff-bruc-40": (1180, 524),
    "relation.staff-bruc-41": (320, 629),
    "relation.staff-bruc-42": (750, 629),
    "relation.staff-bruc-43": (1180, 629),
}
ROUTES = {}
for relation_id, target in STAFF_TARGETS.items():
    number = int(relation_id.rsplit("-", 1)[1])
    ROUTES[relation_id] = (((110, 280) if number <= 37 else (110, 560) if number <= 40 else (110, 765)), target)
ROUTES.update({
    "relation.notification-bruc-39": ((1785, 612), (1600, 612), (1600, 425), (1020, 524)),
})
DEPENDENCY_LABELS = {}
