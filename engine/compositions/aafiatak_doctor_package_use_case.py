from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float

CANVAS = (2200, 1200)
BOUNDARY = Box(100, 120, 2000, 1000)
PACKAGE = Box(135, 175, 1930, 900)
ACTORS = {
    'actor.doctor': Box(1015, 185, 170, 80),
}
USE_CASES = {
    'uc.duc-01': Box(200, 365, 260, 64),
    'uc.duc-02': Box(485, 365, 260, 64),
    'uc.duc-03': Box(850, 365, 260, 64),
    'uc.duc-04': Box(1135, 365, 260, 64),
    'uc.duc-05': Box(1460, 365, 260, 64),
    'uc.duc-06': Box(1745, 365, 260, 64),
    'uc.duc-07': Box(1460, 441, 260, 64),
    'uc.duc-08': Box(1745, 441, 260, 64),
}
FIELDS = (
    ('AUTHENTICATION', Box(170, 300, 560, 190), 'access'),
    ('APPOINTMENTS', Box(820, 300, 600, 190), 'patient'),
    ('ARRIVAL GROUPS & QUEUE', Box(1430, 300, 560, 430), 'operations'),
)
CASE_ROLES = {
    'uc.duc-01': 'access',
    'uc.duc-02': 'access',
    'uc.duc-03': 'patient',
    'uc.duc-04': 'patient',
    'uc.duc-05': 'operations',
    'uc.duc-06': 'operations',
    'uc.duc-07': 'operations',
    'uc.duc-08': 'operations',
}
ROUTES = {}
DEPENDENCY_LABELS = {}
