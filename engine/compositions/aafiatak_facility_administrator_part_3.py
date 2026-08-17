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
    "uc.fauc-29": Box(320, 300, 270, 58),
    "uc.fauc-30": Box(630, 300, 270, 58),
    "uc.fauc-31": Box(320, 415, 270, 58),
    "uc.fauc-32": Box(630, 415, 270, 58),
    "uc.fauc-33": Box(1020, 300, 270, 58),
    "uc.fauc-34": Box(1310, 300, 270, 58),
    "uc.fauc-35": Box(1020, 415, 270, 58),
    "uc.fauc-36": Box(1310, 415, 270, 58),
    "uc.fauc-37": Box(1020, 530, 270, 58),
    "uc.fauc-38": Box(1310, 530, 270, 58),
}
FIELDS = (
    ("Facility Staff Administration", Box(290, 250, 640, 300), "operations"),
    ("Operations & Oversight", Box(980, 250, 620, 420), "platform"),
)
CASE_ROLES = {
    **{f"uc.fauc-{i:02d}": "operations" for i in range(29, 33)},
    **{f"uc.fauc-{i:02d}": "platform" for i in range(33, 39)},
}
STAFF_TARGETS = {
    "relation.facility-admin-fauc-29": (320, 329),
    "relation.facility-admin-fauc-30": (630, 329),
    "relation.facility-admin-fauc-31": (320, 444),
    "relation.facility-admin-fauc-32": (630, 444),
    "relation.facility-admin-fauc-33": (1020, 329),
    "relation.facility-admin-fauc-34": (1310, 329),
    "relation.facility-admin-fauc-35": (1020, 444),
    "relation.facility-admin-fauc-36": (1310, 444),
    "relation.facility-admin-fauc-37": (1020, 559),
    "relation.facility-admin-fauc-38": (1310, 559),
}
ROUTES = {}
for relation_id, target in STAFF_TARGETS.items():
    number = int(relation_id.rsplit("-", 1)[1])
    ROUTES[relation_id] = (((110, 342) if number <= 32 else (110, 637)), target)
ROUTES.update({
    "relation.notification-fauc-38": ((1785, 612), (1660, 612), (1660, 559), (1580, 559)),
})
DEPENDENCY_LABELS = {}
