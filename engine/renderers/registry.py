from __future__ import annotations

from engine.renderers.activity import ActivityRenderer
from engine.renderers.base import BaseRenderer
from engine.renderers.class_diagram import ClassRenderer
from engine.renderers.communication import CommunicationRenderer
from engine.renderers.component import ComponentRenderer
from engine.renderers.deployment import DeploymentRenderer
from engine.renderers.object_diagram import ObjectRenderer
from engine.renderers.package import PackageRenderer
from engine.renderers.sequence import SequenceRenderer
from engine.renderers.state import StateRenderer
from engine.renderers.use_case import UseCaseRenderer

RENDERERS: dict[str, type[BaseRenderer]] = {
    "use_case": UseCaseRenderer,
    "class": ClassRenderer,
    "object": ObjectRenderer,
    "activity": ActivityRenderer,
    "sequence": SequenceRenderer,
    "communication": CommunicationRenderer,
    "state": StateRenderer,
    "package": PackageRenderer,
    "component": ComponentRenderer,
    "deployment": DeploymentRenderer,
}


def get_renderer(diagram_type: str) -> BaseRenderer:
    try:
        return RENDERERS[diagram_type]()
    except KeyError as exc:
        raise ValueError(f"unsupported diagram type: {diagram_type}") from exc
