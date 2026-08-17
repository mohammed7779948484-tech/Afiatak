from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float

CANVAS = (2600, 1800)
BOUNDARY = Box(140, 140, 2320, 1600)
PACKAGE = Box(175, 195, 2250, 1500)
ACTORS = {
    "actor.booking-reception-staff": Box(1215, 205, 170, 80),
}
USE_CASES = {
    "uc.bruc-01": Box(205, 378, 250, 64),
    "uc.bruc-02": Box(470, 378, 250, 64),
    "uc.bruc-03": Box(775, 378, 250, 64),
    "uc.bruc-04": Box(1040, 378, 250, 64),
    "uc.bruc-05": Box(775, 454, 250, 64),
    "uc.bruc-06": Box(1040, 454, 250, 64),
    "uc.bruc-07": Box(775, 530, 250, 64),
    "uc.bruc-08": Box(1040, 530, 250, 64),
    "uc.bruc-09": Box(775, 606, 250, 64),
    "uc.bruc-10": Box(1345, 378, 250, 64),
    "uc.bruc-11": Box(1610, 378, 250, 64),
    "uc.bruc-12": Box(1345, 454, 250, 64),
    "uc.bruc-13": Box(1610, 454, 250, 64),
    "uc.bruc-14": Box(1895, 378, 250, 64),
    "uc.bruc-15": Box(2160, 378, 250, 64),
    "uc.bruc-16": Box(1895, 454, 250, 64),
    "uc.bruc-17": Box(205, 868, 250, 64),
    "uc.bruc-18": Box(470, 868, 250, 64),
    "uc.bruc-19": Box(205, 944, 250, 64),
    "uc.bruc-20": Box(470, 944, 250, 64),
    "uc.bruc-21": Box(205, 1020, 250, 64),
    "uc.bruc-22": Box(470, 1020, 250, 64),
    "uc.bruc-23": Box(205, 1096, 250, 64),
    "uc.bruc-24": Box(470, 1096, 250, 64),
    "uc.bruc-25": Box(205, 1172, 250, 64),
    "uc.bruc-26": Box(470, 1172, 250, 64),
    "uc.bruc-27": Box(205, 1248, 250, 64),
    "uc.bruc-28": Box(470, 1248, 250, 64),
    "uc.bruc-29": Box(205, 1324, 250, 64),
    "uc.bruc-30": Box(470, 1324, 250, 64),
    "uc.bruc-31": Box(205, 1400, 250, 64),
    "uc.bruc-32": Box(775, 868, 250, 64),
    "uc.bruc-33": Box(1040, 868, 250, 64),
    "uc.bruc-34": Box(775, 944, 250, 64),
    "uc.bruc-35": Box(1040, 944, 250, 64),
    "uc.bruc-36": Box(775, 1020, 250, 64),
    "uc.bruc-37": Box(1040, 1020, 250, 64),
    "uc.bruc-38": Box(775, 1096, 250, 64),
    "uc.bruc-39": Box(1040, 1096, 250, 64),
    "uc.bruc-40": Box(775, 1172, 250, 64),
    "uc.bruc-41": Box(1040, 1172, 250, 64),
    "uc.bruc-42": Box(775, 1248, 250, 64),
    "uc.bruc-43": Box(1040, 1248, 250, 64),
}
FIELDS = (
    ('AUTHENTICATION', Box(190, 330, 535, 164), 'access'),
    ('DAILY OPERATIONS', Box(760, 330, 535, 392), 'operations'),
    ('APPOINTMENT OPERATIONS', Box(1330, 330, 535, 240), 'patient'),
    ('CAPACITY OPERATIONS', Box(1880, 330, 535, 240), 'facility'),
    ('ARRIVAL, QUEUE & VISIT', Box(190, 820, 535, 696), 'operations'),
    ('OPERATIONAL EXCEPTIONS', Box(760, 820, 535, 544), 'facility'),
)
CASE_ROLES = {
    "uc.bruc-01": 'access',
    "uc.bruc-02": 'access',
    "uc.bruc-03": 'operations',
    "uc.bruc-04": 'operations',
    "uc.bruc-05": 'operations',
    "uc.bruc-06": 'operations',
    "uc.bruc-07": 'operations',
    "uc.bruc-08": 'operations',
    "uc.bruc-09": 'operations',
    "uc.bruc-10": 'patient',
    "uc.bruc-11": 'patient',
    "uc.bruc-12": 'patient',
    "uc.bruc-13": 'patient',
    "uc.bruc-14": 'facility',
    "uc.bruc-15": 'facility',
    "uc.bruc-16": 'facility',
    "uc.bruc-17": 'operations',
    "uc.bruc-18": 'operations',
    "uc.bruc-19": 'operations',
    "uc.bruc-20": 'operations',
    "uc.bruc-21": 'operations',
    "uc.bruc-22": 'operations',
    "uc.bruc-23": 'operations',
    "uc.bruc-24": 'operations',
    "uc.bruc-25": 'operations',
    "uc.bruc-26": 'operations',
    "uc.bruc-27": 'operations',
    "uc.bruc-28": 'operations',
    "uc.bruc-29": 'operations',
    "uc.bruc-30": 'operations',
    "uc.bruc-31": 'operations',
    "uc.bruc-32": 'facility',
    "uc.bruc-33": 'facility',
    "uc.bruc-34": 'facility',
    "uc.bruc-35": 'facility',
    "uc.bruc-36": 'facility',
    "uc.bruc-37": 'facility',
    "uc.bruc-38": 'facility',
    "uc.bruc-39": 'facility',
    "uc.bruc-40": 'facility',
    "uc.bruc-41": 'facility',
    "uc.bruc-42": 'facility',
    "uc.bruc-43": 'facility',
}
ROUTES = {}
DEPENDENCY_LABELS = {}
