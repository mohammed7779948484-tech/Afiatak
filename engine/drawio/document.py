from __future__ import annotations

from dataclasses import dataclass
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class Geometry:
    x: float
    y: float
    width: float
    height: float


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
        self._connector_clearance = connector_clearance

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
        if not waypoints:
            source_box = self._absolute_geometry(source)
            target_box = self._absolute_geometry(target)
            sx = source_box.x + source_box.width / 2
            sy = source_box.y + source_box.height / 2
            tx = target_box.x + target_box.width / 2
            ty = target_box.y + target_box.height / 2
            if abs(tx - sx) >= abs(ty - sy):
                middle = (sx + tx) / 2
                primary = ((middle, sy), (middle, ty))
            else:
                middle = (sy + ty) / 2
                primary = ((sx, middle), (tx, middle))
            top, bottom = self._outer_y(-40), self._outer_y(40)
            left, right = self._outer_x(-40), self._outer_x(40)
            candidates = [
                primary,
                ((sx, top), (tx, top)),
                ((sx, bottom), (tx, bottom)),
                ((left, sy), (left, ty)),
                ((right, sy), (right, ty)),
            ]
            selected = next(
                (
                    candidate
                    for candidate in candidates
                    if not self._route_hits((sx, sy), (tx, ty), candidate, {source, target})
                ),
                None,
            )
            if selected is None:
                raise ValueError(f"no collision-free orthogonal route from {source} to {target}")
            waypoints = selected
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
        if waypoints:
            points = ET.SubElement(geometry, "Array", {"as": "points"})
            for x, y in waypoints:
                ET.SubElement(points, "mxPoint", {"x": str(x), "y": str(y)})
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

    def _outer_x(self, padding: float) -> float:
        boxes = [self._absolute_geometry(item) for item in self._geometries]
        return (
            min(item.x for item in boxes) + padding
            if padding < 0
            else max(item.x + item.width for item in boxes) + padding
        )

    def _outer_y(self, padding: float) -> float:
        boxes = [self._absolute_geometry(item) for item in self._geometries]
        return (
            min(item.y for item in boxes) + padding
            if padding < 0
            else max(item.y + item.height for item in boxes) + padding
        )

    def _route_hits(self, start, end, waypoints, excluded: set[str]) -> bool:
        points = (start, *waypoints, end)
        containers = set(self._parents.values())
        for cell_id in self._geometries:
            owner = cell_id
            owned_by_endpoint = False
            while owner in self._parents:
                owner = self._parents[owner]
                if owner in excluded:
                    owned_by_endpoint = True
                    break
            if cell_id in excluded or cell_id in containers or owned_by_endpoint:
                continue
            box = self._absolute_geometry(cell_id)
            clearance = self._connector_clearance
            box = Geometry(
                box.x - clearance,
                box.y - clearance,
                box.width + 2 * clearance,
                box.height + 2 * clearance,
            )
            for first, second in zip(points, points[1:], strict=False):
                if first[0] == second[0]:
                    if (
                        box.x < first[0] < box.x + box.width
                        and max(first[1], second[1]) > box.y
                        and min(first[1], second[1]) < box.y + box.height
                    ):
                        return True
                elif (
                    first[1] == second[1]
                    and box.y < first[1] < box.y + box.height
                    and max(first[0], second[0]) > box.x
                    and min(first[0], second[0]) < box.x + box.width
                ):
                    return True
        return False

    def edge_label(self, cell_id: str, edge_id: str, label: str, position: float) -> str:
        self._reserve(cell_id)
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cell_id,
                "value": label,
                "style": "edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];",
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
        ET.SubElement(geometry, "mxPoint", {"as": "offset"})
        return cell_id

    def to_bytes(self) -> bytes:
        ET.indent(self.mxfile, space="  ")
        return ET.tostring(
            self.mxfile, encoding="utf-8", xml_declaration=True, short_empty_elements=True
        )

    def write(self, path: str) -> None:
        from pathlib import Path

        Path(path).write_bytes(self.to_bytes())
