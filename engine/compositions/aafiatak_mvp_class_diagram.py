from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float

CANVAS = (9000, 6364)  # A3 landscape equivalent ratio

CLASS_BOXES = {
    # Identity & Access
    'class.c01': Box(350, 650, 520, 500),
    'class.c02': Box(1000, 430, 520, 420),
    'class.c03': Box(1000, 980, 520, 470),
    'class.c04': Box(1650, 980, 520, 470),
    'class.c05': Box(1650, 430, 520, 470),
    'class.c06': Box(350, 1800, 520, 470),
    'class.c07': Box(350, 1250, 520, 430),
    # Platform reference data
    'class.c08': Box(2500, 520, 480, 400),
    'class.c09': Box(3080, 520, 480, 400),
    'class.c10': Box(3660, 520, 480, 400),
    'class.c13': Box(2600, 1120, 500, 400),
    'class.c14': Box(3250, 1120, 500, 400),
    # Facility and medical offering
    'class.c11': Box(4400, 520, 550, 470),
    'class.c12': Box(5100, 520, 550, 500),
    'class.c15': Box(5800, 1220, 550, 500),
    'class.c16': Box(6500, 1020, 620, 760),
    # Schedule and digital availability
    'class.c17': Box(4400, 2600, 550, 470),
    'class.c18': Box(5100, 2600, 550, 450),
    'class.c19': Box(5800, 2300, 650, 860),
    'class.c20': Box(6650, 2400, 600, 650),
    'class.c21': Box(7400, 2500, 520, 430),
    # Appointment and payment
    'class.c22': Box(2100, 3650, 600, 500),
    'class.c23': Box(2800, 3650, 600, 480),
    'class.c24': Box(3500, 3500, 680, 780),
    'class.c25': Box(4350, 3500, 620, 500),
    'class.c26': Box(4350, 4150, 620, 590),
    # Visit, queue, and operational exceptions
    'class.c27': Box(5250, 4400, 600, 600),
    'class.c28': Box(6000, 4500, 560, 500),
    'class.c29': Box(6700, 4300, 620, 600),
    'class.c30': Box(7500, 4450, 600, 500),
}

NOTE_BOXES = {
    'class.note-n1': Box(1700, 1700, 650, 250),
    'class.note-n2': Box(5800, 3300, 650, 210),
    'class.note-n3': Box(6550, 3250, 650, 210),
    'class.note-n4': Box(2100, 4300, 650, 240),
    'class.note-n5': Box(7300, 1050, 700, 220),
    'class.note-n6': Box(3450, 4500, 720, 210),
    'class.note-n7': Box(4350, 4850, 650, 190),
    'class.note-n8': Box(5950, 5200, 700, 220),
    'class.note-n9': Box(6700, 5150, 720, 210),
    'class.note-n10': Box(2500, 1700, 720, 210),
}

# These are visual zones only; they have no UML package semantics.
ZONES = (
    ('IDENTITY & ACCESS', Box(180, 250, 2150, 2100), '#F4F7FB'),
    ('PLATFORM & REFERENCE DATA', Box(2400, 250, 1800, 1800), '#F7F7FC'),
    ('FACILITY & MEDICAL OFFERING', Box(4250, 250, 2950, 1800), '#F8FAF5'),
    ('SCHEDULE & DIGITAL AVAILABILITY', Box(4250, 2150, 3700, 1250), '#F5FBFB'),
    ('APPOINTMENT & PAYMENT', Box(1950, 3500, 3100, 1600), '#FFFBF3'),
    ('VISIT, QUEUE & OPERATIONAL EXCEPTIONS', Box(5100, 4200, 3150, 1300), '#FCF6F6'),
)
