from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float


CANVAS = (1920, 1080)
BOUNDARY = Box(220, 135, 1480, 810)

# This file is the diagram's artboard. Coordinates express presentation only;
# product semantics remain in the canonical model and view.
ACTORS = {
    "actor.visitor": Box(25, 210, 170, 115),
    "actor.facility-administrator": Box(20, 650, 180, 120),
    "actor.patient": Box(1720, 235, 175, 120),
    "actor.notification-service": Box(1720, 445, 175, 120),
    "actor.doctor": Box(1720, 630, 175, 120),
    "actor.platform-administrator": Box(1715, 830, 185, 120),
    "actor.map-service": Box(450, 15, 170, 110),
    "actor.whatsapp-auth-provider": Box(20, 400, 180, 125),
    "actor.payment-gateway": Box(1370, 15, 175, 110),
    "actor.booking-reception-staff": Box(820, 955, 220, 120),
}

USE_CASES = {
    "uc.muc-01": Box(290, 230, 220, 58),
    "uc.muc-02": Box(555, 230, 220, 58),
    "uc.muc-03": Box(290, 325, 220, 58),
    "uc.muc-04": Box(555, 325, 220, 58),
    "uc.muc-05": Box(555, 420, 220, 58),
    "uc.muc-06": Box(1190, 215, 220, 58),
    "uc.muc-09": Box(1435, 300, 220, 58),
    "uc.muc-11": Box(1190, 385, 220, 58),
    "uc.muc-12": Box(1435, 470, 220, 58),
    "uc.muc-13": Box(1190, 555, 220, 58),
    "uc.muc-14": Box(950, 470, 220, 58),
    "uc.muc-15": Box(290, 630, 220, 58),
    "uc.muc-16": Box(535, 630, 220, 58),
    "uc.muc-19": Box(780, 630, 220, 58),
    "uc.muc-20": Box(780, 730, 220, 58),
    "uc.muc-21": Box(535, 730, 220, 58),
    "uc.muc-22": Box(780, 830, 220, 58),
    "uc.muc-25": Box(1435, 625, 220, 58),
    "uc.muc-26": Box(1190, 730, 220, 58),
    "uc.muc-27": Box(1435, 795, 220, 58),
    "uc.muc-28": Box(1175, 830, 220, 58),
    "uc.muc-29": Box(1435, 875, 220, 58),
}

FIELDS = (
    ("Access & identity", Box(260, 195, 550, 310), "access"),
    ("Patient services", Box(920, 195, 745, 430), "patient"),
    ("Facility administration", Box(260, 590, 520, 310), "facility"),
    ("Care operations", Box(760, 590, 665, 310), "operations"),
    ("Platform administration", Box(1150, 785, 515, 150), "platform"),
)

# Connector paths are intentionally authored. The composition, not a router,
# keeps relationships local and avoids semantic nodes.
ROUTES = {
    "relation.visitor-muc-01": ((135, 252), (290, 259)),
    "relation.visitor-muc-02": ((120, 229), (240, 200), (665, 200), (665, 230)),
    "relation.visitor-muc-03": ((110, 268), (250, 354), (290, 354)),
    "relation.visitor-muc-04": ((133, 292), (245, 540), (820, 540), (820, 354), (775, 354)),
    "relation.patient-muc-04": ((1797, 254), (1650, 165), (820, 165), (820, 354), (775, 354)),
    "relation.patient-muc-06": ((1782, 277), (1410, 244)),
    "relation.patient-muc-09": ((1782, 277), (1655, 329)),
    "relation.patient-muc-11": ((1807, 293), (1660, 414), (1410, 414)),
    "relation.patient-muc-12": ((1784, 317), (1665, 499), (1655, 499)),
    "relation.patient-muc-13": ((1784, 317), (1670, 584), (1410, 584)),
    "relation.facility-admin-muc-15": ((135, 692), (290, 659)),
    "relation.facility-admin-muc-16": ((120, 669), (245, 590), (645, 590), (645, 630)),
    "relation.facility-admin-muc-19": ((110, 708), (240, 570), (890, 570), (890, 630)),
    "relation.facility-admin-muc-21": ((133, 732), (535, 759)),
    "relation.reception-muc-19": ((920, 974), (1050, 955), (1050, 659), (1000, 659)),
    "relation.reception-muc-20": ((940, 974), (1060, 955), (1060, 759), (1000, 759)),
    "relation.reception-muc-21": ((905, 997), (645, 955), (645, 788)),
    "relation.reception-muc-22": ((930, 964), (890, 888)),
    "relation.reception-muc-26": ((955, 997), (1140, 955), (1140, 759), (1190, 759)),
    "relation.doctor-muc-25": ((1782, 672), (1655, 654)),
    "relation.doctor-muc-26": ((1784, 712), (1410, 759)),
    "relation.platform-admin-muc-27": ((1797, 849), (1655, 824)),
    "relation.platform-admin-muc-28": ((1782, 872), (1670, 935), (1285, 935), (1285, 888)),
    "relation.platform-admin-muc-29": ((1784, 912), (1655, 904)),
    "relation.payment-gateway-muc-09": ((1480, 97), (1545, 130), (1545, 300)),
    "relation.notification-service-muc-14": ((1782, 487), (1690, 500), (1690, 445), (1170, 445), (1170, 499)),
    "relation.map-service-muc-02": ((558, 97), (640, 130), (640, 190), (665, 190), (665, 230)),
    "relation.whatsapp-provider-muc-05": ((135, 442), (555, 449)),
    "relation.inc-01": ((510, 354), (530, 354), (530, 449), (555, 449)),
    "relation.inc-02": ((665, 383), (665, 420)),
    "relation.ext-01": ((1435, 329), (1400, 329), (1400, 285), (1300, 285), (1300, 273)),
}

DEPENDENCY_LABELS = {
    "relation.inc-01": ((520, 398), None),
    "relation.inc-02": ((705, 405), None),
    "relation.ext-01": ((1350, 305), (1260, 342)),
}
