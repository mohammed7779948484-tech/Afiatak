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
    "uc.fauc-01": Box(320, 280, 220, 50),
    "uc.fauc-02": Box(570, 280, 220, 50),
    "uc.fauc-03": Box(900, 280, 240, 50),
    "uc.fauc-04": Box(1210, 280, 260, 50),
    "uc.fauc-05": Box(900, 345, 240, 50),
    "uc.fauc-06": Box(1210, 345, 260, 50),
    "uc.fauc-07": Box(1055, 410, 260, 50),
    "uc.fauc-08": Box(320, 520, 240, 50),
    "uc.fauc-09": Box(610, 520, 240, 50),
    "uc.fauc-10": Box(900, 520, 240, 50),
    "uc.fauc-11": Box(1190, 520, 260, 50),
    "uc.fauc-12": Box(320, 640, 240, 50),
    "uc.fauc-13": Box(610, 640, 240, 50),
    "uc.fauc-14": Box(900, 640, 240, 50),
}
FIELDS = (
    ("Authentication", Box(290, 235, 520, 150), "access"),
    ("Facility Configuration", Box(850, 235, 720, 250), "facility"),
    ("Doctors & Services", Box(290, 470, 1280, 290), "operations"),
)
CASE_ROLES = {
    "uc.fauc-01": "access", "uc.fauc-02": "helper",
    **{f"uc.fauc-{i:02d}": "facility" for i in range(3, 8)},
    **{f"uc.fauc-{i:02d}": "operations" for i in range(8, 15)},
}
STAFF_TARGETS = {
    "relation.facility-admin-fauc-01": (320, 305),
    "relation.facility-admin-fauc-03": (900, 305),
    "relation.facility-admin-fauc-04": (1210, 305),
    "relation.facility-admin-fauc-05": (900, 370),
    "relation.facility-admin-fauc-06": (1210, 370),
    "relation.facility-admin-fauc-07": (1055, 435),
    "relation.facility-admin-fauc-08": (320, 545),
    "relation.facility-admin-fauc-09": (610, 545),
    "relation.facility-admin-fauc-10": (900, 545),
    "relation.facility-admin-fauc-11": (1190, 545),
    "relation.facility-admin-fauc-12": (320, 665),
    "relation.facility-admin-fauc-13": (610, 665),
    "relation.facility-admin-fauc-14": (900, 665),
}
ROUTES = {}
for relation_id, target in STAFF_TARGETS.items():
    number = int(relation_id.rsplit("-", 1)[1])
    ROUTES[relation_id] = (((110, 242) if number <= 7 else (110, 542) if number <= 11 else (110, 747)), target)
ROUTES.update({
    "relation.whatsapp-fauc-02": ((135, 67), (570, 305)),
    "relation.finc-01": ((540, 305), (570, 305)),
})
DEPENDENCY_LABELS = {"relation.finc-01": ((555, 285), None)}
