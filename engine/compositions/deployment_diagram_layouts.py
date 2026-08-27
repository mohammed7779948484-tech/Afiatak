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
class DeploymentVisualTokens:
    title_font_size: float = 68.0
    node_name_font_size: float = 52.0
    node_name_line_height: float = 66.0
    contained_font_size: float = 35.0
    contained_line_height: float = 44.0
    subtitle_font_size: float = 31.0
    node_stroke_width: float = 3.2
    contained_stroke_width: float = 2.6
    connector_stroke_width: float = 3.0
    perspective_x: float = 58.0
    perspective_y: float = 46.0
    node_inset: float = 115.0


TOKENS = DeploymentVisualTokens()


@dataclass(frozen=True)
class NodeLayout:
    box: Rect
    title_bounds: Rect
    contained: tuple[tuple[str, Rect], ...] = ()
    subtitle: tuple[str, Rect] | None = None


@dataclass(frozen=True)
class DeploymentLayout:
    width: int
    height: int
    title_y: int
    nodes: dict[str, NodeLayout]
    communication_paths: dict[str, tuple[tuple[float, float], ...]]


CANVAS_WIDTH = 12400
CANVAS_HEIGHT = 7200


LAYOUT = DeploymentLayout(
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    title_y=245,
    nodes={
        "node.dep01.patient-mobile-device": NodeLayout(
            Rect(650, 1060, 2400, 980),
            Rect(870, 1220, 1960, 150),
            (("Android / iOS", Rect(900, 1515, 1900, 140)), ("Patient Application", Rect(900, 1720, 1900, 140))),
        ),
        "node.dep01.facility-client-device": NodeLayout(
            Rect(650, 3200, 2400, 980),
            Rect(870, 3360, 1960, 150),
            (("Desktop / Tablet", Rect(900, 3655, 1900, 140)), ("Web Browser", Rect(900, 3860, 1900, 140))),
        ),
        "node.dep01.platform-admin-client-device": NodeLayout(
            Rect(650, 5340, 2400, 980),
            Rect(835, 5500, 2030, 150),
            (("Web Browser", Rect(900, 5820, 1900, 140)),),
        ),
        "node.dep01.aafiatak-centralized-server": NodeLayout(
            Rect(4500, 1960, 3300, 2540),
            Rect(4740, 2140, 2820, 150),
            (
                ("Facility Web Dashboard", Rect(4780, 2660, 2740, 330)),
                ("Aafiatak Platform Administration Dashboard", Rect(4780, 3215, 2740, 330)),
                ("Aafiatak Backend", Rect(4780, 3770, 2740, 330)),
            ),
            ("Logical server-side grouping; physical placement unresolved", Rect(4780, 4260, 2740, 100)),
        ),
        "node.dep01.postgresql-environment": NodeLayout(
            Rect(5150, 5440, 2200, 900),
            Rect(5350, 5600, 1800, 140),
            (("PostgreSQL Database", Rect(5400, 5905, 1700, 150)),),
            ("Physical placement unresolved", Rect(5400, 6130, 1700, 80)),
        ),
        "node.dep01.whatsapp-auth-provider": NodeLayout(
            Rect(9200, 860, 2500, 820),
            Rect(9410, 1095, 2080, 145),
        ),
        "node.dep01.payment-gateway": NodeLayout(
            Rect(9200, 2460, 2500, 820),
            Rect(9410, 2730, 2080, 145),
        ),
        "node.dep01.notification-service": NodeLayout(
            Rect(9200, 4060, 2500, 820),
            Rect(9410, 4330, 2080, 145),
        ),
        "node.dep01.map-service": NodeLayout(
            Rect(9200, 5660, 2500, 820),
            Rect(9410, 5885, 2080, 145),
            (),
            ("Technical caller unresolved", Rect(9410, 6210, 2080, 80)),
        ),
    },
    communication_paths={
        "relation.dep01.communication.patient-mobile-to-server": ((3050, 1550), (4300, 1550), (4300, 2700), (4500, 2700)),
        "relation.dep01.communication.facility-client-to-server": ((3050, 3690), (4050, 3690), (4050, 3180), (4500, 3180)),
        "relation.dep01.communication.platform-admin-client-to-server": ((3050, 5830), (4250, 5830), (4250, 3950), (4500, 3950)),
        "relation.dep01.communication.server-to-postgresql": ((6200, 4500), (6200, 5440)),
        "relation.dep01.communication.server-to-whatsapp-auth": ((7800, 2490), (8500, 2490), (8500, 1270), (9200, 1270)),
        "relation.dep01.communication.server-to-payment-gateway": ((7800, 3000), (8740, 3000), (8740, 2870), (9200, 2870)),
        "relation.dep01.communication.server-to-notification-service": ((7800, 3900), (8600, 3900), (8600, 4470), (9200, 4470)),
    },
)


def layout_for(view_id: str) -> DeploymentLayout:
    if view_id != "aafiatak-mvp-deployment":
        raise ValueError(f"No deployment composition registered for {view_id}")
    return LAYOUT
