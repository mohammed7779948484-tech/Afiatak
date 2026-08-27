from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rect:
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
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2


@dataclass(frozen=True)
class InterfacePlacement:
    component_id: str
    side: str
    x: float
    y: float
    label_anchor: str
    label_x: float
    label_y: float
    label_width: float


@dataclass(frozen=True)
class ComponentLayout:
    width: int
    height: int
    title_y: int
    component_boxes: dict[str, Rect]
    interfaces: dict[str, InterfacePlacement]
    connector_paths: dict[str, tuple[tuple[float, float], ...]]


CANVAS_WIDTH = 16000
CANVAS_HEIGHT = 9000


LAYOUT = ComponentLayout(
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    title_y=280,
    component_boxes={
        "component.cmp01.patient-application": Rect(850, 1400, 3000, 900),
        "component.cmp01.facility-web-dashboard": Rect(850, 3650, 3000, 900),
        "component.cmp01.platform-administration-dashboard": Rect(850, 5900, 3000, 1080),
        "component.cmp01.aafiatak-backend": Rect(6100, 3450, 3700, 1650),
        "component.cmp01.postgresql-database": Rect(6800, 6550, 2300, 880),
        "component.cmp01.whatsapp-authentication-provider": Rect(12100, 1150, 3050, 900),
        "component.cmp01.payment-gateway": Rect(12100, 3150, 3050, 900),
        "component.cmp01.notification-service": Rect(12100, 5150, 3050, 900),
        "component.cmp01.map-service": Rect(12100, 7150, 3050, 900),
    },
    interfaces={
        "component.cmp01.pi.aafiatak-application-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "left", 5900, 4225, "start", 6350, 3950, 2500
        ),
        "component.cmp01.pi.persistence-interface": InterfacePlacement(
            "component.cmp01.postgresql-database", "top", 7950, 6350, "middle", 7950, 6900, 1850
        ),
        "component.cmp01.pi.whatsapp-authentication-interface": InterfacePlacement(
            "component.cmp01.whatsapp-authentication-provider", "left", 11900, 1600, "start", 12350, 1515, 2550
        ),
        "component.cmp01.pi.payment-interface": InterfacePlacement(
            "component.cmp01.payment-gateway", "left", 11900, 3600, "start", 12350, 3515, 1800
        ),
        "component.cmp01.pi.notification-interface": InterfacePlacement(
            "component.cmp01.notification-service", "left", 11900, 5600, "start", 12350, 5515, 2100
        ),
        "component.cmp01.pi.map-location-interface": InterfacePlacement(
            "component.cmp01.map-service", "left", 11900, 7600, "start", 12350, 7515, 2100
        ),
        "component.cmp01.ri.patient-application-interface": InterfacePlacement(
            "component.cmp01.patient-application", "right", 4050, 1850, "end", 3600, 1770, 2200
        ),
        "component.cmp01.ri.facility-web-dashboard-interface": InterfacePlacement(
            "component.cmp01.facility-web-dashboard", "right", 4050, 4100, "end", 3600, 4020, 2200
        ),
        "component.cmp01.ri.platform-administration-dashboard-interface": InterfacePlacement(
            "component.cmp01.platform-administration-dashboard", "right", 4050, 6440, "end", 3600, 6360, 2200
        ),
        "component.cmp01.ri.persistence-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "bottom", 7950, 5300, "middle", 7950, 4820, 1800
        ),
        "component.cmp01.ri.whatsapp-authentication-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "right", 10000, 3825, "end", 9650, 3745, 2500
        ),
        "component.cmp01.ri.payment-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "right", 10000, 4275, "end", 9650, 4195, 1600
        ),
        "component.cmp01.ri.notification-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "right", 10000, 4725, "end", 9650, 4645, 1950
        ),
    },
    connector_paths={
        "relation.cmp01.assembly.patient-application": ((4120, 1850), (4850, 1850), (4850, 4225), (5845, 4225)),
        "relation.cmp01.assembly.facility-web-dashboard": ((4120, 4100), (5200, 4100), (5200, 4225), (5845, 4225)),
        "relation.cmp01.assembly.platform-administration-dashboard": ((4120, 6440), (5450, 6440), (5450, 4225), (5845, 4225)),
        "relation.cmp01.assembly.persistence": ((7950, 5370), (7950, 6295)),
        "relation.cmp01.assembly.whatsapp-authentication": ((10070, 3825), (10800, 3825), (10800, 1600), (11845, 1600)),
        "relation.cmp01.assembly.payment": ((10070, 4275), (11000, 4275), (11000, 3600), (11845, 3600)),
        "relation.cmp01.assembly.notification": ((10070, 4725), (11200, 4725), (11200, 5600), (11845, 5600)),
    },
)


def layout_for(view_id: str) -> ComponentLayout:
    if view_id != "aafiatak-system-component-architecture":
        raise ValueError(f"No component composition registered for {view_id}")
    return LAYOUT
