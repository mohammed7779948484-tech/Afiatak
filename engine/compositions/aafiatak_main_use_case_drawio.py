from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def cx(self) -> float:
        return self.x + self.width / 2

    @property
    def cy(self) -> float:
        return self.y + self.height / 2


@dataclass(frozen=True)
class Route:
    exit_x: float
    exit_y: float
    entry_x: float
    entry_y: float
    waypoints: tuple[tuple[float, float], ...] = ()


CANVAS = (3000, 1750)
BOUNDARY = Box(400, 240, 2200, 1210)
TITLE = Box(470, 260, 2060, 70)

ACTORS = {
    # Human actors
    "actor.visitor": Box(70, 380, 240, 140),
    "actor.facility-administrator": Box(50, 940, 290, 150),
    "actor.patient": Box(2700, 380, 230, 140),
    "actor.booking-reception-staff": Box(1250, 1530, 500, 160),
    "actor.doctor": Box(1900, 1530, 260, 160),
    "actor.platform-administrator": Box(2640, 1280, 330, 160),
    # External systems: kept outside the top edge directly above their related
    # use cases to minimize long cross-diagram routes.
    "actor.map-service": Box(520, 50, 300, 120),
    "actor.whatsapp-auth-provider": Box(880, 50, 390, 120),
    "actor.payment-gateway": Box(1530, 50, 320, 120),
    "actor.notification-service": Box(2050, 50, 340, 120),
}

USE_CASES = {
    # Access & Identity
    "uc.muc-01": Box(500, 390, 260, 80),
    "uc.muc-02": Box(800, 390, 260, 80),
    "uc.muc-03": Box(500, 550, 260, 80),
    "uc.muc-04": Box(1050, 550, 260, 80),  # shared identity hub
    "uc.muc-05": Box(760, 690, 260, 80),
    # Patient Services
    "uc.muc-06": Box(1430, 390, 280, 80),
    "uc.muc-09": Box(1780, 390, 280, 80),
    "uc.muc-11": Box(2130, 390, 300, 80),
    "uc.muc-12": Box(1430, 570, 300, 80),
    "uc.muc-13": Box(1790, 570, 280, 80),
    "uc.muc-14": Box(2140, 570, 300, 80),
    # Facility Administration
    "uc.muc-15": Box(510, 920, 270, 80),
    "uc.muc-16": Box(820, 920, 290, 80),
    # Care & Facility Operations — shared operations are deliberately central.
    "uc.muc-19": Box(1190, 920, 300, 80),
    "uc.muc-20": Box(1530, 920, 300, 80),
    "uc.muc-25": Box(1870, 920, 300, 80),
    "uc.muc-21": Box(1190, 1100, 280, 80),
    "uc.muc-22": Box(1530, 1100, 320, 80),
    "uc.muc-26": Box(1890, 1100, 260, 80),
    # Platform Administration
    "uc.muc-27": Box(2210, 920, 310, 80),
    "uc.muc-28": Box(2190, 1100, 330, 90),
    "uc.muc-29": Box(2210, 1270, 310, 80),
}

FIELDS = (
    ("Access & Identity", Box(450, 340, 900, 470), "access"),
    ("Patient Services", Box(1390, 340, 1160, 470), "patient"),
    ("Facility Administration", Box(450, 850, 690, 260), "facility"),
    ("Care & Facility Operations", Box(1160, 850, 1020, 390), "operations"),
    ("Platform Administration", Box(2180, 850, 370, 530), "platform"),
)

GROUP_FOR_USE_CASE = {
    **{f"uc.muc-{n:02d}": "access" for n in (1, 2, 3, 4, 5)},
    **{f"uc.muc-{n:02d}": "patient" for n in (6, 9, 11, 12, 13, 14)},
    **{f"uc.muc-{n:02d}": "facility" for n in (15, 16)},
    **{f"uc.muc-{n:02d}": "operations" for n in (19, 20, 21, 22, 25, 26)},
    **{f"uc.muc-{n:02d}": "platform" for n in (27, 28, 29)},
}

ROUTES = {
    # Visitor: short local lines plus two open routing lanes between rows.
    "relation.visitor-muc-01": Route(1.0, 0.28, 0.0, 0.50),
    "relation.visitor-muc-02": Route(1.0, 0.16, 0.50, 0.0, ((360, 350), (930, 350))),
    "relation.visitor-muc-03": Route(1.0, 0.68, 0.0, 0.50, ((370, 590),)),
    "relation.visitor-muc-04": Route(1.0, 0.84, 0.50, 0.0, ((360, 520), (1180, 520))),
    # Patient: shared Login uses the corridor above the second row; other routes
    # stay within the patient neighborhood.
    "relation.patient-muc-04": Route(0.0, 0.08, 0.50, 0.0, ((2670, 300), (1180, 300), (1180, 550))),
    "relation.patient-muc-06": Route(0.0, 0.18, 0.50, 0.0, ((2640, 330), (1570, 330))),
    "relation.patient-muc-09": Route(0.0, 0.30, 0.50, 0.0, ((2610, 350), (1920, 350))),
    "relation.patient-muc-11": Route(0.0, 0.43, 1.0, 0.50),
    "relation.patient-muc-12": Route(0.0, 0.60, 0.50, 0.0, ((2610, 530), (1580, 530))),
    "relation.patient-muc-13": Route(0.0, 0.78, 0.50, 1.0, ((2610, 700), (1930, 700))),
    # Facility Administrator: M19/M21 sit on the shared-operations edge.
    "relation.facility-admin-muc-15": Route(1.0, 0.34, 0.0, 0.50),
    "relation.facility-admin-muc-16": Route(1.0, 0.18, 0.50, 0.0, ((380, 830), (965, 830))),
    "relation.facility-admin-muc-19": Route(1.0, 0.52, 0.50, 0.0, ((370, 810), (1340, 810))),
    "relation.facility-admin-muc-21": Route(1.0, 0.76, 0.50, 1.0, ((380, 1200), (1330, 1200))),
    # Booking & Reception Staff: enters from below through a dedicated clear
    # corridor under the functional cards, then fans upward without crossing nodes.
    "relation.reception-muc-19": Route(0.10, 0.0, 0.0, 0.50, ((1300, 1480), (1150, 1480), (1150, 960))),
    "relation.reception-muc-20": Route(0.30, 0.0, 0.0, 0.50, ((1400, 1460), (1500, 1460), (1500, 960))),
    "relation.reception-muc-21": Route(0.46, 0.0, 0.50, 1.0, ((1480, 1440), (1330, 1440))),
    "relation.reception-muc-22": Route(0.64, 0.0, 0.50, 1.0, ((1570, 1420), (1690, 1420))),
    "relation.reception-muc-26": Route(0.90, 0.0, 0.30, 1.0, ((1700, 1400), (1970, 1400))),
    # Doctor
    "relation.doctor-muc-25": Route(0.75, 0.0, 1.0, 0.50, ((2100, 1460), (2170, 1460), (2170, 960))),
    "relation.doctor-muc-26": Route(0.35, 0.0, 0.70, 1.0, ((1990, 1440), (2070, 1440))),
    # Platform Administrator
    "relation.platform-admin-muc-27": Route(0.0, 0.16, 1.0, 0.50, ((2610, 960),)),
    "relation.platform-admin-muc-28": Route(0.0, 0.42, 1.0, 0.50, ((2610, 1145),)),
    "relation.platform-admin-muc-29": Route(0.0, 0.72, 1.0, 0.50),
    # External systems
    "relation.payment-gateway-muc-09": Route(0.50, 1.0, 0.50, 0.0, ((1690, 220), (1920, 220))),
    "relation.notification-service-muc-14": Route(0.50, 1.0, 1.0, 0.50, ((2220, 210), (2500, 210), (2500, 610))),
    "relation.map-service-muc-02": Route(0.50, 1.0, 0.50, 0.0, ((670, 210), (930, 210))),
    "relation.whatsapp-provider-muc-05": Route(0.50, 1.0, 0.50, 0.0, ((1070, 220), (1320, 220), (1320, 780), (890, 780))),
    # Dependencies
    "relation.inc-01": Route(0.82, 1.0, 0.22, 0.0, ((710, 660), (820, 660))),
    "relation.inc-02": Route(0.18, 1.0, 0.78, 0.0, ((1100, 660), (960, 660))),
    "relation.ext-01": Route(0.0, 0.50, 1.0, 0.50),
}

DEPENDENCY_LABELS = {
    "relation.inc-01": Box(610, 640, 150, 40),
    "relation.inc-02": Box(1050, 640, 150, 40),
    "relation.ext-01": Box(1680, 410, 120, 40),
}
EXTEND_CONDITION = Box(1650, 470, 390, 40)
