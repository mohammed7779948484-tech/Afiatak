from __future__ import annotations

import math

from engine.core.models import SemanticElement
from engine.drawio.document import Geometry


class LayoutEngine:
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
