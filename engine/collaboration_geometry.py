"""Deterministic, collision-aware geometry for UML Collaboration/Communication diagrams.

This module deliberately owns geometry only.  Semantic models stay immutable, while SVG
and diagrams.net renderers consume the same :class:`CollaborationRenderPlan`.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from math import ceil, hypot
from pathlib import Path
from typing import Iterable, Sequence

from PIL import ImageFont

from engine.compositions.collaboration_diagram_layouts import layout_for
from engine.core.models import SemanticElement, SemanticModel, SemanticRelation, ViewSpec


DEJAVU_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def shifted(self, dx: float, dy: float) -> "Point":
        return Point(self.x + dx, self.y + dy)


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    def expanded(self, amount: float) -> "Rect":
        return Rect(self.x - amount, self.y - amount, self.width + 2 * amount, self.height + 2 * amount)

    def intersects(self, other: "Rect") -> bool:
        return self.left < other.right and self.right > other.left and self.top < other.bottom and self.bottom > other.top

    def contains(self, point: Point) -> bool:
        return self.left <= point.x <= self.right and self.top <= point.y <= self.bottom

    def within(self, canvas: "Rect", margin: float = 0) -> bool:
        return self.left >= canvas.left + margin and self.right <= canvas.right - margin and self.top >= canvas.top + margin and self.bottom <= canvas.bottom - margin

    def data(self) -> str:
        return ",".join(f"{value:.2f}" for value in (self.x, self.y, self.width, self.height))

    @classmethod
    def from_data(cls, value: str) -> "Rect":
        x, y, width, height = (float(item) for item in value.split(","))
        return cls(x, y, width, height)


@dataclass(frozen=True)
class Segment:
    start: Point
    end: Point

    @property
    def length(self) -> float:
        return hypot(self.end.x - self.start.x, self.end.y - self.start.y)

    @property
    def unit(self) -> Point:
        length = self.length or 1.0
        return Point((self.end.x - self.start.x) / length, (self.end.y - self.start.y) / length)

    @property
    def normal(self) -> Point:
        unit = self.unit
        return Point(-unit.y, unit.x)

    @property
    def bounds(self) -> Rect:
        return Rect(min(self.start.x, self.end.x), min(self.start.y, self.end.y), abs(self.end.x - self.start.x), abs(self.end.y - self.start.y))

    def at(self, distance: float) -> Point:
        unit = self.unit
        return Point(self.start.x + unit.x * distance, self.start.y + unit.y * distance)

    def shifted(self, dx: float, dy: float) -> "Segment":
        return Segment(self.start.shifted(dx, dy), self.end.shifted(dx, dy))

    def data(self) -> str:
        return f"{self.start.x:.2f},{self.start.y:.2f};{self.end.x:.2f},{self.end.y:.2f}"

    @classmethod
    def from_data(cls, value: str) -> "Segment":
        start, end = value.split(";")
        sx, sy = (float(item) for item in start.split(","))
        ex, ey = (float(item) for item in end.split(","))
        return cls(Point(sx, sy), Point(ex, ey))


@dataclass(frozen=True)
class Polyline:
    points: tuple[Point, ...]

    @property
    def segments(self) -> tuple[Segment, ...]:
        return tuple(Segment(self.points[index], self.points[index + 1]) for index in range(len(self.points) - 1))

    @property
    def length(self) -> float:
        return sum(segment.length for segment in self.segments)

    @property
    def bounds(self) -> Rect:
        xs = [point.x for point in self.points]
        ys = [point.y for point in self.points]
        return Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

    def at(self, distance: float) -> tuple[Point, Point]:
        remaining = max(0.0, min(distance, self.length))
        for segment in self.segments:
            if remaining <= segment.length:
                return segment.at(remaining), segment.unit
            remaining -= segment.length
        segment = self.segments[-1]
        return segment.end, segment.unit

    def intersects(self, rect: Rect) -> bool:
        return any(segment_intersects_rect(segment, rect) for segment in self.segments)

    def data(self) -> str:
        return " ".join(f"{point.x:.2f},{point.y:.2f}" for point in self.points)

    @classmethod
    def from_data(cls, value: str) -> "Polyline":
        return cls(tuple(Point(*(float(number) for number in point.split(","))) for point in value.split()))


@dataclass(frozen=True)
class TextBlock:
    lines: tuple[str, ...]
    bounds: Rect
    number: str
    number_x: float
    text_x: float
    first_baseline: float
    line_height: float
    font_size: float


@dataclass(frozen=True)
class ParticipantGeometry:
    element: SemanticElement
    bounds: Rect
    name_lines: tuple[str, ...]


@dataclass(frozen=True)
class StructuralLinkGeometry:
    link_id: str
    source_id: str
    target_id: str
    polyline: Polyline


@dataclass(frozen=True)
class ArrowGeometry:
    relation: SemanticRelation
    link_id: str
    segment: Segment
    lane: int
    start_distance: float
    end_distance: float


@dataclass(frozen=True)
class MessageLabelGeometry:
    relation: SemanticRelation
    link_id: str
    text: TextBlock


@dataclass(frozen=True)
class SelfLoopGeometry:
    relation: SemanticRelation
    owner_id: str
    side: str
    lane: int
    path: Polyline
    bounds: Rect
    label: MessageLabelGeometry


@dataclass(frozen=True)
class MessageRunGeometry:
    link_id: str
    side: str
    group_bounds: Rect
    labels: tuple[MessageLabelGeometry, ...]
    arrows: tuple[ArrowGeometry, ...]


@dataclass(frozen=True)
class Collision:
    code: str
    subject: str
    other: str | None
    message: str


@dataclass
class CollaborationRenderPlan:
    canvas: Rect
    heading: TextBlock
    participants: dict[str, ParticipantGeometry]
    links: dict[str, StructuralLinkGeometry]
    runs: dict[str, MessageRunGeometry]
    loops: tuple[SelfLoopGeometry, ...]
    layout_issues: list[Collision] = field(default_factory=list)

    @property
    def labels(self) -> tuple[MessageLabelGeometry, ...]:
        link_labels = tuple(label for run in self.runs.values() for label in run.labels)
        loop_labels = tuple(loop.label for loop in self.loops)
        return link_labels + loop_labels

    @property
    def arrows(self) -> tuple[ArrowGeometry, ...]:
        return tuple(arrow for run in self.runs.values() for arrow in run.arrows)


class TextMeasurer:
    """Font-aware, deterministic text measurement shared by all renderers."""

    def __init__(self, font_size: int, line_height: int, font_path: str = DEJAVU_SERIF):
        self.font_size = font_size
        self.line_height = line_height
        try:
            self.font = ImageFont.truetype(font_path, font_size)
        except OSError:
            self.font = ImageFont.load_default()

    def width(self, text: str) -> float:
        if hasattr(self.font, "getlength"):
            return float(self.font.getlength(text))
        box = self.font.getbbox(text)
        return float(box[2] - box[0])

    def wrap(self, text: str, maximum_width: float) -> tuple[str, ...]:
        words = text.split()
        if not words:
            return ("",)
        lines: list[str] = []
        line = ""
        for word in words:
            candidate = word if not line else f"{line} {word}"
            if line and self.width(candidate) > maximum_width:
                lines.append(line)
                line = self._split_long_word(word, maximum_width)
                if "\n" in line:
                    fragments = line.split("\n")
                    lines.extend(fragments[:-1])
                    line = fragments[-1]
            else:
                line = candidate
        if line:
            lines.append(line)
        return tuple(lines)

    def _split_long_word(self, word: str, maximum_width: float) -> str:
        if self.width(word) <= maximum_width:
            return word
        fragments: list[str] = []
        current = ""
        for character in word:
            candidate = current + character
            if current and self.width(candidate) > maximum_width:
                fragments.append(current)
                current = character
            else:
                current = candidate
        if current:
            fragments.append(current)
        return "\n".join(fragments)

    def label(self, relation: SemanticRelation, origin: Point, maximum_width: float) -> TextBlock:
        number = f"{relation.metadata['sequence']}."
        number_width = self.width(number)
        gap = max(24.0, self.font_size * 0.40)
        lines = self.wrap(relation.name, max(280.0, maximum_width - number_width - gap))
        line_widths = [self.width(line) for line in lines]
        width = max(number_width + gap + line_width for line_width in line_widths)
        top_pad = max(10.0, self.font_size * 0.14)
        bottom_pad = max(12.0, self.font_size * 0.17)
        height = top_pad + self.line_height * len(lines) + bottom_pad
        baseline = origin.y + top_pad + self.font_size
        return TextBlock(
            lines=lines,
            bounds=Rect(origin.x, origin.y, width, height),
            number=number,
            number_x=origin.x,
            text_x=origin.x + number_width + gap,
            first_baseline=baseline,
            line_height=self.line_height,
            font_size=self.font_size,
        )

    def participant_lines(self, name: str, maximum_width: float) -> tuple[str, ...]:
        return self.wrap(name, maximum_width)


# ---------- Basic geometry predicates ----------


def orientation(a: Point, b: Point, c: Point) -> float:
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def on_segment(a: Point, b: Point, c: Point) -> bool:
    return min(a.x, b.x) <= c.x <= max(a.x, b.x) and min(a.y, b.y) <= c.y <= max(a.y, b.y)


def segments_intersect(first: Segment, second: Segment) -> bool:
    a, b, c, d = first.start, first.end, second.start, second.end
    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    if o1 == 0 and on_segment(a, b, c):
        return True
    if o2 == 0 and on_segment(a, b, d):
        return True
    if o3 == 0 and on_segment(c, d, a):
        return True
    if o4 == 0 and on_segment(c, d, b):
        return True
    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)


def segment_intersects_rect(segment: Segment, rect: Rect) -> bool:
    if rect.contains(segment.start) or rect.contains(segment.end):
        return True
    corners = (Point(rect.left, rect.top), Point(rect.right, rect.top), Point(rect.right, rect.bottom), Point(rect.left, rect.bottom))
    edges = tuple(Segment(corners[index], corners[(index + 1) % 4]) for index in range(4))
    return any(segments_intersect(segment, edge) for edge in edges)


def point_to_segment_distance(point: Point, segment: Segment) -> float:
    dx = segment.end.x - segment.start.x
    dy = segment.end.y - segment.start.y
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return hypot(point.x - segment.start.x, point.y - segment.start.y)
    projection = ((point.x - segment.start.x) * dx + (point.y - segment.start.y) * dy) / length_squared
    projection = min(1.0, max(0.0, projection))
    nearest = Point(segment.start.x + projection * dx, segment.start.y + projection * dy)
    return hypot(point.x - nearest.x, point.y - nearest.y)


def segment_to_segment_distance(first: Segment, second: Segment) -> float:
    if segments_intersect(first, second):
        return 0.0
    return min(
        point_to_segment_distance(first.start, second),
        point_to_segment_distance(first.end, second),
        point_to_segment_distance(second.start, first),
        point_to_segment_distance(second.end, first),
    )


def rect_to_polyline_distance(rect: Rect, polyline: Polyline) -> float:
    """Return the shortest edge-to-edge distance from a label rectangle to a link."""
    corners = (Point(rect.left, rect.top), Point(rect.right, rect.top), Point(rect.right, rect.bottom), Point(rect.left, rect.bottom))
    rectangle_edges = tuple(Segment(corners[index], corners[(index + 1) % 4]) for index in range(4))
    return min(segment_to_segment_distance(rectangle_edge, link_segment) for rectangle_edge in rectangle_edges for link_segment in polyline.segments)


def rect_edge_point(centre: Point, other: Point, bounds: Rect) -> Point:
    dx, dy = other.x - centre.x, other.y - centre.y
    if dx == 0 and dy == 0:
        return centre
    half_width, half_height = bounds.width / 2, bounds.height / 2
    scale = min(half_width / abs(dx) if dx else float("inf"), half_height / abs(dy) if dy else float("inf"))
    return Point(centre.x + dx * scale, centre.y + dy * scale)


# ---------- Scene construction ----------


def _layout_side_candidates(hint: object) -> tuple[str, ...]:
    if isinstance(hint, str):
        return (hint,)
    if isinstance(hint, (list, tuple)):
        return tuple(str(value) for value in hint)
    return ("right", "left", "above", "below")


def _participant_geometry(model: SemanticModel, view: ViewSpec, composition: dict, layout, measurer: TextMeasurer) -> dict[str, ParticipantGeometry]:
    visible = {element.id: element for element in model.elements if element.id in view.include}
    if set(visible) != set(composition["participants"]):
        raise ValueError("Collaboration composition and visible participant set do not match")
    result: dict[str, ParticipantGeometry] = {}
    source_centre = Point(layout.composition_width / 2, layout.composition_height / 2)
    target_centre = Point(layout.width / 2, layout.height / 2)
    for element_id, element in visible.items():
        raw_x, raw_y = composition["participants"][element_id]
        cx = target_centre.x + (raw_x - source_centre.x) * layout.network_scale
        cy = target_centre.y + (raw_y - source_centre.y) * layout.network_scale
        bounds = Rect(cx - layout.participant_width / 2, cy - layout.participant_height / 2, layout.participant_width, layout.participant_height)
        result[element_id] = ParticipantGeometry(element, bounds, measurer.participant_lines(element.name, layout.participant_width - 180))
    return result


def _route_direct_or_orthogonal(source: ParticipantGeometry, target: ParticipantGeometry, obstacles: Iterable[ParticipantGeometry], canvas: Rect) -> Polyline:
    start = rect_edge_point(source.bounds.center, target.bounds.center, source.bounds)
    end = rect_edge_point(target.bounds.center, source.bounds.center, target.bounds)
    direct = Polyline((start, end))
    others = [item.bounds.expanded(80) for item in obstacles if item.element.id not in {source.element.id, target.element.id}]
    if not any(direct.intersects(rectangle) for rectangle in others):
        return direct
    candidates: list[Polyline] = []
    clearance = 180.0
    for rectangle in others:
        for y in (rectangle.top - clearance, rectangle.bottom + clearance):
            candidates.append(Polyline((start, Point(start.x, y), Point(end.x, y), end)))
        for x in (rectangle.left - clearance, rectangle.right + clearance):
            candidates.append(Polyline((start, Point(x, start.y), Point(x, end.y), end)))
    valid = [candidate for candidate in candidates if all(not candidate.intersects(rectangle) for rectangle in others) and candidate.bounds.within(canvas, 40)]
    return min(valid, key=lambda candidate: candidate.length) if valid else direct


def _link_geometries(view: ViewSpec, participants: dict[str, ParticipantGeometry], canvas: Rect) -> dict[str, StructuralLinkGeometry]:
    result: dict[str, StructuralLinkGeometry] = {}
    for link in view.options["structuralLinks"]:
        source_id, target_id = link["participants"]
        polyline = _route_direct_or_orthogonal(participants[source_id], participants[target_id], participants.values(), canvas)
        result[link["id"]] = StructuralLinkGeometry(link["id"], source_id, target_id, polyline)
    return result


def _side_vector(side: str) -> Point:
    return {
        "right": Point(1.0, 0.0),
        "left": Point(-1.0, 0.0),
        "above": Point(0.0, -1.0),
        "below": Point(0.0, 1.0),
    }[side]


def _local_sides(hint: object, tangent: Point) -> tuple[str, ...]:
    """Return useful local normal sides for the current link segment.

    A vertical corridor accepts labels to its right or left, while a horizontal
    corridor accepts labels above or below.  Diagonal corridors retain all
    cardinal preferences, projected onto the actual segment normal below.
    """
    requested = _layout_side_candidates(hint)
    if abs(tangent.y) >= abs(tangent.x) * 1.35:
        useful = ("right", "left")
    elif abs(tangent.x) >= abs(tangent.y) * 1.35:
        useful = ("above", "below")
    else:
        useful = ("right", "left", "above", "below")
    return tuple(side for side in requested if side in useful) + tuple(side for side in useful if side not in requested)


def _candidate_group_rect(anchor: Point, tangent: Point, side: str, width: float, height: float, shift: float, gap: float) -> Rect:
    """Place an axis-aligned label run in the local tangent/normal frame of a link."""
    normal = Point(-tangent.y, tangent.x)
    preferred = _side_vector(side)
    sign = 1.0 if normal.x * preferred.x + normal.y * preferred.y >= 0 else -1.0
    outward = Point(normal.x * sign, normal.y * sign)
    projected_half_extent = abs(outward.x) * width / 2 + abs(outward.y) * height / 2
    centre = anchor.shifted(
        outward.x * (projected_half_extent + gap) + tangent.x * shift,
        outward.y * (projected_half_extent + gap) + tangent.y * shift,
    )
    return Rect(centre.x - width / 2, centre.y - height / 2, width, height)


def _shifts() -> tuple[float, ...]:
    values = [0.0]
    for offset in range(170, 2381, 170):
        values.extend((-float(offset), float(offset)))
    return tuple(values)


def _group_measure(relations: Sequence[SemanticRelation], measurer: TextMeasurer, width_limit: float) -> tuple[list[TextBlock], float, float]:
    drafts: list[TextBlock] = []
    cursor = 0.0
    max_width = 0.0
    for relation in relations:
        text = measurer.label(relation, Point(0.0, cursor), width_limit)
        drafts.append(text)
        max_width = max(max_width, text.bounds.width)
        cursor += text.bounds.height + 24.0
    return drafts, max_width, max(0.0, cursor - 24.0)


def _collides_group(
    candidate: Rect,
    canvas: Rect,
    heading: Rect,
    participants: Iterable[ParticipantGeometry],
    links: dict[str, StructuralLinkGeometry],
    own_link_id: str,
    occupied_labels: Iterable[Rect],
    occupied_loops: Iterable[Rect],
) -> bool:
    if not candidate.within(canvas, 80):
        return True
    if candidate.expanded(24).intersects(heading):
        return True
    if any(candidate.expanded(36).intersects(participant.bounds) for participant in participants):
        return True
    if any(candidate.expanded(48).intersects(rectangle) for rectangle in occupied_labels):
        return True
    if any(candidate.expanded(36).intersects(rectangle) for rectangle in occupied_loops):
        return True
    return any(link_id != own_link_id and link.polyline.intersects(candidate.expanded(28)) for link_id, link in links.items())


def _labels_for_group(
    link_id: str,
    relations: Sequence[SemanticRelation],
    group: Rect,
    measurer: TextMeasurer,
    width_limit: float,
    side: str,
) -> tuple[MessageLabelGeometry, ...]:
    """Build labels inside a local group while keeping their near edge link-facing."""
    labels: list[MessageLabelGeometry] = []
    cursor = group.y
    for relation in relations:
        draft = measurer.label(relation, Point(0.0, cursor), width_limit)
        # A left-side vertical corridor must right-align each individual label.
        # Otherwise a short label inherits the group width as empty space and looks
        # detached even though the group envelope itself touches the link.
        if side == "left":
            origin_x = group.right - draft.bounds.width
        elif side in {"above", "below"}:
            origin_x = group.center.x - draft.bounds.width / 2
        else:
            origin_x = group.x
        text = measurer.label(relation, Point(origin_x, cursor), width_limit)
        labels.append(MessageLabelGeometry(relation, link_id, text))
        cursor += text.bounds.height + 24.0
    return tuple(labels)


def _link_run_candidates(
    link_id: str,
    relations: Sequence[SemanticRelation],
    hint: dict,
    link: StructuralLinkGeometry,
    canvas: Rect,
    heading: Rect,
    participants: dict[str, ParticipantGeometry],
    links: dict[str, StructuralLinkGeometry],
    occupied_labels: list[Rect],
    occupied_loops: list[Rect],
    measurer: TextMeasurer,
) -> list[tuple[tuple[float, float, int, int, int, float], str, Rect, tuple[MessageLabelGeometry, ...]]]:
    """Enumerate local, collision-free candidates ordered by own-link proximity."""
    base_width = float(hint.get("maxLabelWidth", 2700))
    local_gap = max(100.0, min(180.0, float(hint.get("labelGap", 180)) * 0.55))
    # Dense runs may occupy a small stack of parallel local lanes.  Every lane
    # remains within the hard own-link proximity ceiling; no remote text column
    # is introduced when the nearest lane is already occupied.
    local_gaps = tuple(dict.fromkeys((80.0, local_gap, 230.0, 380.0)))
    anchor_fractions = (0.50, 0.42, 0.58, 0.32, 0.68)
    anchors = tuple((fraction, *link.polyline.at(link.polyline.length * fraction)) for fraction in anchor_fractions)
    # The primary pass implements the target 80–250-unit local corridor.  The
    # second pass is reserved for dense, otherwise collision-free corridors.
    for allowed_distance in (250.0, 450.0):
        candidates: list[tuple[tuple[float, float, int, int, int, float], str, Rect, tuple[MessageLabelGeometry, ...]]] = []
        for width_index, width_limit in enumerate((base_width, max(1600.0, base_width - 320), max(1400.0, base_width - 640))):
            _, group_width, group_height = _group_measure(relations, measurer, width_limit)
            for fraction_index, (_, anchor, tangent) in enumerate(anchors):
                sides = _local_sides(hint.get("side"), tangent)
                for side_index, side in enumerate(sides):
                    for gap in local_gaps:
                        for shift in _shifts():
                            group = _candidate_group_rect(anchor, tangent, side, group_width, group_height, shift, gap)
                            if _collides_group(group, canvas, heading, participants.values(), links, link_id, occupied_labels, occupied_loops):
                                continue
                            labels = _labels_for_group(link_id, relations, group, measurer, width_limit, side)
                            distances = [rect_to_polyline_distance(label.text.bounds, link.polyline) for label in labels]
                            if min(distances) < 60.0 or max(distances) > allowed_distance:
                                continue
                            score = (max(distances), sum(distances) / len(distances), width_index, side_index, fraction_index, abs(shift))
                            candidates.append((score, side, group, labels))
        if candidates:
            unique: list[tuple[tuple[float, float, int, int, int, float], str, Rect, tuple[MessageLabelGeometry, ...]]] = []
            seen: set[tuple[str, int, int, int, int]] = set()
            for candidate in sorted(candidates, key=lambda item: item[0]):
                _, side, group, _ = candidate
                key = (side, round(group.x), round(group.y), round(group.width), round(group.height))
                if key not in seen:
                    seen.add(key)
                    unique.append(candidate)
            return unique
    return []


def _place_link_run(
    link_id: str,
    relations: Sequence[SemanticRelation],
    hint: dict,
    link: StructuralLinkGeometry,
    canvas: Rect,
    heading: Rect,
    participants: dict[str, ParticipantGeometry],
    links: dict[str, StructuralLinkGeometry],
    occupied_labels: list[Rect],
    occupied_loops: list[Rect],
    measurer: TextMeasurer,
) -> tuple[str, Rect, tuple[MessageLabelGeometry, ...]] | None:
    """Choose the closest collision-free local annotation corridor for one link."""
    candidates = _link_run_candidates(link_id, relations, hint, link, canvas, heading, participants, links, occupied_labels, occupied_loops, measurer)
    if not candidates:
        return None
    _, side, group, labels = candidates[0]
    occupied_labels.extend(label.text.bounds for label in labels)
    return side, group, labels


def _place_link_runs(
    link_id: str,
    relations: Sequence[SemanticRelation],
    hint: dict,
    link: StructuralLinkGeometry,
    canvas: Rect,
    heading: Rect,
    participants: dict[str, ParticipantGeometry],
    links: dict[str, StructuralLinkGeometry],
    occupied_labels: list[Rect],
    occupied_loops: list[Rect],
    measurer: TextMeasurer,
) -> tuple[tuple[str, Rect, tuple[MessageLabelGeometry, ...], tuple[SemanticRelation, ...]], ...] | None:
    """Place one local run, or minimally split a dense run into local sub-runs.

    Splitting preserves a message's structural-link membership and only occurs
    when the complete run cannot fit in the link's own local corridor.  It is a
    generic density adaptation: each chunk is still a compact numbered block
    beside the same reusable communication link.
    """
    whole = _place_link_run(link_id, relations, hint, link, canvas, heading, participants, links, occupied_labels, occupied_loops, measurer)
    if whole is not None:
        side, group, labels = whole
        return ((side, group, labels, tuple(relations)),)
    if len(relations) < 2:
        return None
    # Prefer the fewest local blocks, then progressively reduce the block size
    # only when another occupied label or a crossing corridor makes it necessary.
    for chunk_size in range((len(relations) + 1) // 2, 0, -1):
        chunks = tuple(tuple(relations[start:start + chunk_size]) for start in range(0, len(relations), chunk_size))
        if chunk_size == 1:
            # Deterministic last resort for a genuinely dense corridor: reserve
            # the longest labels first and use the closest open stacked lane.
            ranked = sorted(
                chunks,
                key=lambda chunk: measurer.label(chunk[0], Point(0.0, 0.0), float(hint.get("maxLabelWidth", 2700))).bounds.width,
                reverse=True,
            )
            final_occupied = list(occupied_labels)
            placements: list[tuple[str, Rect, tuple[MessageLabelGeometry, ...], tuple[SemanticRelation, ...]]] = []
            for chunk in ranked:
                candidates = _link_run_candidates(link_id, chunk, hint, link, canvas, heading, participants, links, final_occupied, occupied_loops, measurer)
                if not candidates:
                    placements = []
                    break
                _, side, group, labels = candidates[0]
                placements.append((side, group, labels, chunk))
                final_occupied.extend(label.text.bounds for label in labels)
            if placements:
                occupied_labels[:] = final_occupied
                return tuple(placements)
            continue
        # Keep a small beam of the best non-overlapping partial arrangements.
        # This solves dense paired/singleton lanes without exponential search and
        # remains deterministic because candidates are already proximity-sorted.
        beam: list[tuple[float, list[tuple[str, Rect, tuple[MessageLabelGeometry, ...], tuple[SemanticRelation, ...]]], list[Rect]]] = [(0.0, [], list(occupied_labels))]
        for chunk in chunks:
            expanded: list[tuple[float, list[tuple[str, Rect, tuple[MessageLabelGeometry, ...], tuple[SemanticRelation, ...]]], list[Rect]]] = []
            for cost, placements, current_occupied in beam:
                for candidate_score, side, group, labels in _link_run_candidates(link_id, chunk, hint, link, canvas, heading, participants, links, current_occupied, occupied_loops, measurer)[:8]:
                    next_occupied = [*current_occupied, *(label.text.bounds for label in labels)]
                    next_cost = cost + candidate_score[0] * 1000.0 + candidate_score[1]
                    expanded.append((next_cost, [*placements, (side, group, labels, chunk)], next_occupied))
            if not expanded:
                beam = []
                break
            beam = sorted(expanded, key=lambda item: item[0])[:24]
        if beam:
            _, placements, final_occupied = beam[0]
            occupied_labels[:] = final_occupied
            return tuple(placements)
    return None


def _point_projection_on_segment(point: Point, segment: Segment) -> tuple[Point, float]:
    dx = segment.end.x - segment.start.x
    dy = segment.end.y - segment.start.y
    denominator = dx * dx + dy * dy
    if denominator == 0:
        return segment.start, 0.0
    factor = min(1.0, max(0.0, ((point.x - segment.start.x) * dx + (point.y - segment.start.y) * dy) / denominator))
    return Point(segment.start.x + factor * dx, segment.start.y + factor * dy), factor


def _closest_polyline_distance(point: Point, polyline: Polyline) -> float:
    travelled = 0.0
    best_distance = float("inf")
    best_along = 0.0
    for segment in polyline.segments:
        projected, factor = _point_projection_on_segment(point, segment)
        distance = hypot(point.x - projected.x, point.y - projected.y)
        if distance < best_distance:
            best_distance = distance
            best_along = travelled + segment.length * factor
        travelled += segment.length
    return best_along


def _arrow_geometries(
    link_id: str,
    relations: Sequence[SemanticRelation],
    link: StructuralLinkGeometry,
    first_participant_id: str,
    labels: Sequence[MessageLabelGeometry],
    label_bounds: Sequence[Rect],
) -> tuple[ArrowGeometry, ...]:
    """Place small arrows on the same local link corridor as their own labels."""
    if not relations:
        return ()
    total = link.polyline.length
    endpoint_clearance = min(170.0, total * 0.08)
    usable = max(280.0, total - 2 * endpoint_clearance)
    minimum_length, minimum_gap = 62.0, 48.0
    # Reserve extra visual breathing room beyond the validator's hard minimum;
    # this produces compact parallel lanes instead of a crowded single-arrow rail.
    per_lane_capacity = min(4, max(1, int((usable + minimum_gap) // (minimum_length + minimum_gap + 36.0))))
    lane_count = max(1, ceil(len(relations) / per_lane_capacity))
    assignments: list[list[tuple[int, SemanticRelation]]] = [[] for _ in range(lane_count)]
    for index, relation in enumerate(relations):
        assignments[index % lane_count].append((index, relation))

    def segment_for(distance: float, relation: SemanticRelation, lane_offset: float, length: float) -> Segment:
        centre, direction = link.polyline.at(distance)
        normal = Point(-direction.y, direction.x)
        centre = centre.shifted(normal.x * lane_offset, normal.y * lane_offset)
        half = length / 2
        actual_direction = direction if relation.source == first_participant_id else Point(-direction.x, -direction.y)
        return Segment(
            Point(centre.x - actual_direction.x * half, centre.y - actual_direction.y * half),
            Point(centre.x + actual_direction.x * half, centre.y + actual_direction.y * half),
        )

    label_by_relation = {label.relation.id: label for label in labels}
    arrows: list[ArrowGeometry] = []
    for lane, assigned in enumerate(assignments):
        slot_count = len(assigned)
        spacing = usable / (slot_count + 1)
        arrow_length = max(minimum_length, min(150.0, spacing - minimum_gap))
        lane_offset = (lane - (lane_count - 1) / 2) * 36.0
        used_distances: list[float] = []
        for slot, (_, relation) in enumerate(assigned, start=1):
            label = label_by_relation[relation.id]
            label_centre = label.text.bounds.center
            preferred = _closest_polyline_distance(label_centre, link.polyline)
            preferred = min(total - endpoint_clearance - arrow_length / 2, max(endpoint_clearance + arrow_length / 2, preferred))
            fallback = endpoint_clearance + slot * spacing
            step = max(72.0, arrow_length + minimum_gap)
            candidates = [preferred, fallback]
            for multiple in range(1, 16):
                candidates.extend((preferred - multiple * step, preferred + multiple * step))
            centre_distance = preferred
            segment = segment_for(preferred, relation, lane_offset, arrow_length)
            for proposal in candidates:
                if proposal - arrow_length / 2 < endpoint_clearance or proposal + arrow_length / 2 > total - endpoint_clearance:
                    continue
                candidate_segment = segment_for(proposal, relation, lane_offset, arrow_length)
                if any(segment_intersects_rect(candidate_segment, bounds.expanded(14)) for bounds in label_bounds):
                    continue
                if any(abs(proposal - existing) < arrow_length + minimum_gap for existing in used_distances):
                    continue
                centre_distance, segment = proposal, candidate_segment
                break
            used_distances.append(centre_distance)
            half = arrow_length / 2
            arrows.append(ArrowGeometry(relation, link_id, segment, lane, centre_distance - half, centre_distance + half))
    return tuple(sorted(arrows, key=lambda arrow: arrow.relation.metadata["sequence"]))


def _loop_candidate(owner: ParticipantGeometry, side: str, lane: int, relation: SemanticRelation, measurer: TextMeasurer, canvas: Rect, label_side: str = "right") -> SelfLoopGeometry:
    bounds = owner.bounds
    clearance = 62.0 + lane * 54.0
    span = 235.0
    depth = 190.0 + lane * 42.0
    # Assign a distinct attachment slot for each self message.  The first uses the
    # object centre; later loops alternate above/below (or left/right) instead of
    # expanding into the same geometry.
    slot = 0.0 if lane == 0 else (1.0 if lane % 2 else -1.0) * ((lane + 1) // 2) * 260.0
    if side == "right":
        centre_y = bounds.center.y + slot
        loop_bounds = Rect(bounds.right, centre_y - span / 2, clearance + depth, span)
        path = Polyline((Point(bounds.right, centre_y - span * 0.28), Point(loop_bounds.right, loop_bounds.top), Point(loop_bounds.right, loop_bounds.bottom), Point(bounds.right, centre_y + span * 0.28)))
        label_origin = Point(loop_bounds.right + 48.0, loop_bounds.top)
    elif side == "left":
        centre_y = bounds.center.y + slot
        loop_bounds = Rect(bounds.left - clearance - depth, centre_y - span / 2, clearance + depth, span)
        path = Polyline((Point(bounds.left, centre_y - span * 0.28), Point(loop_bounds.left, loop_bounds.top), Point(loop_bounds.left, loop_bounds.bottom), Point(bounds.left, centre_y + span * 0.28)))
        draft = measurer.label(relation, Point(0, 0), 2000)
        label_origin = Point(loop_bounds.left - 48.0 - draft.bounds.width, loop_bounds.top)
    elif side == "above":
        centre_x = bounds.center.x + slot
        loop_bounds = Rect(centre_x - span / 2, bounds.top - clearance - depth, span, clearance + depth)
        path = Polyline((Point(centre_x - span * 0.28, bounds.top), Point(loop_bounds.left, loop_bounds.top), Point(loop_bounds.right, loop_bounds.top), Point(centre_x + span * 0.28, bounds.top)))
        label_origin = Point(loop_bounds.right + 48.0, loop_bounds.top)
    elif side == "below":
        centre_x = bounds.center.x + slot
        loop_bounds = Rect(centre_x - span / 2, bounds.bottom, span, clearance + depth)
        path = Polyline((Point(centre_x - span * 0.28, bounds.bottom), Point(loop_bounds.left, loop_bounds.bottom), Point(loop_bounds.right, loop_bounds.bottom), Point(centre_x + span * 0.28, bounds.bottom)))
        if label_side == "left":
            draft = measurer.label(relation, Point(0, 0), 2000)
            label_origin = Point(loop_bounds.left - 48.0 - draft.bounds.width, loop_bounds.bottom - depth)
        else:
            label_origin = Point(loop_bounds.right + 48.0, loop_bounds.bottom - depth)
    else:
        raise ValueError(f"Unknown self-loop side: {side}")
    label = MessageLabelGeometry(relation, "SELF", measurer.label(relation, label_origin, 2000))
    return SelfLoopGeometry(relation, owner.element.id, side, lane, path, loop_bounds, label)


def _loop_collides(
    loop: SelfLoopGeometry,
    canvas: Rect,
    participants: dict[str, ParticipantGeometry],
    links: dict[str, StructuralLinkGeometry],
    occupied_loops: Iterable[SelfLoopGeometry],
    occupied_labels: Iterable[Rect],
) -> bool:
    if not loop.bounds.within(canvas, 80) or not loop.label.text.bounds.within(canvas, 80):
        return True
    for participant_id, participant in participants.items():
        if participant_id != loop.owner_id and loop.bounds.expanded(25).intersects(participant.bounds):
            return True
        if loop.label.text.bounds.expanded(32).intersects(participant.bounds):
            return True
    if any(link.polyline.intersects(loop.bounds.expanded(24)) for link in links.values()):
        return True
    if any(link.polyline.intersects(loop.label.text.bounds.expanded(28)) for link in links.values()):
        return True
    if any(loop.bounds.expanded(40).intersects(other.bounds) or loop.label.text.bounds.expanded(48).intersects(other.label.text.bounds) for other in occupied_loops):
        return True
    return any(loop.label.text.bounds.expanded(48).intersects(rectangle) for rectangle in occupied_labels)


def _place_self_loops(
    relations: Sequence[SemanticRelation],
    composition: dict,
    participants: dict[str, ParticipantGeometry],
    links: dict[str, StructuralLinkGeometry],
    canvas: Rect,
    measurer: TextMeasurer,
) -> tuple[tuple[SelfLoopGeometry, ...], list[Collision]]:
    by_owner: dict[str, list[SemanticRelation]] = defaultdict(list)
    for relation in relations:
        if relation.source == relation.target:
            by_owner[relation.source].append(relation)
    placed: list[SelfLoopGeometry] = []
    issues: list[Collision] = []
    occupied_label_bounds: list[Rect] = []
    for owner_id, owner_relations in by_owner.items():
        owner_relations.sort(key=lambda relation: relation.metadata["sequence"])
        hints = composition.get("selfMessages", {}).get(owner_id, {})
        sides = _layout_side_candidates(hints.get("sides", ("right", "left", "below", "above")))
        label_side = str(hints.get("labelSide", "right"))
        for lane, relation in enumerate(owner_relations):
            candidate: SelfLoopGeometry | None = None
            for side in sides:
                proposal = _loop_candidate(participants[owner_id], side, lane, relation, measurer, canvas, label_side)
                if not _loop_collides(proposal, canvas, participants, links, placed, occupied_label_bounds):
                    candidate = proposal
                    break
            if candidate is None:
                candidate = _loop_candidate(participants[owner_id], sides[0], lane, relation, measurer, canvas, label_side)
                issues.append(Collision("self-loop-unplaced", relation.id, None, "No collision-free self-loop lane was available"))
            placed.append(candidate)
            occupied_label_bounds.append(candidate.label.text.bounds)
    return tuple(placed), issues


def _heading(view: ViewSpec, canvas: Rect) -> TextBlock:
    measurer = TextMeasurer(68, 78)
    relation = type("Heading", (), {"metadata": {"sequence": ""}, "name": view.title})()
    # A heading is ordinary text without a visible numerical prefix.
    lines = measurer.wrap(view.title, canvas.width - 520)
    width = max(measurer.width(line) for line in lines)
    top = 100.0
    return TextBlock(lines, Rect(230.0, top, width, 18.0 + len(lines) * 78.0), "", 230.0, 230.0, top + 68.0, 78.0, 68.0)


def build_collaboration_render_plan(model: SemanticModel, view: ViewSpec) -> CollaborationRenderPlan:
    layout, composition = layout_for(view.id)
    canvas = Rect(0.0, 0.0, float(layout.width), float(layout.height))
    heading = _heading(view, canvas)
    measurer = TextMeasurer(layout.message_font_size, layout.message_line_height)
    participants = _participant_geometry(model, view, composition, layout, measurer)
    links = _link_geometries(view, participants, canvas)
    relation_map = {relation.id: relation for relation in model.relations}
    relations = tuple(sorted((relation_map[relation_id] for relation_id in view.relations), key=lambda relation: relation.metadata["sequence"]))
    loops, issues = _place_self_loops(relations, composition, participants, links, canvas, measurer)
    occupied_labels = [loop.label.text.bounds for loop in loops]
    occupied_loops = [loop.bounds for loop in loops]
    by_link: dict[str, list[SemanticRelation]] = defaultdict(list)
    for relation in relations:
        if relation.source != relation.target:
            by_link[relation.metadata["structuralLink"]].append(relation)
    pending_runs: dict[str, tuple[str, Rect, tuple[MessageLabelGeometry, ...], tuple[SemanticRelation, ...], str, str]] = {}
    for link_data in view.options["structuralLinks"]:
        link_id = link_data["id"]
        group = tuple(sorted(by_link.get(link_id, []), key=lambda relation: relation.metadata["sequence"]))
        placements = _place_link_runs(link_id, group, composition["links"].get(link_id, {}), links[link_id], canvas, heading.bounds, participants, links, occupied_labels, occupied_loops, measurer)
        if placements is None:
            issues.append(Collision("message-run-unplaced", link_id, None, "No collision-free local message-run lane was available"))
            # Leave a deterministic in-bounds fallback so Q5 can report the exact geometry conflict.
            _, width, height = _group_measure(group, measurer, 1800)
            group_bounds = Rect(120.0, 900.0, width, height)
            labels = _labels_for_group(link_id, group, group_bounds, measurer, 1500, "fallback")
            placements = (("fallback", group_bounds, labels, group),)
        for chunk_index, (side, group_bounds, labels, chunk) in enumerate(placements, start=1):
            run_key = link_id if len(placements) == 1 else f"{link_id}#{chunk_index}"
            pending_runs[run_key] = (side, group_bounds, labels, chunk, link_data["participants"][0], link_id)

    all_label_bounds = [label.text.bounds for loop in loops for label in (loop.label,)]
    all_label_bounds.extend(label.text.bounds for _, _, labels, _, _, _ in pending_runs.values() for label in labels)
    arrows_by_relation: dict[str, ArrowGeometry] = {}
    for link_data in view.options["structuralLinks"]:
        link_id = link_data["id"]
        link_run_records = [record for record in pending_runs.values() if record[5] == link_id]
        link_relations = tuple(relation for _, _, _, chunk, _, _ in link_run_records for relation in chunk)
        link_labels = tuple(label for _, _, labels, _, _, _ in link_run_records for label in labels)
        for arrow in _arrow_geometries(link_id, link_relations, links[link_id], link_data["participants"][0], link_labels, all_label_bounds):
            arrows_by_relation[arrow.relation.id] = arrow
    runs: dict[str, MessageRunGeometry] = {}
    for run_key, (side, group_bounds, labels, group, first_participant_id, link_id) in pending_runs.items():
        arrows = tuple(arrows_by_relation[relation.id] for relation in group)
        runs[run_key] = MessageRunGeometry(link_id, side, group_bounds, labels, arrows)
    return CollaborationRenderPlan(canvas, heading, participants, links, runs, loops, issues)


def layout_metadata(plan: CollaborationRenderPlan) -> dict[str, str]:
    return {
        "data-page-bounds": plan.canvas.data(),
        "data-layout-issue-count": str(len(plan.layout_issues)),
        "data-layout-issues": "|".join(f"{issue.code}:{issue.subject}" for issue in plan.layout_issues),
    }


def link_data(link: StructuralLinkGeometry) -> dict[str, str]:
    return {"data-points": link.polyline.data(), "data-link-bounds": link.polyline.bounds.data()}


def label_data(label: MessageLabelGeometry) -> dict[str, str]:
    return {
        "data-label-bounds": label.text.bounds.data(),
        "data-label-lines": str(len(label.text.lines)),
        "data-label-font-size": f"{label.text.font_size:.2f}",
    }


def arrow_data(arrow: ArrowGeometry) -> dict[str, str]:
    return {
        "data-arrow-segment": arrow.segment.data(),
        "data-arrow-lane": str(arrow.lane),
        "data-arrow-start-distance": f"{arrow.start_distance:.2f}",
        "data-arrow-end-distance": f"{arrow.end_distance:.2f}",
    }


def loop_data(loop: SelfLoopGeometry) -> dict[str, str]:
    return {
        "data-loop-bounds": loop.bounds.data(),
        "data-loop-points": loop.path.data(),
        "data-loop-side": loop.side,
        "data-loop-lane": str(loop.lane),
    }


def parse_rect(value: str) -> Rect:
    return Rect.from_data(value)


def parse_segment(value: str) -> Segment:
    return Segment.from_data(value)


def parse_polyline(value: str) -> Polyline:
    return Polyline.from_data(value)
