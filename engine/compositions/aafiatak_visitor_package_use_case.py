from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float


CANVAS = (1600, 900)
BOUNDARY = Box(150, 100, 1250, 720)
PACKAGE = Box(220, 150, 1000, 610)

ACTORS = {
    "actor.visitor": Box(635, 153, 170, 80),
}

USE_CASES = {
    "uc.vuc-01": Box(350, 250, 260, 64),
    "uc.vuc-02": Box(680, 250, 260, 64),
    "uc.vuc-03": Box(350, 330, 260, 64),
    "uc.vuc-04": Box(680, 330, 260, 64),
    "uc.vuc-05": Box(470, 510, 260, 64),
    "uc.vuc-06": Box(800, 510, 260, 64),
    "uc.vuc-07": Box(635, 620, 260, 64),
}

FIELDS = (
    ("Discovery", Box(300, 210, 700, 220), "access"),
    ("Access", Box(420, 470, 690, 230), "patient"),
)

CASE_ROLES = {
    "uc.vuc-01": "access",
    "uc.vuc-02": "access",
    "uc.vuc-03": "access",
    "uc.vuc-04": "access",
    "uc.vuc-05": "patient",
    "uc.vuc-06": "patient",
    "uc.vuc-07": "helper",
}

ROUTES = {
    "relation.visitor-vuc-01": ((95, 462), (350, 282)),
    "relation.visitor-vuc-02": ((95, 462), (680, 282)),
    "relation.visitor-vuc-03": ((95, 462), (350, 362)),
    "relation.visitor-vuc-04": ((95, 462), (680, 362)),
    "relation.visitor-vuc-05": ((95, 462), (470, 542)),
    "relation.visitor-vuc-06": ((95, 462), (800, 542)),
    "relation.map-vuc-04": ((1485, 352), (1350, 352), (1350, 362), (940, 362)),
    "relation.whatsapp-vuc-07": ((1485, 632), (1350, 632), (1350, 652), (895, 652)),
    "relation.vinc-01": ((600, 574), (710, 600), (765, 600), (765, 620)),
    "relation.vinc-02": ((930, 574), (820, 600), (765, 600), (765, 620)),
}

DEPENDENCY_LABELS = {
    "relation.vinc-01": ((642, 596), None),
    "relation.vinc-02": ((888, 596), None),
}
