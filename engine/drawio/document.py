from __future__ import annotations

import heapq
import math
from dataclasses import dataclass
from typing import Any, Mapping
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class Geometry:
    x: float
    y: float
    width: float
    height: float


@dataclass
class _EdgeRecord:
    cell_id: str
    source: str
    target: str
    cell: ET.Element
    geometry: ET.Element
    explicit_waypoints: tuple[tuple[float, float], ...]


class Document:
    """Small deterministic uncompressed mxGraph document builder."""

    LAYERS = (
        ("layer-background", "01 Background"),
        ("layer-containers", "02 Containers"),
        ("layer-nodes", "03 Nodes"),
        ("layer-relationships", "04 Relationships"),
        ("layer-labels", "05 Labels"),
        ("layer-notes", "06 Notes"),
        ("layer-qa", "99 QA Guides"),
    )

    def __init__(
        self,
        title: str,
        *,
        width: int = 1600,
        height: int = 1000,
        connector_clearance: float = 0,
        routing_options: Mapping[str, Any] | None = None,
    ) -> None:
        self.mxfile = ET.Element("mxfile", {"host": "drawio", "version": "26.0.0"})
        self.diagram = ET.SubElement(self.mxfile, "diagram", {"id": "page-1", "name": title})
        self.model = ET.SubElement(
            self.diagram,
            "mxGraphModel",
            {
                "dx": "1422",
                "dy": "794",
                "grid": "1",
                "gridSize": "10",
                "guides": "1",
                "tooltips": "1",
                "connect": "1",
                "arrows": "1",
                "fold": "1",
                "page": "1",
                "pageScale": "1",
                "pageWidth": str(width),
                "pageHeight": str(height),
                "math": "0",
                "shadow": "0",
            },
        )
        self.root = ET.SubElement(self.model, "root")
        ET.SubElement(self.root, "mxCell", {"id": "0"})
        ET.SubElement(self.root, "mxCell", {"id": "1", "parent": "0"})
        for layer_id, name in self.LAYERS:
            ET.SubElement(self.root, "mxCell", {"id": layer_id, "value": name, "parent": "0"})
        self._ids = {"0", "1", *(item[0] for item in self.LAYERS)}
        self._geometries: dict[str, Geometry] = {}
        self._parents: dict[str, str] = {}
        self._vertex_styles: dict[str, str] = {}
        self._connector_clearance = connector_clearance
        self._routing_options = dict(routing_options or {})
        self._edges: list[_EdgeRecord] = []

    def _reserve(self, cell_id: str) -> None:
        if cell_id in self._ids:
            raise ValueError(f"duplicate draw.io cell id: {cell_id}")
        self._ids.add(cell_id)

    def vertex(
        self,
        cell_id: str,
        label: str,
        style: str,
        geometry: Geometry,
        *,
        parent: str = "layer-nodes",
        metadata: dict[str, str] | None = None,
    ) -> str:
        self._reserve(cell_id)
        self._geometries[cell_id] = geometry
        self._parents[cell_id] = parent
        self._vertex_styles[cell_id] = style
        attrs = {"id": cell_id, "label": label, **(metadata or {})}
        wrapper = ET.SubElement(self.root, "object", attrs)
        cell = ET.SubElement(wrapper, "mxCell", {"style": style, "vertex": "1", "parent": parent})
        ET.SubElement(
            cell,
            "mxGeometry",
            {
                "x": str(geometry.x),
                "y": str(geometry.y),
                "width": str(geometry.width),
                "height": str(geometry.height),
                "as": "geometry",
            },
        )
        return cell_id

    def edge(
        self,
        cell_id: str,
        source: str,
        target: str,
        label: str,
        style: str,
        *,
        waypoints: tuple[tuple[float, float], ...] = (),
    ) -> str:
        self._reserve(cell_id)
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cell_id,
                "value": label,
                "style": style,
                "edge": "1",
                "parent": "layer-relationships",
                "source": source,
                "target": target,
            },
        )
        geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        self._edges.append(
            _EdgeRecord(cell_id, source, target, cell, geometry, tuple(waypoints))
        )
        return cell_id

    def _absolute_geometry(self, cell_id: str) -> Geometry:
        geometry = self._geometries[cell_id]
        parent = self._parents[cell_id]
        if parent in self._geometries:
            owner = self._absolute_geometry(parent)
            return Geometry(
                owner.x + geometry.x,
                owner.y + geometry.y,
                geometry.width,
                geometry.height,
            )
        return geometry

    def edge_label(
        self,
        cell_id: str,
        edge_id: str,
        label: str,
        position: float,
        *,
        style: str | None = None,
        offset: tuple[float, float] = (0, 0),
    ) -> str:
        self._reserve(cell_id)
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cell_id,
                "value": label,
                "style": style
                or "edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];",
                "vertex": "1",
                "connectable": "0",
                "parent": edge_id,
            },
        )
        geometry = ET.SubElement(
            cell,
            "mxGeometry",
            {"x": str(position), "relative": "1", "as": "geometry"},
        )
        ET.SubElement(
            geometry,
            "mxPoint",
            {"x": str(offset[0]), "y": str(offset[1]), "as": "offset"},
        )
        return cell_id

    @staticmethod
    def _style_values(style: str) -> dict[str, str]:
        values: dict[str, str] = {}
        for token in filter(None, style.split(";")):
            key, separator, value = token.partition("=")
            values[key] = value if separator else "1"
        return values

    @staticmethod
    def _set_style_values(style: str, **updates: float) -> str:
        values = Document._style_values(style)
        values.update({key: f"{value:g}" for key, value in updates.items()})
        return ";".join(f"{key}={value}" for key, value in values.items()) + ";"

    def _routing_number(self, name: str, default: float, *aliases: str) -> float:
        containers = [self._routing_options]
        for key in ("scoring", "weights", "costs", "router", "orthogonal"):
            value = self._routing_options.get(key)
            if isinstance(value, Mapping):
                containers.append(value)
                nested = value.get("weights")
                if isinstance(nested, Mapping):
                    containers.append(nested)
        for container in containers:
            for key in (name, *aliases):
                value = container.get(key)
                if isinstance(value, (int, float)):
                    return float(value)
        return default

    @staticmethod
    def _centre(box: Geometry) -> tuple[float, float]:
        return box.x + box.width / 2, box.y + box.height / 2

    def _side_facing(self, source: Geometry, target: Geometry) -> str:
        sx, sy = self._centre(source)
        tx, ty = self._centre(target)
        dx, dy = tx - sx, ty - sy
        if abs(dx) >= abs(dy):
            return "E" if dx >= 0 else "W"
        return "S" if dy >= 0 else "N"

    def _assign_ports(self) -> dict[tuple[str, str], tuple[float, float]]:
        groups: dict[tuple[str, str], list[tuple[_EdgeRecord, str, Geometry]]] = {}
        for edge in self._edges:
            source = self._absolute_geometry(edge.source)
            target = self._absolute_geometry(edge.target)
            style = self._style_values(edge.cell.get("style", ""))
            for end, node, peer, box, peer_box in (
                ("source", edge.source, edge.target, source, target),
                ("target", edge.target, edge.source, target, source),
            ):
                prefix = "exit" if end == "source" else "entry"
                if prefix + "X" in style and prefix + "Y" in style:
                    continue
                side = self._side_facing(box, peer_box)
                groups.setdefault((node, side), []).append((edge, end, peer_box))

        ports: dict[tuple[str, str], tuple[float, float]] = {}
        for (_, side), ends in sorted(groups.items()):
            horizontal = side in {"N", "S"}
            ends.sort(
                key=lambda item: (
                    self._centre(item[2])[0 if horizontal else 1],
                    self._centre(item[2])[1 if horizontal else 0],
                    item[0].cell_id,
                    item[1],
                )
            )
            for index, (edge, end, _) in enumerate(ends):
                slot = (index + 1) / (len(ends) + 1)
                if side == "N":
                    port = (slot, 0.0)
                elif side == "S":
                    port = (slot, 1.0)
                elif side == "W":
                    port = (0.0, slot)
                else:
                    port = (1.0, slot)
                ports[(edge.cell_id, end)] = port
                prefix = "exit" if end == "source" else "entry"
                edge.cell.set(
                    "style",
                    self._set_style_values(
                        edge.cell.get("style", ""),
                        **{
                            prefix + "X": port[0],
                            prefix + "Y": port[1],
                            prefix + "Dx": 0,
                            prefix + "Dy": 0,
                        },
                    ),
                )
        return ports

    def _endpoint(self, edge: _EdgeRecord, end: str) -> tuple[float, float]:
        cell_id = edge.source if end == "source" else edge.target
        box = self._absolute_geometry(cell_id)
        style = self._style_values(edge.cell.get("style", ""))
        prefix = "exit" if end == "source" else "entry"
        x = float(style.get(prefix + "X", 0.5))
        y = float(style.get(prefix + "Y", 0.5))
        return box.x + x * box.width, box.y + y * box.height

    def _leaf_obstacles(self, excluded: set[str]) -> list[tuple[str, Geometry, Geometry]]:
        containers = set(self._parents.values())
        result = []
        for cell_id in sorted(self._geometries):
            if cell_id in excluded or cell_id in containers:
                continue
            box = self._absolute_geometry(cell_id)
            if self._style_values(self._vertex_styles.get(cell_id, "")).get("shape") == "umlActor":
                label_clearance = self._routing_number("actor_label_clearance", 0)
                box = Geometry(box.x, box.y, box.width, box.height + label_clearance)
            clearance = self._connector_clearance
            result.append(
                (
                    cell_id,
                    box,
                    Geometry(
                        box.x - clearance,
                        box.y - clearance,
                        box.width + 2 * clearance,
                        box.height + 2 * clearance,
                    ),
                )
            )
        return result

    def _shared_container(self, source: str, target: str) -> Geometry | None:
        source_parent = self._parents.get(source)
        target_parent = self._parents.get(target)
        if source_parent == target_parent and source_parent in self._geometries:
            return self._absolute_geometry(source_parent)
        return None

    @staticmethod
    def _inside(point: tuple[float, float], box: Geometry) -> bool:
        return box.x < point[0] < box.x + box.width and box.y < point[1] < box.y + box.height

    @staticmethod
    def _segment_hits_box(
        first: tuple[float, float], second: tuple[float, float], box: Geometry
    ) -> bool:
        if first[0] == second[0]:
            return (
                box.x < first[0] < box.x + box.width
                and max(first[1], second[1]) > box.y
                and min(first[1], second[1]) < box.y + box.height
            )
        return (
            box.y < first[1] < box.y + box.height
            and max(first[0], second[0]) > box.x
            and min(first[0], second[0]) < box.x + box.width
        )

    @staticmethod
    def _segments_cross(
        first: tuple[float, float],
        second: tuple[float, float],
        other_first: tuple[float, float],
        other_second: tuple[float, float],
    ) -> bool:
        if first[0] == second[0] and other_first[1] == other_second[1]:
            return (
                min(first[1], second[1]) < other_first[1] < max(first[1], second[1])
                and min(other_first[0], other_second[0])
                < first[0]
                < max(other_first[0], other_second[0])
            )
        if first[1] == second[1] and other_first[0] == other_second[0]:
            return (
                min(first[0], second[0]) < other_first[0] < max(first[0], second[0])
                and min(other_first[1], other_second[1])
                < first[1]
                < max(other_first[1], other_second[1])
            )
        return False

    @staticmethod
    def _parallel_overlap(
        first: tuple[float, float],
        second: tuple[float, float],
        other_first: tuple[float, float],
        other_second: tuple[float, float],
        proximity: float,
    ) -> float:
        if first[0] == second[0] and other_first[0] == other_second[0]:
            if abs(first[0] - other_first[0]) > proximity:
                return 0.0
            return max(
                0.0,
                min(max(first[1], second[1]), max(other_first[1], other_second[1]))
                - max(min(first[1], second[1]), min(other_first[1], other_second[1])),
            )
        if first[1] == second[1] and other_first[1] == other_second[1]:
            if abs(first[1] - other_first[1]) > proximity:
                return 0.0
            return max(
                0.0,
                min(max(first[0], second[0]), max(other_first[0], other_second[0]))
                - max(min(first[0], second[0]), min(other_first[0], other_second[0])),
            )
        return 0.0

    @staticmethod
    def _segment_box_distance(
        first: tuple[float, float], second: tuple[float, float], box: Geometry
    ) -> float:
        if first[0] == second[0]:
            dx = max(box.x - first[0], 0.0, first[0] - (box.x + box.width))
            low, high = sorted((first[1], second[1]))
            dy = max(box.y - high, 0.0, low - (box.y + box.height))
        else:
            dy = max(box.y - first[1], 0.0, first[1] - (box.y + box.height))
            low, high = sorted((first[0], second[0]))
            dx = max(box.x - high, 0.0, low - (box.x + box.width))
        return math.hypot(dx, dy)

    def _container_boxes(self) -> list[Geometry]:
        containers = set(self._parents.values())
        return [
            self._absolute_geometry(cell_id)
            for cell_id in sorted(containers)
            if cell_id in self._geometries
        ]

    def _segment_cost(
        self,
        first: tuple[float, float],
        second: tuple[float, float],
        direction: str | None,
        routed: list[tuple[tuple[float, float], ...]],
        obstacles: list[tuple[str, Geometry, Geometry]],
        boundaries: list[Geometry],
    ) -> float:
        length = abs(second[0] - first[0]) + abs(second[1] - first[1])
        next_direction = "V" if first[0] == second[0] else "H"
        clearance = max(self._connector_clearance, 1.0)
        cost = length * self._routing_number("length", 1.0, "route_length")
        if direction is not None and direction != next_direction:
            cost += self._routing_number("bends", clearance * 2, "bend")
        crossing_weight = self._routing_number(
            "crossings", clearance * 20, "crossing", "edge_crossing"
        )
        congestion_weight = self._routing_number(
            "congestion", 4.0, "overlap", "shared_segment"
        )
        for route in routed:
            for other_first, other_second in zip(route, route[1:], strict=False):
                if self._segments_cross(first, second, other_first, other_second):
                    cost += crossing_weight
                overlap = self._parallel_overlap(
                    first, second, other_first, other_second, clearance
                )
                cost += overlap * congestion_weight
        clearance_weight = self._routing_number(
            "obstacle_clearance", 2.0, "clearance", "obstacleClearance"
        )
        preferred = clearance * 2
        for _, original, _ in obstacles:
            distance = self._segment_box_distance(first, second, original)
            cost += max(0.0, preferred - distance) * clearance_weight
        boundary_weight = self._routing_number(
            "boundary_hugging", 3.0, "boundary", "boundaryHugging", "boundary_crossing"
        )
        for box in boundaries:
            if first[0] == second[0]:
                distance = min(abs(first[0] - box.x), abs(first[0] - box.x - box.width))
                overlap = max(
                    0.0,
                    min(max(first[1], second[1]), box.y + box.height)
                    - max(min(first[1], second[1]), box.y),
                )
            else:
                distance = min(abs(first[1] - box.y), abs(first[1] - box.y - box.height))
                overlap = max(
                    0.0,
                    min(max(first[0], second[0]), box.x + box.width)
                    - max(min(first[0], second[0]), box.x),
                )
            if distance <= clearance:
                cost += overlap * boundary_weight
        return cost

    def _route(
        self,
        edge: _EdgeRecord,
        routed: list[tuple[tuple[float, float], ...]],
    ) -> tuple[tuple[float, float], ...]:
        start = self._endpoint(edge, "source")
        end = self._endpoint(edge, "target")
        obstacles = self._leaf_obstacles({edge.source, edge.target})
        boundaries = self._container_boxes()
        clearance = max(self._connector_clearance, 1.0)
        boxes = [item[2] for item in obstacles]
        all_boxes = [self._absolute_geometry(item) for item in self._geometries]
        shared_container = self._shared_container(edge.source, edge.target)
        corridor = self._routing_number(
            "corridor", 2 * clearance, "routing_corridor", "outer_corridor"
        )
        min_x = min([start[0], end[0], *(box.x for box in all_boxes)]) - corridor
        max_x = max([start[0], end[0], *(box.x + box.width for box in all_boxes)]) + corridor
        min_y = min([start[1], end[1], *(box.y for box in all_boxes)]) - corridor
        max_y = max([start[1], end[1], *(box.y + box.height for box in all_boxes)]) + corridor
        xs = sorted({start[0], end[0], min_x, max_x, *(v for box in boxes for v in (box.x, box.x + box.width))})
        ys = sorted({start[1], end[1], min_y, max_y, *(v for box in boxes for v in (box.y, box.y + box.height))})
        x_index = {value: index for index, value in enumerate(xs)}
        y_index = {value: index for index, value in enumerate(ys)}
        start_node = (x_index[start[0]], y_index[start[1]])
        end_node = (x_index[end[0]], y_index[end[1]])
        valid_cache: dict[tuple[int, int], bool] = {}

        def point(node: tuple[int, int]) -> tuple[float, float]:
            return xs[node[0]], ys[node[1]]

        def valid(node: tuple[int, int]) -> bool:
            if node not in valid_cache:
                value = point(node)
                inside_container = (
                    shared_container is None
                    or shared_container.x <= value[0] <= shared_container.x + shared_container.width
                    and shared_container.y <= value[1] <= shared_container.y + shared_container.height
                )
                valid_cache[node] = inside_container and not any(
                    self._inside(value, box) for box in boxes
                )
            return valid_cache[node]

        queue: list[tuple[float, int, tuple[int, int], str | None]] = []
        heapq.heappush(queue, (0.0, 0, start_node, None))
        distance: dict[tuple[tuple[int, int], str | None], float] = {(start_node, None): 0.0}
        previous: dict[
            tuple[tuple[int, int], str | None], tuple[tuple[int, int], str | None]
        ] = {}
        serial = 0
        final: tuple[tuple[int, int], str | None] | None = None
        while queue:
            cost, _, node, direction = heapq.heappop(queue)
            state = (node, direction)
            if cost != distance.get(state):
                continue
            if node == end_node:
                final = state
                break
            for dx, dy, next_direction in ((-1, 0, "H"), (1, 0, "H"), (0, -1, "V"), (0, 1, "V")):
                neighbour = (node[0] + dx, node[1] + dy)
                if not (0 <= neighbour[0] < len(xs) and 0 <= neighbour[1] < len(ys)):
                    continue
                if not valid(neighbour):
                    continue
                first, second = point(node), point(neighbour)
                if any(self._segment_hits_box(first, second, box) for box in boxes):
                    continue
                next_cost = cost + self._segment_cost(
                    first, second, direction, routed, obstacles, boundaries
                )
                next_state = (neighbour, next_direction)
                if next_cost >= distance.get(next_state, math.inf):
                    continue
                distance[next_state] = next_cost
                previous[next_state] = state
                serial += 1
                heapq.heappush(queue, (next_cost, serial, neighbour, next_direction))
        if final is None:
            raise ValueError(
                f"no collision-free orthogonal route from {edge.source} to {edge.target}"
            )
        states = [final]
        while states[-1] in previous:
            states.append(previous[states[-1]])
        points = [point(state[0]) for state in reversed(states)]
        simplified = [points[0]]
        for value in points[1:]:
            if len(simplified) >= 2:
                first, second = simplified[-2], simplified[-1]
                if (first[0] == second[0] == value[0]) or (
                    first[1] == second[1] == value[1]
                ):
                    simplified[-1] = value
                    continue
            simplified.append(value)
        return tuple(simplified)

    @staticmethod
    def _write_waypoints(
        geometry: ET.Element, waypoints: tuple[tuple[float, float], ...]
    ) -> None:
        existing = geometry.find("Array[@as='points']")
        if existing is not None:
            geometry.remove(existing)
        if not waypoints:
            return
        points = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in waypoints:
            ET.SubElement(points, "mxPoint", {"x": f"{x:g}", "y": f"{y:g}"})

    def _route_edges(self) -> None:
        if not self._edges:
            return
        self._assign_ports()
        routed: list[tuple[tuple[float, float], ...]] = []
        def priority(item: _EdgeRecord) -> tuple[bool, bool, float, str]:
            style = self._style_values(item.cell.get("style", ""))
            source = self._centre(self._absolute_geometry(item.source))
            target = self._centre(self._absolute_geometry(item.target))
            distance = abs(target[0] - source[0]) + abs(target[1] - source[1])
            return (
                not item.explicit_waypoints,
                style.get("dashed") != "1",
                distance,
                item.cell_id,
            )

        ordered = sorted(self._edges, key=priority)
        for edge in ordered:
            if edge.explicit_waypoints:
                full_route = (
                    self._endpoint(edge, "source"),
                    *edge.explicit_waypoints,
                    self._endpoint(edge, "target"),
                )
            else:
                full_route = self._route(edge, routed)
            self._write_waypoints(edge.geometry, tuple(full_route[1:-1]))
            routed.append(tuple(full_route))

    def to_bytes(self) -> bytes:
        self._route_edges()
        ET.indent(self.mxfile, space="  ")
        return ET.tostring(
            self.mxfile, encoding="utf-8", xml_declaration=True, short_empty_elements=True
        )

    def write(self, path: str) -> None:
        from pathlib import Path

        Path(path).write_bytes(self.to_bytes())
