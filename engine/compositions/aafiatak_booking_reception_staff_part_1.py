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
    "uc.bruc-01": Box(320, 290, 220, 50),
    "uc.bruc-02": Box(570, 290, 220, 50),
    "uc.bruc-03": Box(900, 290, 230, 50),
    "uc.bruc-04": Box(1210, 290, 240, 50),
    "uc.bruc-05": Box(900, 355, 230, 50),
    "uc.bruc-06": Box(1210, 355, 240, 50),
    "uc.bruc-07": Box(900, 420, 230, 50),
    "uc.bruc-08": Box(1210, 420, 240, 50),
    "uc.bruc-09": Box(900, 485, 230, 50),
    "uc.bruc-10": Box(320, 545, 220, 50),
    "uc.bruc-11": Box(570, 545, 220, 50),
    "uc.bruc-12": Box(320, 610, 220, 50),
    "uc.bruc-13": Box(900, 650, 230, 50),
    "uc.bruc-14": Box(1210, 650, 240, 50),
    "uc.bruc-15": Box(900, 715, 230, 50),
    "uc.bruc-16": Box(1210, 715, 240, 50),
}
FIELDS = (
    ("Authentication", Box(290, 245, 520, 150), "access"),
    ("Daily Operations", Box(850, 245, 760, 315), "operations"),
    ("Capacity Operations", Box(290, 500, 520, 210), "facility"),
    ("Appointment Operations", Box(850, 605, 760, 205), "patient"),
)
CASE_ROLES = {"uc.bruc-01": "access", **{f"uc.bruc-{i:02d}": "operations" for i in range(3, 10)}, **{f"uc.bruc-{i:02d}": "facility" for i in range(10, 13)}, **{f"uc.bruc-{i:02d}": "patient" for i in range(13, 17)}, "uc.bruc-02": "helper"}
STAFF_TARGETS = {
    "relation.staff-bruc-01": (320, 315),
    "relation.staff-bruc-03": (900, 315),
    "relation.staff-bruc-04": (1210, 315),
    "relation.staff-bruc-05": (900, 380),
    "relation.staff-bruc-06": (1210, 380),
    "relation.staff-bruc-07": (900, 445),
    "relation.staff-bruc-08": (1210, 445),
    "relation.staff-bruc-09": (900, 510),
    "relation.staff-bruc-10": (320, 570),
    "relation.staff-bruc-11": (570, 570),
    "relation.staff-bruc-12": (320, 635),
    "relation.staff-bruc-13": (900, 675),
    "relation.staff-bruc-14": (1210, 675),
    "relation.staff-bruc-15": (900, 740),
    "relation.staff-bruc-16": (1210, 740),
}
ROUTES = {}
for relation_id, target in STAFF_TARGETS.items():
    number = int(relation_id.rsplit("-", 1)[1])
    ROUTES[relation_id] = (((110, 280) if number <= 9 else (110, 560) if number <= 12 else (110, 765)), target)
ROUTES.update({
    "relation.whatsapp-bruc-02": ((135, 67), (570, 315)),
    "relation.notification-bruc-09": ((1785, 512), (1130, 510)),
    "relation.brinc-01": ((540, 315), (570, 315)),
})
DEPENDENCY_LABELS = {"relation.brinc-01": ((555, 295), None)}
