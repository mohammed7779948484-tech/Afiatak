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
        layout = view.options.get("layout", {})
        canvas = layout.get("canvas", [1600, 1000])
        clearance = self.design.geometry["quality"]["minimum_connector_clearance"]
        document = Document(
            view.title,
            width=int(canvas[0]),
            height=int(canvas[1]),
            connector_clearance=float(clearance),
        )
        document.model.set("background", layout.get("background", "#FFFFFF"))
        title = layout.get("title", [400, 30, 900, 50])
        document.vertex(
            "diagram-title",
            view.title,
            compile_style(
                "text;html=1;align=center;verticalAlign=middle;strokeColor=none;fillColor=none",
                fontFamily=self.design.typography["font_family"],
                fontSize=44,
                fontStyle=1,
                fontColor=self.design.palette["ink"],
            ),
            Geometry(*title),
            parent="layer-labels",
        )
        boundary_geometry = Geometry(*layout.get("boundary", [400, 100, 900, 650]))
        boundary = document.vertex(
            "system-boundary",
            view.options.get("systemName", "System"),
            compile_style(
                "swimlane;horizontal=1;startSize=50;container=1;pointerEvents=0;html=1;verticalAlign=top;align=left;spacingLeft=14",
                fillColor="none",
                strokeColor="#243B53",
                strokeWidth=2,
                fontStyle=1,
                fontSize=20,
                fontColor="#18324B",
            ),
            boundary_geometry,
            parent="layer-containers",
        )
        for index, heading in enumerate(layout.get("headings", []), start=1):
            document.vertex(
                f"section-heading-{index}",
                heading[0],
                compile_style(
                    "text;html=1;align=left;verticalAlign=middle;strokeColor=none;fillColor=none",
                    fontFamily=self.design.typography["font_family"],
                    fontSize=24,
                    fontStyle=1,
                    fontColor=heading[1],
                ),
                Geometry(*heading[2:]),
                parent=boundary,
            )
        configured_cases = layout.get("useCases", {})
        case_positions = (
            {
                item.id: Geometry(
                    *configured_cases[item.id][:2],
                    *(configured_cases[item.id][2:] or [300, 84]),
                )
                for item in cases
            }
            if configured_cases
            else self.layout.grid(
                cases, width=220, height=70, columns=2, origin=(60, 80), gap=(180, 55)
            )
        )
        case_roles = layout.get("caseRoles", {})
        family_styles = layout.get("familyStyles", {})
        for item in cases:
            family = case_roles.get(item.id, "access")
            document.vertex(
                drawio_id(item.id),
                item.name,
                compile_style(
                    self.design.node(
                        "primary",
                        "shape=ellipse;perimeter=ellipsePerimeter",
                    ),
                    **family_styles.get(family, {}),
                    fontSize=28,
                    fontColor="#18324B",
                    strokeWidth=2,
                ),
                case_positions[item.id],
                parent=boundary,
                metadata={"semanticId": item.id, "semanticType": item.type},
            )
        configured_actors = layout.get("actors", {})
        for index, actor in enumerate(actors):
            right = index % 2 == 1
            side_index = index // 2
            actor_geometry = configured_actors.get(
                actor.id,
                [1360 if right else 170, 180 + side_index * 210, 90, 130],
            )
            document.vertex(
                drawio_id(actor.id),
                actor.name,
                compile_style(
                    self.design.node(
                        "external",
                        "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top",
                    ),
                    fillColor=layout.get("background", "#FFFFFF"),
                    strokeColor="#334E68",
                    fontColor="#18324B",
                    fontSize=22,
                    strokeWidth=2,
                ),
                Geometry(*actor_geometry),
                metadata={"semanticId": actor.id, "semanticType": actor.type},
            )
        routes = layout.get("routes", {})
        for relation in relations:
            label = relation.name
            if relation.type in {"include", "extend"}:
                label = f"&lt;&lt;{relation.type}&gt;&gt;"
                condition = relation.metadata.get("condition")
                if condition:
                    label += f"<br>{condition}"
            edge_style = self.design.edge(relation.type)
            if relation.type == "association":
                external_service = relation.source in {
                    "actor.payment-gateway",
                    "actor.notification-service",
                    "actor.map-service",
                    "actor.whatsapp-auth-provider",
                }
                edge_style = compile_style(
                    edge_style,
                    strokeColor="#405F73" if external_service else "#5F7485",
                    strokeWidth=1.6 if external_service else 1.2,
                    opacity=88 if external_service else 70,
                )
            else:
                edge_style = compile_style(
                    edge_style,
                    strokeColor="#244E70",
                    strokeWidth=2,
                    fontSize=20,
                )
            document.edge(
                f"sem-{relation.id}",
                drawio_id(relation.source),
                drawio_id(relation.target),
                label,
                edge_style,
                waypoints=tuple(tuple(point) for point in routes.get(relation.id, [])),
            )
        return document
