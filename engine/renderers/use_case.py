from __future__ import annotations

import inspect
import math
from collections.abc import Mapping
from typing import Any

from engine.core.ids import drawio_id
from engine.core.models import SemanticModel, ViewSpec
from engine.drawio import Document, Geometry
from engine.drawio.styles import compile_style
from engine.renderers.base import BaseRenderer


class UseCaseRenderer(BaseRenderer):
    diagram_type = "use_case"

    _ROLE_FALLBACKS = {
        "access": "primary",
        "booking": "accent",
        "facility": "success",
        "reception": "warning",
        "administration": "secondary",
    }

    @staticmethod
    def _value(source: Any, *names: str, default: Any = None) -> Any:
        for name in names:
            if isinstance(source, Mapping) and name in source:
                return source[name]
            if hasattr(source, name):
                return getattr(source, name)
        return default

    @staticmethod
    def _geometry(value: Any) -> Geometry:
        if isinstance(value, Geometry):
            return value
        if hasattr(value, "geometry"):
            return UseCaseRenderer._geometry(value.geometry)
        if isinstance(value, Mapping):
            return Geometry(
                float(value["x"]),
                float(value["y"]),
                float(value["width"]),
                float(value["height"]),
            )
        return Geometry(*(float(item) for item in value))

    def _call_design(self, name: str, *args: Any, **kwargs: Any) -> Any:
        method = getattr(self.design, name, None)
        if not callable(method):
            return None
        signature = inspect.signature(method)
        if any(item.kind == inspect.Parameter.VAR_KEYWORD for item in signature.parameters.values()):
            return method(*args, **kwargs)
        accepted = {key: value for key, value in kwargs.items() if key in signature.parameters}
        return method(*args, **accepted)

    def _text_style(self, role: str, profile: str) -> str:
        provided = self._call_design(
            "semantic_text",
            role,
            profile=profile,
            align="center" if role in {"page_title", "stereotype"} else "left",
        )
        if provided:
            return provided
        typography = self.design.typography
        token = self.design.typography_role(role)
        return compile_style(
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap",
            align="center" if role in {"page_title", "stereotype"} else "left",
            verticalAlign="middle",
            fontFamily=typography["font_family"],
            fontSize=token["size"],
            fontStyle=1 if token.get("bold") else 0,
            fontColor=self.design.palette["ink"],
        )

    def _boundary_style(self, profile: str) -> str:
        provided = self._call_design(
            "semantic_node",
            "secondary",
            "swimlane;horizontal=1;container=1;pointerEvents=0;html=1;"
            "verticalAlign=top;align=left",
            text_role="boundary_title",
            appearance_role="boundary",
        )
        header = self.design.geometry["boundary"]["title_band_height"]
        inset = self.design.geometry["spacing"]["sm"]
        if provided:
            return compile_style(
                provided,
                fillColor="none",
                strokeColor=self.design.palette["boundary"],
                startSize=header,
                spacingLeft=inset,
                align="left",
                verticalAlign="top",
            )
        return compile_style(
            self.design.node(
                "secondary",
                "swimlane;horizontal=1;container=1;pointerEvents=0;html=1;"
                "verticalAlign=top;align=left",
            ),
            fillColor="none",
            strokeColor=self.design.palette["boundary"],
            startSize=header,
            spacingLeft=inset,
            fontStyle=1 if self.design.typography["section"].get("bold") else 0,
            fontSize=self.design.typography["section"]["size"],
            align="left",
            verticalAlign="top",
        )

    def _case_style(self, role: str, profile: str) -> str:
        appearance_role = role if role in {"helper", "shared"} else "use_case"
        provided = self._call_design(
            "semantic_node",
            role,
            "shape=ellipse;perimeter=ellipsePerimeter",
            profile=profile,
            text_role="use_case",
            appearance_role=appearance_role,
        )
        if provided:
            return provided
        palette_role = role if f"{role}_fill" in self.design.palette else self._ROLE_FALLBACKS.get(
            role, "primary"
        )
        return self.design.node(
            palette_role,
            "shape=ellipse;perimeter=ellipsePerimeter",
        )

    def _actor_style(self, role: str, profile: str) -> str:
        role = role.replace("-", "_")
        palette_role = "external_service" if role == "external_service" else "external"
        provided = self._call_design(
            "semantic_node",
            palette_role,
            "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top",
            profile=profile,
            text_role="actor",
            appearance_role=role,
        )
        if provided:
            return compile_style(
                provided,
                fillColor="none" if role == "actor" else None,
                verticalLabelPosition="bottom",
                verticalAlign="top",
            )
        return compile_style(
            self.design.node(
                palette_role,
                "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top",
            ),
            fillColor="none" if role == "actor" else None,
        )

    def _relationship_label_style(self, text_role: str, profile: str) -> str:
        text = self._text_style(text_role, profile)
        return compile_style(
            "edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[]",
            text,
            labelBackgroundColor=self.design.background(profile=profile),
        )

    def _planner_result(
        self,
        model: SemanticModel,
        view: ViewSpec,
        profile: Mapping[str, Any],
        actors: list,
        cases: list,
        relations: list,
    ) -> Any:
        planner = getattr(self.layout, "plan_use_case", None)
        if not callable(planner):
            planner = None
        available = {
            "model": model,
            "view": view,
            "profile": profile,
            "design": self.design,
            "actors": actors,
            "use_cases": cases,
            "cases": cases,
            "relations": relations,
            "elements": [*actors, *cases],
        }
        if planner is not None:
            signature = inspect.signature(planner)
            if any(
                item.kind == inspect.Parameter.VAR_KEYWORD
                for item in signature.parameters.values()
            ):
                return planner(**available)
            arguments = {
                name: available[name]
                for name, parameter in signature.parameters.items()
                if name in available and parameter.kind != inspect.Parameter.POSITIONAL_ONLY
            }
            missing = [
                name
                for name, parameter in signature.parameters.items()
                if parameter.default is inspect.Parameter.empty
                and parameter.kind
                not in {inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD}
                and name not in arguments
            ]
            if not missing:
                return planner(**arguments)
        curated = getattr(self.layout, "curated_editorial", None)
        intent = view.options.get("presentation", view.options.get("layout", {}))
        if callable(curated) and profile.get("composition") == "curated-editorial" and intent.get(
            "zones"
        ):
            return curated(
                [*actors, *cases],
                profile=profile,
                design_geometry=self.design.geometry,
                intent=intent,
            )
        return None

    def _fallback_layout(self, actors: list, cases: list) -> dict[str, Any]:
        geometry = self.design.geometry
        page = geometry["page"]["landscape"]
        spacing = geometry["spacing"]
        actor_size = geometry["shapes"]["actor"]
        case_size = geometry["shapes"]["use_case"]
        margin = page["margin"]
        actor_gap = geometry["quality"]["minimum_actor_boundary_gap"]
        title_height = self.design.typography["title"]["size"] + spacing["sm"]
        boundary_x = margin + actor_size["width"] + actor_gap
        boundary_y = margin + title_height + spacing["sm"]
        boundary_width = page["width"] - 2 * boundary_x
        boundary_height = page["height"] - boundary_y - margin
        columns = max(
            1,
            int((boundary_width - 2 * spacing["md"]) // (case_size["width"] + spacing["md"])),
        )
        rows = max(1, math.ceil(len(cases) / columns))
        vertical_gap = max(
            spacing["sm"],
            (boundary_height - 2 * spacing["lg"] - rows * case_size["height"])
            / max(1, rows - 1),
        )
        use_cases = {}
        for index, item in enumerate(cases):
            row, column = divmod(index, columns)
            use_cases[item.id] = Geometry(
                spacing["md"] + column * (case_size["width"] + spacing["md"]),
                spacing["lg"] + row * (case_size["height"] + vertical_gap),
                case_size["width"],
                case_size["height"],
            )
        actor_positions = {}
        side_count = max(1, math.ceil(len(actors) / 2))
        pitch = (page["height"] - 2 * margin - actor_size["height"]) / max(1, side_count - 1)
        for index, actor in enumerate(actors):
            right = index % 2 == 1
            side_index = index // 2
            actor_positions[actor.id] = Geometry(
                page["width"] - margin - actor_size["width"] if right else margin,
                margin + side_index * pitch,
                actor_size["width"],
                actor_size["height"],
            )
        return {
            "canvas": (page["width"], page["height"]),
            "title": Geometry(boundary_x, margin, boundary_width, title_height),
            "boundary": Geometry(boundary_x, boundary_y, boundary_width, boundary_height),
            "actors": actor_positions,
            "use_cases": use_cases,
        }

    def _placements(
        self,
        plan: Any,
        legacy: Mapping[str, Any],
        actors: list,
        cases: list,
    ) -> dict[str, Any]:
        fallback = self._fallback_layout(actors, cases)
        source = plan if plan is not None else legacy
        canvas_value = self._value(source, "canvas", default=fallback["canvas"])
        canvas = (
            (canvas_value.width, canvas_value.height)
            if isinstance(canvas_value, Geometry)
            else tuple(canvas_value)
        )
        title = self._geometry(self._value(source, "title", default=fallback["title"]))
        boundary = self._geometry(self._value(source, "boundary", default=fallback["boundary"]))
        actor_values = self._value(source, "actors", "actor_positions", default={}) or {}
        case_values = self._value(
            source, "use_cases", "useCases", "case_positions", default={}
        ) or {}
        all_values = self._value(source, "placements", "nodes", default={}) or {}
        actors_by_id = {
            item.id: self._geometry(actor_values.get(item.id, all_values.get(item.id, fallback["actors"][item.id])))
            for item in actors
        }
        cases_by_id = {}
        for item in cases:
            if item.id in case_values:
                cases_by_id[item.id] = self._geometry(case_values[item.id])
            elif item.id in all_values:
                absolute = self._geometry(all_values[item.id])
                cases_by_id[item.id] = Geometry(
                    absolute.x - boundary.x,
                    absolute.y - boundary.y,
                    absolute.width,
                    absolute.height,
                )
            else:
                cases_by_id[item.id] = fallback["use_cases"][item.id]
        roles = dict(self._value(source, "case_roles", "caseRoles", "roles", default={}) or {})
        roles.update(
            {
                item.id: getattr(case_values.get(item.id), "role").replace("-", "_")
                for item in cases
                if getattr(case_values.get(item.id), "role", None)
            }
        )
        placement_metadata = self._value(source, "placement_metadata", default={}) or {}
        actor_roles = {}
        for item in actors:
            role = getattr(actor_values.get(item.id), "role", None)
            if role is None and item.id in placement_metadata:
                role = getattr(placement_metadata[item.id], "role", None)
            actor_roles[item.id] = str(role or "actor").replace("-", "_")
        return {
            "canvas": canvas,
            "title": title,
            "boundary": boundary,
            "actors": actors_by_id,
            "use_cases": cases_by_id,
            "headings": self._value(source, "headings", "section_headings", default=[]) or [],
            "roles": roles,
            "actor_roles": actor_roles,
            "zones": {
                item.id: getattr(placement_metadata.get(item.id), "zone", None)
                for item in cases
            },
            "route_overrides": self._value(
                source, "route_overrides", "routeOverrides", default={}
            )
            or {},
        }

    def render(self, model: SemanticModel, view: ViewSpec) -> Document:
        profile = self.profile(view)
        if profile["orientation"] != "LR" or profile["actor_position"] != "outside_boundary":
            raise ValueError("use-case profile requires LR layout with actors outside the boundary")
        elements, relations = self.selected(model, view)
        actors = [item for item in elements if item.type == "actor"]
        cases = [item for item in elements if item.type == "use_case"]
        legacy = view.options.get("layout", {})
        plan = self._planner_result(model, view, profile, actors, cases, relations)
        placement = self._placements(plan, legacy, actors, cases)
        canvas = placement["canvas"]
        clearance = self.design.geometry["quality"]["minimum_connector_clearance"]
        document = Document(
            view.title,
            width=int(canvas[0]),
            height=int(canvas[1]),
            connector_clearance=float(clearance),
            routing_options={
                **self.design.routing,
                "corridor": self.design.geometry["use_case"]["routing_corridor"],
                "actor_label_clearance": self.design.geometry["quality"][
                    "minimum_actor_label_clearance"
                ],
            },
        )
        document.model.set("background", self.design.background(profile=view.layout_profile))
        document.vertex(
            "diagram-title",
            view.title,
            self._text_style("page_title", view.layout_profile),
            placement["title"],
            parent="layer-labels",
        )
        boundary = document.vertex(
            "system-boundary",
            view.options.get("systemName", "System"),
            self._boundary_style(view.layout_profile),
            placement["boundary"],
            parent="layer-containers",
        )
        for index, heading in enumerate(placement["headings"], start=1):
            heading_zone = getattr(heading, "zone", None)
            if hasattr(heading, "geometry"):
                label = heading.label
                geometry = self._geometry(heading.geometry)
            elif isinstance(heading, Mapping):
                label = heading.get("label", heading.get("name", ""))
                geometry = self._geometry(heading.get("geometry", heading))
            else:
                label = heading[0]
                geometry = self._geometry(heading[2:] if len(heading) > 5 else heading[1:])
            document.vertex(
                f"section-heading-{index}",
                label,
                self._text_style("section", view.layout_profile),
                geometry,
                parent=boundary,
                metadata={"presentationZone": str(heading_zone)} if heading_zone else None,
            )
        for item in cases:
            role = placement["roles"].get(item.id, "access")
            document.vertex(
                drawio_id(item.id),
                item.name,
                self._case_style(role, view.layout_profile),
                placement["use_cases"][item.id],
                parent=boundary,
                metadata={
                    "semanticId": item.id,
                    "semanticType": item.type,
                    "presentationZone": str(placement["zones"].get(item.id) or ""),
                },
            )
        for actor in actors:
            document.vertex(
                drawio_id(actor.id),
                actor.name,
                self._actor_style(
                    placement["actor_roles"].get(actor.id, "actor"), view.layout_profile
                ),
                placement["actors"][actor.id],
                metadata={"semanticId": actor.id, "semanticType": actor.type},
            )
        label_offset = -float(self.design.geometry["quality"]["minimum_edge_label_clearance"])
        actor_roles = placement["actor_roles"]
        for relation in relations:
            edge_id = f"sem-{relation.id}"
            is_dependency = relation.type in {"include", "extend"}
            edge_role = relation.type
            if relation.type == "association" and actor_roles.get(relation.source) == "external_service":
                edge_role = "external_association"
            document.edge(
                edge_id,
                drawio_id(relation.source),
                drawio_id(relation.target),
                "" if is_dependency else relation.name,
                self.design.semantic_edge(edge_role, profile=view.layout_profile),
                waypoints=tuple(
                    tuple(float(value) for value in point)
                    for point in placement["route_overrides"].get(relation.id, ())
                ),
            )
            if is_dependency:
                label = f"&lt;&lt;{relation.type}&gt;&gt;"
                condition = relation.metadata.get("condition")
                document.edge_label(
                    f"{edge_id}-label",
                    edge_id,
                    label,
                    0,
                    style=self._relationship_label_style("stereotype", view.layout_profile),
                    offset=(0, label_offset),
                )
                if condition:
                    document.edge_label(
                        f"{edge_id}-condition",
                        edge_id,
                        str(condition),
                        0,
                        style=self._relationship_label_style("condition", view.layout_profile),
                        offset=(0, -label_offset),
                    )
        return document
