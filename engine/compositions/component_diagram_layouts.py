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
class ComponentVisualTokens:
    title_font_size: float = 68.0
    component_name_font_size: float = 54.0
    component_name_line_height: float = 68.0
    interface_label_font_size: float = 36.0
    interface_label_line_height: float = 44.0
    component_stroke_width: float = 3.2
    glyph_stroke_width: float = 3.0
    connector_stroke_width: float = 2.8
    provided_radius: float = 42.0
    required_radius: float = 48.0
    stem_length: float = 110.0
    module_tab_width: float = 138.0
    module_tab_height: float = 58.0
    module_tab_gap: float = 26.0


TOKENS = ComponentVisualTokens()


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


# The refined artboard is 22.5% narrower and 20% shorter than the prior
# 16000×9000 baseline. Components are recomposed, not uniformly scaled.
CANVAS_WIDTH = 12400
CANVAS_HEIGHT = 7200


LAYOUT = ComponentLayout(
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    title_y=245,
    component_boxes={
        "component.cmp01.patient-application": Rect(700, 1100, 3000, 780),
        "component.cmp01.facility-web-dashboard": Rect(700, 3150, 3000, 780),
        "component.cmp01.platform-administration-dashboard": Rect(700, 5100, 3000, 940),
        "component.cmp01.aafiatak-backend": Rect(4920, 2800, 3000, 1700),
        "component.cmp01.postgresql-database": Rect(5450, 5550, 2050, 820),
        "component.cmp01.whatsapp-authentication-provider": Rect(9200, 920, 2500, 780),
        "component.cmp01.payment-gateway": Rect(9200, 2700, 2500, 780),
        "component.cmp01.notification-service": Rect(9200, 4480, 2500, 780),
        "component.cmp01.map-service": Rect(9200, 6100, 2500, 780),
    },
    interfaces={
        # Provided interfaces are labelled in the exterior lane immediately left of
        # their lollipop; required interfaces use the exterior lane above/beside
        # their socket. No label is placed in its own component body.
        "component.cmp01.pi.aafiatak-application-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "left", 4800, 3650, "end", 4700, 4000, 1040
        ),
        "component.cmp01.pi.persistence-interface": InterfacePlacement(
            "component.cmp01.postgresql-database", "top", 6475, 5390, "end", 6275, 5470, 760
        ),
        "component.cmp01.pi.whatsapp-authentication-interface": InterfacePlacement(
            "component.cmp01.whatsapp-authentication-provider", "left", 9080, 1310, "end", 8970, 1190, 1130
        ),
        "component.cmp01.pi.payment-interface": InterfacePlacement(
            "component.cmp01.payment-gateway", "left", 9080, 3090, "end", 8970, 2970, 750
        ),
        "component.cmp01.pi.notification-interface": InterfacePlacement(
            "component.cmp01.notification-service", "left", 9080, 4870, "end", 8970, 5010, 820
        ),
        "component.cmp01.pi.map-location-interface": InterfacePlacement(
            "component.cmp01.map-service", "left", 9080, 6490, "end", 8970, 6370, 900
        ),
        "component.cmp01.ri.patient-application-interface": InterfacePlacement(
            "component.cmp01.patient-application", "right", 3820, 1490, "start", 3980, 1440, 900
        ),
        "component.cmp01.ri.facility-web-dashboard-interface": InterfacePlacement(
            "component.cmp01.facility-web-dashboard", "right", 3820, 3540, "start", 3980, 3518, 900
        ),
        "component.cmp01.ri.platform-administration-dashboard-interface": InterfacePlacement(
            "component.cmp01.platform-administration-dashboard", "right", 3820, 5570, "start", 3980, 5480, 900
        ),
        "component.cmp01.ri.persistence-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "bottom", 6475, 4620, "end", 6275, 4800, 760
        ),
        "component.cmp01.ri.whatsapp-authentication-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "right", 8040, 3240, "start", 8170, 3160, 730
        ),
        "component.cmp01.ri.payment-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "right", 8040, 3650, "start", 8190, 3525, 730
        ),
        "component.cmp01.ri.notification-interface": InterfacePlacement(
            "component.cmp01.aafiatak-backend", "right", 8040, 4060, "start", 8190, 3935, 820
        ),
    },
    connector_paths={
        # Three distinct ingress lanes terminate at different points of the one
        # backend lollipop, avoiding an ambiguous long shared terminal segment.
        "relation.cmp01.assembly.patient-application": ((3884, 1490), (3970, 1490), (3970, 3620), (4770, 3620)),
        "relation.cmp01.assembly.facility-web-dashboard": ((3884, 3540), (3920, 3540), (3920, 3650), (4758, 3650)),
        "relation.cmp01.assembly.platform-administration-dashboard": ((3884, 5570), (4900, 5570), (4900, 3680), (4770, 3680)),
        "relation.cmp01.assembly.persistence": ((6475, 4668), (6475, 5348)),
        "relation.cmp01.assembly.whatsapp-authentication": ((8088, 3240), (8100, 3240), (8100, 1310), (9038, 1310)),
        "relation.cmp01.assembly.payment": ((8088, 3650), (9000, 3650), (9000, 3090), (9038, 3090)),
        "relation.cmp01.assembly.notification": ((8088, 4060), (8720, 4060), (8720, 4870), (9038, 4870)),
    },
)


def layout_for(view_id: str) -> ComponentLayout:
    if view_id != "aafiatak-system-component-architecture":
        raise ValueError(f"No component composition registered for {view_id}")
    return LAYOUT
