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
    "actor.facility-administrator": Box(1215, 205, 170, 80),
}
USE_CASES = {
    "uc.fauc-01": Box(205, 378, 250, 64),
    "uc.fauc-02": Box(470, 378, 250, 64),
    "uc.fauc-03": Box(775, 378, 250, 64),
    "uc.fauc-04": Box(1040, 378, 250, 64),
    "uc.fauc-05": Box(775, 454, 250, 64),
    "uc.fauc-06": Box(1040, 454, 250, 64),
    "uc.fauc-07": Box(775, 530, 250, 64),
    "uc.fauc-08": Box(1345, 378, 250, 64),
    "uc.fauc-09": Box(1610, 378, 250, 64),
    "uc.fauc-10": Box(1345, 454, 250, 64),
    "uc.fauc-11": Box(1610, 454, 250, 64),
    "uc.fauc-12": Box(1345, 530, 250, 64),
    "uc.fauc-13": Box(1610, 530, 250, 64),
    "uc.fauc-14": Box(1345, 606, 250, 64),
    "uc.fauc-15": Box(1895, 378, 250, 64),
    "uc.fauc-16": Box(2160, 378, 250, 64),
    "uc.fauc-17": Box(1895, 454, 250, 64),
    "uc.fauc-18": Box(2160, 454, 250, 64),
    "uc.fauc-19": Box(205, 868, 250, 64),
    "uc.fauc-20": Box(470, 868, 250, 64),
    "uc.fauc-21": Box(205, 944, 250, 64),
    "uc.fauc-22": Box(470, 944, 250, 64),
    "uc.fauc-23": Box(205, 1020, 250, 64),
    "uc.fauc-24": Box(470, 1020, 250, 64),
    "uc.fauc-25": Box(205, 1096, 250, 64),
    "uc.fauc-26": Box(470, 1096, 250, 64),
    "uc.fauc-27": Box(205, 1172, 250, 64),
    "uc.fauc-28": Box(470, 1172, 250, 64),
    "uc.fauc-29": Box(775, 868, 250, 64),
    "uc.fauc-30": Box(1040, 868, 250, 64),
    "uc.fauc-31": Box(775, 944, 250, 64),
    "uc.fauc-32": Box(1040, 944, 250, 64),
    "uc.fauc-33": Box(1345, 868, 250, 64),
    "uc.fauc-34": Box(1610, 868, 250, 64),
    "uc.fauc-35": Box(1345, 944, 250, 64),
    "uc.fauc-36": Box(1610, 944, 250, 64),
    "uc.fauc-37": Box(1345, 1020, 250, 64),
    "uc.fauc-38": Box(1610, 1020, 250, 64),
}
FIELDS = (
    ('AUTHENTICATION', Box(190, 330, 535, 164), 'access'),
    ('FACILITY CONFIGURATION', Box(760, 330, 535, 316), 'facility'),
    ('DOCTORS & SERVICES', Box(1330, 330, 535, 392), 'doctor'),
    ('POLICIES', Box(1880, 330, 535, 240), 'patient'),
    ('SCHEDULES & DIGITAL AVAILABILITY', Box(190, 820, 535, 468), 'facility'),
    ('FACILITY STAFF ADMINISTRATION', Box(760, 820, 535, 240), 'operations'),
    ('OPERATIONS & OVERSIGHT', Box(1330, 820, 535, 316), 'platform'),
)
CASE_ROLES = {
    "uc.fauc-01": 'access',
    "uc.fauc-02": 'access',
    "uc.fauc-03": 'facility',
    "uc.fauc-04": 'facility',
    "uc.fauc-05": 'facility',
    "uc.fauc-06": 'facility',
    "uc.fauc-07": 'facility',
    "uc.fauc-08": 'doctor',
    "uc.fauc-09": 'doctor',
    "uc.fauc-10": 'doctor',
    "uc.fauc-11": 'doctor',
    "uc.fauc-12": 'doctor',
    "uc.fauc-13": 'doctor',
    "uc.fauc-14": 'doctor',
    "uc.fauc-15": 'patient',
    "uc.fauc-16": 'patient',
    "uc.fauc-17": 'patient',
    "uc.fauc-18": 'patient',
    "uc.fauc-19": 'facility',
    "uc.fauc-20": 'facility',
    "uc.fauc-21": 'facility',
    "uc.fauc-22": 'facility',
    "uc.fauc-23": 'facility',
    "uc.fauc-24": 'facility',
    "uc.fauc-25": 'facility',
    "uc.fauc-26": 'facility',
    "uc.fauc-27": 'facility',
    "uc.fauc-28": 'facility',
    "uc.fauc-29": 'operations',
    "uc.fauc-30": 'operations',
    "uc.fauc-31": 'operations',
    "uc.fauc-32": 'operations',
    "uc.fauc-33": 'platform',
    "uc.fauc-34": 'platform',
    "uc.fauc-35": 'platform',
    "uc.fauc-36": 'platform',
    "uc.fauc-37": 'platform',
    "uc.fauc-38": 'platform',
}
ROUTES = {}
DEPENDENCY_LABELS = {}
