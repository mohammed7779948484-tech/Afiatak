from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from engine.core.models import SemanticElement
from engine.drawio.document import Geometry


@dataclass(frozen=True)
class PlacedElement:
    """Geometry plus the presentation decisions that produced it."""

    geometry: Geometry
    role: str
    zone: str | None = None
    side: str | None = None
    row: int | None = None
    column: int | None = None
    near: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HeadingPlacement(Mapping[str, Any]):
    id: str
    label: str
    geometry: Geometry
    role: str
    zone: str

    def __getitem__(self, key: str) -> Any:
        return {
            "id": self.id,
            "label": self.label,
            "geometry": self.geometry,
            "role": self.role,
            "zone": self.zone,
        }[key]

    def __iter__(self) -> Iterator[str]:
        return iter(("id", "label", "geometry", "role", "zone"))

    def __len__(self) -> int:
        return 5


@dataclass(frozen=True)
class UseCaseComposition:
    """Complete placement contract for a use-case renderer.

    ``canvas`` is ``(width, height)``. ``boundary`` and ``title`` use page
    coordinates. Use cases and headings use coordinates relative to
    ``boundary`` because they are true children of that container. Actors use
    page coordinates.
    """

    canvas: tuple[int, int]
    title: Geometry
    boundary: Geometry
    headings: tuple[HeadingPlacement, ...]
    use_cases: Mapping[str, Geometry]
    actors: Mapping[str, Geometry]
    case_roles: Mapping[str, str]
    placement_metadata: Mapping[str, PlacedElement]
    route_overrides: Mapping[str, tuple[tuple[float, float], ...]]
    metadata: Mapping[str, Any]

    def geometry_for(self, element_id: str) -> Geometry:
        if element_id in self.use_cases:
            return self.use_cases[element_id]
        return self.actors[element_id]


@dataclass(frozen=True)
class _Zone:
    id: str
    title: str
    role: str
    case_ids: tuple[str, ...]
    row: int
    column: int
    columns: int


class CuratedEditorialUseCasePlanner:
    """Deterministic semantic-neighborhood composition for large use-case views.

    The planner consumes high-level intent rather than authored coordinates.
    Supported intent keys are ``zones``, ``visualRoles``, ``preferredRows``,
    ``preferredColumns``, ``preferredSides``, ``near``/``proximity``,
    ``humanActors``, ``externalActors``, and optional ``geometry`` overrides.
    Camel-case and snake-case forms are accepted where practical.
    """

    SIDES = ("left", "right", "top", "bottom")

    def plan(
        self,
        elements: Sequence[SemanticElement],
        *,
        profile: Mapping[str, Any],
        design_geometry: Mapping[str, Any],
        intent: Mapping[str, Any],
    ) -> UseCaseComposition:
        if profile.get("composition") != "curated-editorial":
            raise ValueError("curated planner requires composition: curated-editorial")
        if profile.get("actor_position", "outside_boundary") != "outside_boundary":
            raise ValueError("curated use-case composition requires actors outside the boundary")

        actors = tuple(item for item in elements if item.type == "actor")
        cases = tuple(item for item in elements if item.type == "use_case")
        if not actors or not cases:
            raise ValueError("curated use-case composition requires actors and use cases")

        grid = int(design_geometry.get("grid", 10))
        spacing = design_geometry.get("spacing", {})
        quality = design_geometry.get("quality", {})
        shapes = design_geometry.get("shapes", {})
        overrides = {**profile.get("geometry", {}), **intent.get("geometry", {})}
        case_width, case_height = self._size(
            overrides.get("useCase", overrides.get("use_case")),
            shapes.get("use_case", {}),
            (220, 70),
        )
        actor_width, actor_height = self._size(
            overrides.get("actor"), shapes.get("actor", {}), (90, 130)
        )
        minimum_gap = int(quality.get("minimum_node_gap", 30))
        horizontal_gap = int(overrides.get("horizontalGap", spacing.get("lg", 80)))
        vertical_gap = int(overrides.get("verticalGap", spacing.get("md", 40)))
        zone_gap_x = int(overrides.get("zoneGapX", spacing.get("xl", 120)))
        zone_gap_y = int(overrides.get("zoneGapY", spacing.get("lg", 80)))
        horizontal_gap = max(minimum_gap, horizontal_gap)
        vertical_gap = max(minimum_gap, vertical_gap)
        heading_height = int(overrides.get("headingHeight", spacing.get("md", 40)))
        boundary_header = int(overrides.get("boundaryHeader", spacing.get("lg", 80)))
        boundary_padding = int(overrides.get("boundaryPadding", spacing.get("md", 40)))
        page_margin = int(quality.get("minimum_page_margin", 40))
        actor_gap = int(
            overrides.get("actorGap", quality.get("minimum_actor_boundary_gap", 40))
        )
        title_height = int(overrides.get("titleHeight", 60))

        zones = self._zones(intent, cases)
        preferred_rows = self._mapping(intent, "preferredRows", "preferred_rows")
        preferred_columns = self._mapping(intent, "preferredColumns", "preferred_columns")
        visual_roles = self._mapping(intent, "visualRoles", "visual_roles")
        near = self._near(intent)
        actor_ids = {item.id for item in actors}
        case_ids = {item.id for item in cases}
        invalid_near_sources = set(near) - actor_ids
        invalid_near_targets = {target for targets in near.values() for target in targets} - case_ids
        if invalid_near_sources or invalid_near_targets:
            invalid = invalid_near_sources | invalid_near_targets
            raise ValueError(f"proximity intent references unknown IDs: {', '.join(sorted(invalid))}")

        zone_orders: dict[str, tuple[str, ...]] = {}
        zone_slots: dict[str, dict[str, tuple[int, int]]] = {}
        zone_sizes: dict[str, tuple[int, int, int]] = {}
        for zone in zones:
            ordered = tuple(
                sorted(
                    zone.case_ids,
                    key=lambda item_id: (
                        int(preferred_rows.get(item_id, 10**6)),
                        int(preferred_columns.get(item_id, 10**6)),
                        item_id,
                    ),
                )
            )
            slots = {}
            for index, case_id in enumerate(ordered):
                default_row, default_column = divmod(index, zone.columns)
                row = int(preferred_rows.get(case_id, default_row))
                column = int(preferred_columns.get(case_id, default_column))
                if row < 0 or column < 0 or column >= zone.columns:
                    raise ValueError(f"invalid preferred row/column for {case_id}")
                slots[case_id] = (row, column)
            rows = max((item[0] for item in slots.values()), default=0) + 1
            width = zone.columns * case_width + (zone.columns - 1) * horizontal_gap
            height = heading_height + vertical_gap + rows * case_height + (rows - 1) * vertical_gap
            zone_orders[zone.id] = ordered
            zone_slots[zone.id] = slots
            zone_sizes[zone.id] = (width, height, rows)

        grid_columns = max(zone.column for zone in zones) + 1
        grid_rows = max(zone.row for zone in zones) + 1
        column_widths = [0] * grid_columns
        row_heights = [0] * grid_rows
        for zone in zones:
            width, height, _ = zone_sizes[zone.id]
            column_widths[zone.column] = max(column_widths[zone.column], width)
            row_heights[zone.row] = max(row_heights[zone.row], height)
        column_x = self._offsets(column_widths, zone_gap_x, boundary_padding)
        row_y = self._offsets(row_heights, zone_gap_y, boundary_header + boundary_padding)
        content_width = sum(column_widths) + zone_gap_x * (grid_columns - 1)
        content_height = sum(row_heights) + zone_gap_y * (grid_rows - 1)
        boundary_width = boundary_padding * 2 + content_width
        boundary_height = boundary_header + boundary_padding * 2 + content_height
        requested_boundary_width = int(overrides.get("boundaryWidth", boundary_width))
        requested_boundary_height = int(overrides.get("boundaryHeight", boundary_height))
        if requested_boundary_width > boundary_width:
            shift = (requested_boundary_width - boundary_width) // 2
            column_x = [value + shift for value in column_x]
            boundary_width = requested_boundary_width
        if requested_boundary_height > boundary_height:
            shift = (requested_boundary_height - boundary_height) // 2
            row_y = [value + shift for value in row_y]
            boundary_height = requested_boundary_height

        placed_cases: dict[str, PlacedElement] = {}
        headings: list[HeadingPlacement] = []
        zone_boxes: dict[str, tuple[int, int, int, int]] = {}
        by_case = {item.id: item for item in cases}
        for zone in zones:
            zone_x, zone_y = column_x[zone.column], row_y[zone.row]
            zone_width, zone_height, _ = zone_sizes[zone.id]
            zone_boxes[zone.id] = (zone_x, zone_y, zone_width, zone_height)
            headings.append(
                HeadingPlacement(
                    id=f"heading.{zone.id}",
                    label=zone.title,
                    geometry=self._geometry(zone_x, zone_y, zone_width, heading_height, grid),
                    role=zone.role,
                    zone=zone.id,
                )
            )
            for case_id in zone_orders[zone.id]:
                row, column = zone_slots[zone.id][case_id]
                geometry = self._geometry(
                    zone_x + column * (case_width + horizontal_gap),
                    zone_y + heading_height + vertical_gap + row * (case_height + vertical_gap),
                    case_width,
                    case_height,
                    grid,
                )
                placed_cases[case_id] = PlacedElement(
                    geometry=geometry,
                    role=str(visual_roles.get(case_id, zone.role)),
                    zone=zone.id,
                    row=row,
                    column=column,
                    metadata={"name": by_case[case_id].name, "coordinateSpace": "boundary"},
                )

        self._ensure_no_overlap(placed_cases)
        preferred_sides = self._mapping(intent, "preferredSides", "preferred_sides")
        external_ids = set(intent.get("externalActors", intent.get("external_actors", ())))
        human_ids = set(intent.get("humanActors", intent.get("human_actors", ())))
        unknown = (external_ids | human_ids) - actor_ids
        if unknown:
            raise ValueError(f"actor intent references unknown IDs: {', '.join(sorted(unknown))}")
        if not human_ids:
            human_ids = actor_ids - external_ids
        if external_ids & human_ids or external_ids | human_ids != actor_ids:
            raise ValueError("humanActors and externalActors must partition all selected actors")
        unknown_sides = set(preferred_sides) - actor_ids
        if unknown_sides:
            raise ValueError(
                f"preferred sides reference unknown actors: {', '.join(sorted(unknown_sides))}"
            )

        actor_sides: dict[str, str] = {}
        for actor in actors:
            side = preferred_sides.get(actor.id)
            if side is None and actor.id in external_ids:
                side = self._nearest_side(near.get(actor.id, ()), placed_cases, boundary_width, boundary_height)
            if side is None:
                raise ValueError(f"preferred side is required for human actor {actor.id}")
            side = str(side).lower()
            if side not in self.SIDES:
                raise ValueError(f"invalid preferred side {side!r} for {actor.id}")
            if actor.id in human_ids and side not in {"left", "right"}:
                raise ValueError(f"human actor {actor.id} must be on a left or right rail")
            actor_sides[actor.id] = side

        has_top = "top" in actor_sides.values()
        has_bottom = "bottom" in actor_sides.values()
        has_left = "left" in actor_sides.values()
        has_right = "right" in actor_sides.values()
        top_reserve = page_margin + title_height + vertical_gap
        if has_top:
            top_reserve += actor_height + actor_gap
        boundary_x = max(
            page_margin + (actor_width + actor_gap if has_left else 0),
            int(overrides.get("boundaryLeftMargin", 0)),
        )
        boundary_y = max(top_reserve, int(overrides.get("boundaryTopMargin", 0)))
        canvas_width = boundary_x + boundary_width + (actor_gap + actor_width if has_right else 0) + page_margin
        canvas_height = boundary_y + boundary_height + (actor_gap + actor_height if has_bottom else 0) + page_margin
        requested_canvas = intent.get("canvas")
        if requested_canvas:
            canvas_width = max(canvas_width, int(requested_canvas[0]))
            canvas_height = max(canvas_height, int(requested_canvas[1]))
        if not overrides.get("boundaryLeftMargin"):
            boundary_x += max(
                0,
                (
                    canvas_width
                    - (
                        boundary_x
                        + boundary_width
                        + (actor_gap + actor_width if has_right else 0)
                        + page_margin
                    )
                )
                // 2,
            )
        boundary = self._geometry(boundary_x, boundary_y, boundary_width, boundary_height, grid)

        desired: dict[str, float] = {}
        for actor in actors:
            targets = near.get(actor.id, ())
            target_centres = [self._case_centre(placed_cases[item].geometry) for item in targets if item in placed_cases]
            side = actor_sides[actor.id]
            if target_centres:
                axis = 1 if side in {"left", "right"} else 0
                desired[actor.id] = sum(item[axis] for item in target_centres) / len(target_centres)
            else:
                desired[actor.id] = boundary_height / 2 if side in {"left", "right"} else boundary_width / 2

        placed_actors: dict[str, PlacedElement] = {}
        for side in self.SIDES:
            side_actors = [item for item in actors if actor_sides[item.id] == side]
            if not side_actors:
                continue
            vertical = side in {"left", "right"}
            limit = boundary_height if vertical else boundary_width
            actor_size = actor_height if vertical else actor_width
            positions = self._spread(
                [(item.id, desired[item.id] - actor_size / 2) for item in side_actors],
                actor_size,
                minimum_gap,
                0,
                limit,
                grid,
            )
            for actor in side_actors:
                along = positions[actor.id]
                if side == "left":
                    geometry = Geometry(boundary.x - actor_gap - actor_width, boundary.y + along, actor_width, actor_height)
                elif side == "right":
                    geometry = Geometry(boundary.x + boundary.width + actor_gap, boundary.y + along, actor_width, actor_height)
                elif side == "top":
                    geometry = Geometry(boundary.x + along, boundary.y - actor_gap - actor_height, actor_width, actor_height)
                else:
                    geometry = Geometry(boundary.x + along, boundary.y + boundary.height + actor_gap, actor_width, actor_height)
                placed_actors[actor.id] = PlacedElement(
                    geometry=self._geometry(geometry.x, geometry.y, geometry.width, geometry.height, grid),
                    role=str(visual_roles.get(actor.id, "external-service" if actor.id in external_ids else "actor")),
                    side=side,
                    near=near.get(actor.id, ()),
                    metadata={
                        "name": actor.name,
                        "coordinateSpace": "page",
                        "actorKind": "external-service" if actor.id in external_ids else "human",
                    },
                )

        title = self._geometry(boundary.x, page_margin, boundary.width, title_height, grid)
        placement_metadata = {**placed_cases, **placed_actors}
        return UseCaseComposition(
            canvas=(self._snap(canvas_width, grid), self._snap(canvas_height, grid)),
            title=title,
            boundary=boundary,
            headings=tuple(headings),
            use_cases={key: value.geometry for key, value in placed_cases.items()},
            actors={key: value.geometry for key, value in placed_actors.items()},
            case_roles={key: value.role for key, value in placed_cases.items()},
            placement_metadata=placement_metadata,
            route_overrides={},
            metadata={
                "composition": "curated-editorial",
                "coordinateSpaces": {
                    "canvas": "page",
                    "title": "page",
                    "boundary": "page",
                    "headings": "boundary",
                    "useCases": "boundary",
                    "actors": "page",
                },
                "systemName": intent.get("systemName", intent.get("system_name", "System")),
                "zoneBoxes": zone_boxes,
                "actorSides": actor_sides,
                "counts": {"useCases": len(cases), "actors": len(actors), "zones": len(zones)},
            },
        )

    def _zones(self, intent: Mapping[str, Any], cases: Sequence[SemanticElement]) -> tuple[_Zone, ...]:
        raw = intent.get("zones")
        if not raw:
            raise ValueError("curated use-case composition requires functional zones")
        entries = []
        if isinstance(raw, Mapping):
            entries = [(str(key), value or {}) for key, value in raw.items()]
        else:
            entries = [(str(value["id"]), value) for value in raw]
        known = {item.id for item in cases}
        assigned: set[str] = set()
        result = []
        for index, (zone_id, value) in enumerate(entries):
            tags = set(value.get("tags", (zone_id,)))
            case_ids = tuple(
                value.get("useCases", value.get("use_cases", value.get("elements", ())))
            )
            if not case_ids:
                case_ids = tuple(item.id for item in cases if tags.intersection(item.tags))
            invalid = set(case_ids) - known
            duplicate = set(case_ids) & assigned
            if invalid or duplicate:
                bad = invalid or duplicate
                raise ValueError(f"invalid or duplicate use cases in zone {zone_id}: {', '.join(sorted(bad))}")
            assigned.update(case_ids)
            result.append(
                _Zone(
                    id=zone_id,
                    title=str(value.get("title", zone_id.replace("-", " ").title())),
                    role=str(value.get("visualRole", value.get("visual_role", zone_id))),
                    case_ids=case_ids,
                    row=int(value.get("preferredRow", value.get("preferred_row", index))),
                    column=int(value.get("preferredColumn", value.get("preferred_column", 0))),
                    columns=max(1, int(value.get("columns", 2))),
                )
            )
        missing = known - assigned
        if missing:
            raise ValueError(f"use cases missing from functional zones: {', '.join(sorted(missing))}")
        return tuple(result)

    @staticmethod
    def _mapping(intent: Mapping[str, Any], *keys: str) -> Mapping[str, Any]:
        for key in keys:
            value = intent.get(key)
            if isinstance(value, Mapping):
                return value
        return {}

    def _near(self, intent: Mapping[str, Any]) -> dict[str, tuple[str, ...]]:
        raw = intent.get("near", intent.get("proximity", {}))
        result: dict[str, list[str]] = {}
        if isinstance(raw, Mapping):
            for source, targets in raw.items():
                values = targets if isinstance(targets, (list, tuple)) else (targets,)
                result[str(source)] = [str(item) for item in values]
        else:
            for item in raw:
                source = str(item.get("source", item.get("actor")))
                target = str(item.get("target", item.get("near")))
                result.setdefault(source, []).append(target)
        return {key: tuple(dict.fromkeys(values)) for key, values in result.items()}

    @staticmethod
    def _size(value: Any, design: Mapping[str, Any], default: tuple[int, int]) -> tuple[int, int]:
        if isinstance(value, Mapping):
            return int(value.get("width", default[0])), int(value.get("height", default[1]))
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return int(value[0]), int(value[1])
        return int(design.get("width", default[0])), int(design.get("height", default[1]))

    @staticmethod
    def _offsets(sizes: Sequence[int], gap: int, origin: int) -> list[int]:
        result, current = [], origin
        for size in sizes:
            result.append(current)
            current += size + gap
        return result

    def _nearest_side(
        self,
        targets: Sequence[str],
        cases: Mapping[str, PlacedElement],
        boundary_width: int,
        boundary_height: int,
    ) -> str:
        centres = [self._case_centre(cases[item].geometry) for item in targets if item in cases]
        if not centres:
            return "right"
        x = sum(item[0] for item in centres) / len(centres)
        y = sum(item[1] for item in centres) / len(centres)
        distances = ((x, "left"), (boundary_width - x, "right"), (y, "top"), (boundary_height - y, "bottom"))
        return min(distances, key=lambda item: (item[0], self.SIDES.index(item[1])))[1]

    @staticmethod
    def _case_centre(geometry: Geometry) -> tuple[float, float]:
        return geometry.x + geometry.width / 2, geometry.y + geometry.height / 2

    @staticmethod
    def _spread(
        desired: Sequence[tuple[str, float]],
        size: int,
        gap: int,
        minimum: int,
        maximum: int,
        grid: int,
    ) -> dict[str, int]:
        ordered = sorted(desired, key=lambda item: (item[1], item[0]))
        required = len(ordered) * size + max(0, len(ordered) - 1) * gap
        if required > maximum - minimum:
            raise ValueError("actor rail is too short for configured actor geometry")
        positions: dict[str, int] = {}
        cursor = minimum
        for actor_id, wanted in ordered:
            position = max(cursor, min(wanted, maximum - size))
            positions[actor_id] = round(position / grid) * grid
            cursor = positions[actor_id] + size + gap
        overflow = cursor - gap - maximum
        if overflow > 0:
            shift = ((overflow + grid - 1) // grid) * grid
            positions = {key: value - shift for key, value in positions.items()}
        return positions

    @staticmethod
    def _ensure_no_overlap(placements: Mapping[str, PlacedElement]) -> None:
        items = list(placements.items())
        for index, (first_id, first) in enumerate(items):
            a = first.geometry
            for second_id, second in items[index + 1 :]:
                b = second.geometry
                if a.x < b.x + b.width and b.x < a.x + a.width and a.y < b.y + b.height and b.y < a.y + a.height:
                    raise ValueError(f"preferred use-case rows/columns overlap: {first_id} and {second_id}")

    @classmethod
    def _geometry(cls, x: float, y: float, width: float, height: float, grid: int) -> Geometry:
        return Geometry(*(cls._snap(value, grid) for value in (x, y, width, height)))

    @staticmethod
    def _snap(value: float, grid: int) -> int:
        return round(value / grid) * grid
