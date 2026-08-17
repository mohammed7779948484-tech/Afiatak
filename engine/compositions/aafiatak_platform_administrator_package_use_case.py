from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float

CANVAS = (2800, 1900)
BOUNDARY = Box(100, 120, 2600, 1700)
PACKAGE = Box(135, 175, 2530, 1600)
ACTORS = {
    'actor.platform-administrator': Box(1315, 185, 170, 80),
}
USE_CASES = {
    'uc.pauc-01': Box(200, 365, 260, 64),
    'uc.pauc-02': Box(485, 365, 260, 64),
    'uc.pauc-03': Box(790, 365, 290, 64),
    'uc.pauc-04': Box(1105, 365, 290, 64),
    'uc.pauc-05': Box(790, 441, 290, 64),
    'uc.pauc-06': Box(1105, 441, 290, 64),
    'uc.pauc-07': Box(790, 517, 290, 64),
    'uc.pauc-08': Box(1105, 517, 290, 64),
    'uc.pauc-09': Box(790, 593, 290, 64),
    'uc.pauc-10': Box(1770, 365, 300, 64),
    'uc.pauc-11': Box(2095, 365, 300, 64),
    'uc.pauc-12': Box(1770, 441, 300, 64),
    'uc.pauc-13': Box(2095, 441, 300, 64),
    'uc.pauc-14': Box(200, 965, 300, 64),
    'uc.pauc-15': Box(1000, 965, 350, 64),
    'uc.pauc-16': Box(1380, 965, 350, 64),
    'uc.pauc-17': Box(1000, 1041, 350, 64),
    'uc.pauc-18': Box(1380, 1041, 350, 64),
    'uc.pauc-19': Box(1000, 1117, 350, 64),
    'uc.pauc-20': Box(1380, 1117, 350, 64),
}
FIELDS = (
    ('AUTHENTICATION', Box(175, 300, 500, 190), 'access'),
    ('FACILITY ONBOARDING', Box(760, 300, 930, 560), 'facility'),
    ('PLATFORM REFERENCE DATA', Box(1740, 300, 850, 350), 'patient'),
    ('PLATFORM STAFF', Box(175, 900, 720, 220), 'operations'),
    ('SUPPORT & OVERSIGHT', Box(970, 900, 1620, 500), 'platform'),
)
CASE_ROLES = {
    'uc.pauc-01': 'access',
    'uc.pauc-02': 'access',
    'uc.pauc-03': 'facility',
    'uc.pauc-04': 'facility',
    'uc.pauc-05': 'facility',
    'uc.pauc-06': 'facility',
    'uc.pauc-07': 'facility',
    'uc.pauc-08': 'facility',
    'uc.pauc-09': 'facility',
    'uc.pauc-10': 'patient',
    'uc.pauc-11': 'patient',
    'uc.pauc-12': 'patient',
    'uc.pauc-13': 'patient',
    'uc.pauc-14': 'operations',
    'uc.pauc-15': 'platform',
    'uc.pauc-16': 'platform',
    'uc.pauc-17': 'platform',
    'uc.pauc-18': 'platform',
    'uc.pauc-19': 'platform',
    'uc.pauc-20': 'platform',
}
ROUTES = {}
DEPENDENCY_LABELS = {}
