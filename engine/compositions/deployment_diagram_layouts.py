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
    node_stereotype_font_size: float = 26.0
    node_stereotype_line_height: float = 32.0
    contained_font_size: float = 35.0
    contained_line_height: float = 44.0
    contained_stereotype_font_size: float = 23.0
    contained_stereotype_line_height: float = 28.0
    subtitle_font_size: float = 31.0
    node_stroke_width: float = 3.2
    contained_stroke_width: float = 2.6
    connector_stroke_width: float = 3.0
    perspective_x: float = 58.0
    perspective_y: float = 46.0
    node_inset: float = 115.0


TOKENS = DeploymentVisualTokens()


@dataclass(frozen=True)
class ContainedItem:
    """Presentation-only UML notation for content deployed in an approved node."""

    label: str
    bounds: Rect
    visual_kind: str
    uml_kind: str
    stereotype: str


@dataclass(frozen=True)
class NodeLayout:
    box: Rect
    title_bounds: Rect
    contained: tuple[ContainedItem, ...] = ()
    subtitle: tuple[str, Rect] | None = None
    node_stereotype: str | None = None


@dataclass(frozen=True)
class DeploymentLayout:
    width: int
    height: int
    title_y: int
    nodes: dict[str, NodeLayout]
    communication_paths: dict[str, tuple[tuple[float, float], ...]]


def execution_environment(label: str, bounds: Rect) -> ContainedItem:
    return ContainedItem(label, bounds, "execution-environment", "executionEnvironment", "executionEnvironment")


def deployed_artifact(label: str, bounds: Rect) -> ContainedItem:
    return ContainedItem(label, bounds, "deployed-artifact", "artifact", "artifact")


def device_context(label: str, bounds: Rect) -> ContainedItem:
    return ContainedItem(label, bounds, "device-context", "device-context", "device")


# Compact academic composition: clients on the left, logical server at the centre,
# database immediately below, and external service boundaries on the right. All
# communication paths use dedicated, short orthogonal corridors around the server.
CANVAS_WIDTH = 10800
CANVAS_HEIGHT = 6400


LAYOUT = DeploymentLayout(
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    title_y=190,
    nodes={
        "node.dep01.patient-mobile-device": NodeLayout(
            Rect(450, 900, 2250, 900),
            Rect(650, 960, 1850, 210),
            (
                execution_environment("Android / iOS", Rect(700, 1270, 1750, 115)),
                deployed_artifact("Patient Application", Rect(700, 1450, 1750, 115)),
            ),
            node_stereotype="device",
        ),
        "node.dep01.facility-client-device": NodeLayout(
            Rect(450, 2800, 2250, 900),
            Rect(650, 2860, 1850, 210),
            (
                device_context("Desktop / Tablet", Rect(700, 3170, 1750, 115)),
                execution_environment("Web Browser", Rect(700, 3350, 1750, 115)),
            ),
            node_stereotype="device",
        ),
        "node.dep01.platform-admin-client-device": NodeLayout(
            Rect(450, 4700, 2250, 900),
            Rect(625, 4760, 1900, 250),
            (execution_environment("Web Browser", Rect(700, 5120, 1750, 115)),),
            node_stereotype="device",
        ),
        "node.dep01.aafiatak-centralized-server": NodeLayout(
            Rect(3850, 1700, 3100, 2700),
            Rect(4070, 1780, 2660, 220),
            (
                deployed_artifact("Facility Web Dashboard", Rect(4140, 2360, 2520, 280)),
                deployed_artifact("Aafiatak Platform Administration Dashboard", Rect(4140, 2860, 2520, 280)),
                deployed_artifact("Aafiatak Backend", Rect(4140, 3360, 2520, 280)),
            ),
            ("Logical server-side grouping; physical placement unresolved", Rect(4140, 4000, 2520, 100)),
            node_stereotype="executionEnvironment",
        ),
        "node.dep01.postgresql-environment": NodeLayout(
            Rect(4300, 4920, 2200, 830),
            Rect(4500, 4970, 1800, 245),
            (deployed_artifact("PostgreSQL Database", Rect(4550, 5300, 1700, 125)),),
            ("Physical placement unresolved", Rect(4550, 5540, 1700, 70)),
            node_stereotype="executionEnvironment",
        ),
        "node.dep01.whatsapp-auth-provider": NodeLayout(
            Rect(7450, 900, 2600, 720),
            Rect(7670, 1015, 2160, 220),
        ),
        "node.dep01.payment-gateway": NodeLayout(
            Rect(7450, 2300, 2600, 720),
            Rect(7670, 2420, 2160, 170),
        ),
        "node.dep01.notification-service": NodeLayout(
            Rect(7450, 3700, 2600, 720),
            Rect(7670, 3820, 2160, 170),
        ),
        "node.dep01.map-service": NodeLayout(
            Rect(7450, 5100, 2600, 720),
            Rect(7670, 5210, 2160, 170),
            (),
            ("Technical caller unresolved", Rect(7670, 5605, 2160, 70)),
        ),
    },
    communication_paths={
        "relation.dep01.communication.patient-mobile-to-server": ((2700, 1350), (3400, 1350), (3400, 2100), (3850, 2100)),
        "relation.dep01.communication.facility-client-to-server": ((2700, 3250), (3330, 3250), (3330, 2700), (3850, 2700)),
        "relation.dep01.communication.platform-admin-client-to-server": ((2700, 5130), (3520, 5130), (3520, 3650), (3850, 3650)),
        "relation.dep01.communication.server-to-postgresql": ((5400, 4400), (5400, 4920)),
        "relation.dep01.communication.server-to-whatsapp-auth": ((6950, 2200), (7200, 2200), (7200, 1260), (7450, 1260)),
        "relation.dep01.communication.server-to-payment-gateway": ((6950, 2750), (7280, 2750), (7280, 2660), (7450, 2660)),
        "relation.dep01.communication.server-to-notification-service": ((6950, 3400), (7200, 3400), (7200, 4060), (7450, 4060)),
    },
)


def layout_for(view_id: str) -> DeploymentLayout:
    if view_id != "aafiatak-mvp-deployment":
        raise ValueError(f"No deployment composition registered for {view_id}")
    return LAYOUT
