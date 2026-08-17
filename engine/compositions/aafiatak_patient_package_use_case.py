from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float


CANVAS = (1920, 1280)
BOUNDARY = Box(210, 120, 1500, 1100)
PACKAGE = Box(240, 180, 1440, 995)

# Presentation-only coordinates for the reviewed Patient Package diagram.
ACTORS = {
    "actor.patient": Box(725, 180, 170, 80),
}

USE_CASES = {
    "uc.puc-01": Box(290, 280, 220, 50),
    "uc.puc-02": Box(550, 280, 220, 50),
    "uc.puc-03": Box(290, 340, 220, 50),
    "uc.puc-04": Box(550, 340, 220, 50),
    "uc.puc-05": Box(290, 400, 220, 50),
    "uc.puc-06": Box(550, 400, 220, 50),
    "uc.puc-07": Box(290, 460, 220, 50),
    "uc.puc-08": Box(550, 460, 220, 50),
    "uc.puc-09": Box(290, 520, 220, 50),
    "uc.puc-10": Box(550, 520, 220, 50),
    "uc.puc-11": Box(970, 280, 210, 50),
    "uc.puc-12": Box(1215, 280, 210, 50),
    "uc.puc-13": Box(1460, 280, 160, 50),
    "uc.puc-14": Box(970, 365, 210, 50),
    "uc.puc-15": Box(1215, 365, 210, 50),
    "uc.puc-16": Box(290, 660, 220, 50),
    "uc.puc-17": Box(550, 660, 220, 50),
    "uc.puc-18": Box(290, 735, 220, 50),
    "uc.puc-19": Box(550, 735, 220, 50),
    "uc.puc-20": Box(290, 810, 220, 50),
    "uc.puc-21": Box(970, 660, 210, 50),
    "uc.puc-22": Box(1215, 660, 210, 50),
    "uc.puc-23": Box(970, 740, 210, 50),
    "uc.puc-24": Box(1215, 740, 210, 50),
    "uc.puc-25": Box(290, 980, 220, 50),
    "uc.puc-26": Box(550, 980, 220, 50),
    "uc.puc-27": Box(425, 1050, 220, 50),
    "uc.puc-28": Box(970, 940, 210, 50),
    "uc.puc-29": Box(1215, 940, 210, 50),
}

FIELDS = (
    ("Account & Discovery", Box(270, 230, 520, 350), "access"),
    ("Booking & Availability", Box(920, 230, 720, 350), "patient"),
    ("Appointment Follow-up", Box(270, 610, 520, 280), "operations"),
    ("Payment", Box(920, 610, 720, 220), "patient"),
    ("Visit & Queue Visibility", Box(270, 925, 520, 210), "facility"),
    ("Notifications", Box(920, 875, 720, 260), "platform"),
)

CASE_ROLES = {
    **{f"uc.puc-{index:02d}": "access" for index in range(1, 11)},
    **{f"uc.puc-{index:02d}": "patient" for index in range(11, 16)},
    **{f"uc.puc-{index:02d}": "operations" for index in range(16, 21)},
    **{f"uc.puc-{index:02d}": "patient" for index in range(21, 25)},
    **{f"uc.puc-{index:02d}": "facility" for index in range(25, 28)},
    **{f"uc.puc-{index:02d}": "platform" for index in range(28, 30)},
    "uc.puc-02": "helper",
    "uc.puc-12": "helper",
    "uc.puc-13": "helper",
    "uc.puc-22": "helper",
}

PATIENT_TARGETS = {
    "relation.patient-puc-01": (290, 305), "relation.patient-puc-03": (290, 365),
    "relation.patient-puc-04": (550, 365), "relation.patient-puc-05": (290, 425),
    "relation.patient-puc-06": (550, 425), "relation.patient-puc-07": (290, 485),
    "relation.patient-puc-08": (550, 485), "relation.patient-puc-09": (290, 545),
    "relation.patient-puc-10": (550, 545), "relation.patient-puc-11": (970, 305),
    "relation.patient-puc-14": (970, 390), "relation.patient-puc-15": (1215, 390),
    "relation.patient-puc-16": (290, 685), "relation.patient-puc-17": (550, 685),
    "relation.patient-puc-18": (290, 760), "relation.patient-puc-19": (550, 760),
    "relation.patient-puc-20": (290, 835), "relation.patient-puc-21": (970, 685),
    "relation.patient-puc-23": (970, 765), "relation.patient-puc-24": (1215, 765),
    "relation.patient-puc-25": (290, 1005), "relation.patient-puc-26": (550, 1005),
    "relation.patient-puc-27": (425, 1075), "relation.patient-puc-28": (970, 965),
    "relation.patient-puc-29": (1215, 965),
}

# Patient associations are intentionally a light fan behind opaque use-case nodes;
# required detail stays visible without adding false intermediate UML elements.
ROUTES = {
    **{relation_id: ((130, 662), target) for relation_id, target in PATIENT_TARGETS.items()},
    "relation.whatsapp-puc-02": ((130, 287), (550, 305)),
    "relation.map-puc-08": ((758, 92), (800, 160), (800, 485), (770, 485)),
    "relation.payment-puc-21": ((1792, 672), (1660, 620), (1180, 620), (1180, 685)),
    "relation.payment-puc-22": ((1792, 672), (1660, 640), (1425, 640), (1425, 685)),
    "relation.notification-puc-28": ((1792, 1017), (1660, 1100), (1180, 1100), (1180, 965)),
    "relation.notification-puc-29": ((1792, 1017), (1660, 1130), (1425, 1130), (1425, 965)),
    "relation.pinc-01": ((510, 305), (550, 305)),
    "relation.pinc-02": ((1180, 305), (1215, 305)),
    "relation.pinc-03": ((1180, 305), (1180, 255), (1540, 255), (1540, 280)),
    "relation.pinc-04": ((1180, 685), (1215, 685)),
    "relation.pext-01": ((1075, 660), (900, 660), (900, 250), (1075, 250), (1075, 280)),
    "relation.pext-02": ((1320, 365), (1320, 330)),
}

DEPENDENCY_LABELS = {
    "relation.pinc-01": ((530, 286), None),
    "relation.pinc-02": ((1197, 286), None),
    "relation.pinc-03": ((1360, 246), None),
    "relation.pinc-04": ((1197, 666), None),
    "relation.pext-01": ((880, 610), (830, 580)),
    "relation.pext-02": ((1340, 347), (1460, 346)),
}
