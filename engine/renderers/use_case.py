from __future__ import annotations

from engine.core.ids import drawio_id
from engine.core.models import SemanticModel, ViewSpec
from engine.drawio import Document, Geometry
from engine.drawio.styles import compile_style
from engine.renderers.base import BaseRenderer


class UseCaseRenderer(BaseRenderer):
    diagram_type = "use_case"

    def render(self, model: SemanticModel, view: ViewSpec) -> Document:
        profile = self.profile(view)
        if profile["orientation"] != "LR" or profile["actor_position"] != "outside_boundary":
            raise ValueError("use-case profile requires LR layout with actors outside the boundary")
        elements, relations = self.selected(model, view)
        actors = [item for item in elements if item.type == "actor"]
        cases = [item for item in elements if item.type == "use_case"]
        document = self.new_document(view.title)
        boundary = document.vertex(
            "system-boundary",
            view.options.get("systemName", "System"),
            compile_style(
                "swimlane;startSize=36;container=1;pointerEvents=0;html=1",
                fillColor="none",
                strokeColor=self.design.palette["border"],
                fontStyle=1,
            ),
            Geometry(400, 100, 900, max(650, 140 + len(cases) * 90)),
            parent="layer-containers",
        )
        case_positions = self.layout.grid(
            cases, width=220, height=70, columns=2, origin=(60, 80), gap=(180, 55)
        )
        for item in cases:
            document.vertex(
                drawio_id(item.id),
                item.name,
                self.design.node("primary", "ellipse"),
                case_positions[item.id],
                parent=boundary,
                metadata={"semanticId": item.id, "semanticType": item.type},
            )
        for index, actor in enumerate(actors):
            right = index % 2 == 1
            side_index = index // 2
            document.vertex(
                drawio_id(actor.id),
                actor.name,
                self.design.node(
                    "external", "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top"
                ),
                Geometry(1360 if right else 170, 180 + side_index * 210, 90, 130),
                metadata={"semanticId": actor.id, "semanticType": actor.type},
            )
        for relation in relations:
            label = relation.name
            if relation.type in {"include", "extend"}:
                label = f"<<{relation.type}>>"
            document.edge(
                f"sem-{relation.id}",
                drawio_id(relation.source),
                drawio_id(relation.target),
                label,
                self.design.edge(relation.type),
            )
        return document
