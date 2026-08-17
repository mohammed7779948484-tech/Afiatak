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
    "uc.bruc-17": Box(320, 275, 260, 54),
    "uc.bruc-18": Box(750, 275, 270, 54),
    "uc.bruc-19": Box(1180, 275, 270, 54),
    "uc.bruc-20": Box(320, 367, 260, 54),
    "uc.bruc-21": Box(1180, 367, 270, 54),
    "uc.bruc-22": Box(1180, 459, 270, 54),
    "uc.bruc-23": Box(320, 459, 260, 54),
    "uc.bruc-24": Box(750, 459, 270, 54),
    "uc.bruc-25": Box(750, 367, 270, 54),
    "uc.bruc-26": Box(320, 551, 260, 54),
    "uc.bruc-27": Box(750, 551, 270, 54),
    "uc.bruc-28": Box(1180, 551, 270, 54),
    "uc.bruc-29": Box(320, 643, 260, 54),
    "uc.bruc-30": Box(750, 643, 260, 54),
    "uc.bruc-31": Box(1180, 643, 260, 54),
}
FIELDS = (
    ("Check-in & Queue", Box(285, 235, 1320, 405), "operations"),
    ("Visit Progress", Box(285, 650, 880, 170), "facility"),
    ("Late Arrival", Box(1110, 650, 495, 170), "patient"),
)
CASE_ROLES = {**{f"uc.bruc-{i:02d}": "operations" for i in range(17, 26)}, **{f"uc.bruc-{i:02d}": "facility" for i in range(26, 30)}, **{f"uc.bruc-{i:02d}": "patient" for i in range(30, 32)}, "uc.bruc-18": "helper", "uc.bruc-19": "helper", "uc.bruc-25": "helper"}
STAFF_TARGETS = {
    "relation.staff-bruc-17": (320, 302),
    "relation.staff-bruc-18": (750, 302),
    "relation.staff-bruc-19": (1180, 302),
    "relation.staff-bruc-20": (320, 394),
    "relation.staff-bruc-21": (1180, 394),
    "relation.staff-bruc-22": (1180, 486),
    "relation.staff-bruc-23": (320, 486),
    "relation.staff-bruc-24": (750, 486),
    "relation.staff-bruc-25": (750, 394),
    "relation.staff-bruc-26": (320, 578),
    "relation.staff-bruc-27": (750, 578),
    "relation.staff-bruc-28": (1180, 578),
    "relation.staff-bruc-29": (320, 670),
    "relation.staff-bruc-30": (750, 670),
    "relation.staff-bruc-31": (1180, 670),
}
ROUTES = {}
for relation_id, target in STAFF_TARGETS.items():
    number = int(relation_id.rsplit("-", 1)[1])
    ROUTES[relation_id] = (((110, 280) if number <= 25 else (110, 560) if number <= 29 else (110, 765)), target)
ROUTES.update({
    "relation.brinc-02": ((580, 302), (750, 302)),
    "relation.brinc-03": ((580, 302), (580, 215), (1150, 215), (1180, 302)),
    "relation.brinc-04": ((580, 394), (750, 394)),
    "relation.brinc-05": ((1450, 670), (1500, 670), (1500, 850), (290, 850), (290, 302), (320, 302)),
})
DEPENDENCY_LABELS = {
    "relation.brinc-02": ((665, 283), None), "relation.brinc-03": ((880, 205), None),
    "relation.brinc-04": ((665, 375), None), "relation.brinc-05": ((900, 835), None),
}
