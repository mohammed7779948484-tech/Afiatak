from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from engine.core.models import SemanticElement, SemanticModel, SemanticRelation, ViewSpec
from engine.drawio.document import Geometry
from engine.layout.use_case import CuratedEditorialUseCasePlanner, UseCaseComposition


class LayoutEngine:
    def __init__(self) -> None:
        self._use_case_planner = CuratedEditorialUseCasePlanner()

    def grid(
        self,
        elements: list[SemanticElement],
        *,
        width: int = 180,
        height: int = 70,
        columns: int = 4,
        origin: tuple[int, int] = (140, 140),
        gap: tuple[int, int] = (120, 100),
    ) -> dict[str, Geometry]:
        result: dict[str, Geometry] = {}
        for index, element in enumerate(elements):
            row, column = divmod(index, max(1, columns))
            result[element.id] = Geometry(
                origin[0] + column * (width + gap[0]),
                origin[1] + row * (height + gap[1]),
                width,
                height,
            )
        return result

    def radial(
        self, elements: list[SemanticElement], *, centre=(760, 480), radius=300
    ) -> dict[str, Geometry]:
        result = {}
        count = max(1, len(elements))
        for index, element in enumerate(elements):
            angle = 2 * math.pi * index / count
            result[element.id] = Geometry(
                round((centre[0] + radius * math.cos(angle)) / 10) * 10,
                round((centre[1] + radius * math.sin(angle)) / 10) * 10,
                180,
                70,
            )
        return result

    def curated_editorial(
        self,
        elements: Sequence[SemanticElement],
        *,
        profile: Mapping[str, Any],
        design_geometry: Mapping[str, Any],
        intent: Mapping[str, Any],
    ) -> UseCaseComposition:
        """Compose a large use-case view from high-level presentation intent."""

        return self._use_case_planner.plan(
            elements,
            profile=profile,
            design_geometry=design_geometry,
            intent=intent,
        )

    def plan_use_case(
        self,
        *,
        model: SemanticModel,
        view: ViewSpec,
        profile: Mapping[str, Any],
        design: Any,
        actors: Sequence[SemanticElement],
        use_cases: Sequence[SemanticElement],
        relations: Sequence[SemanticRelation],
    ) -> UseCaseComposition | None:
        """Renderer adapter for curated profiles; generic profiles keep fallback behavior."""

        if profile.get("composition") != "curated-editorial":
            return None
        planner_config = profile.get("planner", {})
        if planner_config.get("strategy") != "neighborhood-bands":
            raise ValueError("curated-editorial requires planner.strategy: neighborhood-bands")
        actor_placement = planner_config.get("actor_placement", {})
        if actor_placement.get("human") != "outside-left-and-right" or actor_placement.get(
            "external_service"
        ) != "nearest-interaction":
            raise ValueError("curated-editorial requires explicit human and external actor placement")
        layout = view.options.get("layout", {})
        intent = self._profile_intent(
            profile=profile,
            layout=layout,
            actors=actors,
            use_cases=use_cases,
            relations=relations,
            geometry=design.geometry,
        )
        presentation = dict(view.options.get("presentation", layout.get("intent", {})))
        for key in ("geometry", "visualRoles", "preferredRows", "preferredColumns", "preferredSides", "near"):
            if isinstance(presentation.get(key), Mapping):
                intent[key] = {**intent.get(key, {}), **presentation[key]}
        intent.update(
            {
                key: value
                for key, value in presentation.items()
                if key
                not in {
                    "geometry",
                    "visualRoles",
                    "preferredRows",
                    "preferredColumns",
                    "preferredSides",
                    "near",
                }
            }
        )
        intent.setdefault("systemName", view.options.get("systemName", model.model_id))
        return self.curated_editorial(
            [*actors, *use_cases],
            profile=profile,
            design_geometry=design.geometry,
            intent=intent,
        )

    @staticmethod
    def _profile_intent(
        *,
        profile: Mapping[str, Any],
        layout: Mapping[str, Any],
        actors: Sequence[SemanticElement],
        use_cases: Sequence[SemanticElement],
        relations: Sequence[SemanticRelation],
        geometry: Mapping[str, Any],
    ) -> dict[str, Any]:
        planner = profile.get("planner", {})
        neighborhoods = planner.get("neighborhoods", ())
        zone_cases: dict[str, list[str]] = {item["id"]: [] for item in neighborhoods}
        for case in use_cases:
            tags = set(case.tags)
            candidates = [
                item["id"]
                for item in neighborhoods
                if item["id"] in tags or item.get("tag") in tags
            ]
            if len(candidates) == 1:
                zone_cases[candidates[0]].append(case.id)
        zones = []
        for item in neighborhoods:
            zone_id = item["id"]
            if not zone_cases[zone_id]:
                continue
            zones.append(
                {
                    "id": zone_id,
                    "title": zone_id.replace("-", " ").title(),
                    "visualRole": item.get("role", zone_id),
                    "useCases": zone_cases[zone_id],
                    "preferredRow": int(item.get("row", item.get("order", 1))) - 1,
                    "preferredColumn": int(item.get("column", 0)),
                    "columns": int(item.get("columns", 2)),
                }
            )

        actor_ids = {item.id for item in actors}
        near: dict[str, list[str]] = {}
        for relation in relations:
            if relation.type == "association" and relation.source in actor_ids:
                near.setdefault(relation.source, []).append(relation.target)

        page_key = planner.get("page", "landscape")
        page = geometry.get("page", {}).get(page_key, geometry.get("page", {}).get("landscape", {}))
        shape_key = page_key if page_key in geometry.get("shapes", {}) else "use_case"
        actor_key = "actor_overview" if page_key == "use_case_overview" else "actor"
        use_case_tokens = geometry.get("use_case", {})
        boundary_tokens = geometry.get("boundary", {})
        boundary_profile = boundary_tokens.get(planner.get("boundary", page_key), {})
        return {
            "canvas": [page.get("width", 1600), page.get("height", 1000)],
            "geometry": {
                "useCase": geometry.get("shapes", {}).get(shape_key, {}),
                "actor": geometry.get("shapes", {}).get(actor_key, {}),
                "horizontalGap": use_case_tokens.get("column_gap", geometry.get("spacing", {}).get("lg", 80)),
                "verticalGap": use_case_tokens.get("row_gap", geometry.get("spacing", {}).get("md", 40)),
                "zoneGapX": use_case_tokens.get("neighborhood_gap", geometry.get("spacing", {}).get("xl", 120)),
                "zoneGapY": use_case_tokens.get("neighborhood_gap", geometry.get("spacing", {}).get("lg", 80)),
                "actorGap": use_case_tokens.get("actor_gap", boundary_tokens.get("actor_clearance", 40)),
                "boundaryHeader": boundary_tokens.get("title_band_height", 50),
                "boundaryPadding": boundary_tokens.get("internal_margin", 40),
                "boundaryLeftMargin": boundary_profile.get("left_margin", 0),
                "boundaryTopMargin": boundary_profile.get("top_margin", 0),
                "boundaryWidth": max(
                    0,
                    page.get("width", 0)
                    - boundary_profile.get("left_margin", 0)
                    - boundary_profile.get("right_margin", 0),
                ),
                "boundaryHeight": max(
                    0,
                    page.get("height", 0)
                    - boundary_profile.get("top_margin", 0)
                    - boundary_profile.get("bottom_margin", 0),
                ),
            },
            "zones": zones,
            "near": near,
        }
