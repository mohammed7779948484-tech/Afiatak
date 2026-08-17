from __future__ import annotations

from pathlib import Path
from typing import Any

from engine.core.io import ROOT, load_yaml


def parse_style(style: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for token in filter(None, style.split(";")):
        key, separator, value = token.partition("=")
        result[key] = value if separator else "1"
    return result


def compile_style(*parts: str, **values: Any) -> str:
    tokens: dict[str, str] = {}
    for part in parts:
        tokens.update(parse_style(part))
    tokens.update({key: str(value) for key, value in values.items() if value is not None})
    return ";".join(f"{key}={value}" for key, value in tokens.items()) + ";"


class DesignSystem:
    def __init__(self, root: Path = ROOT / "design") -> None:
        self.palette = load_yaml(root / "palette.yaml")["colors"]
        self.typography = load_yaml(root / "typography.yaml")
        self.geometry = load_yaml(root / "geometry.yaml")
        self.routing = load_yaml(root / "routing.yaml")

    def node(self, role: str = "primary", shape: str = "rounded=1") -> str:
        fill_key = f"{role}_fill" if f"{role}_fill" in self.palette else "primary_fill"
        stroke_key = f"{role}_stroke" if f"{role}_stroke" in self.palette else "primary_stroke"
        return compile_style(
            shape,
            "whiteSpace=wrap;html=1;align=center;verticalAlign=middle",
            fillColor=self.palette[fill_key],
            strokeColor=self.palette[stroke_key],
            fontColor=self.palette["ink"],
            fontFamily=self.typography["font_family"],
            fontSize=self.typography["node"]["size"],
        )

    def edge(self, relation_type: str) -> str:
        directed = {
            "control_flow": "endArrow=block;endFill=1",
            "transition": "endArrow=block;endFill=1",
            "message": "endArrow=block;endFill=1",
            "communication_path": "endArrow=none",
            "connector": "endArrow=none",
        }
        return compile_style(
            self.routing["default"],
            directed.get(
                relation_type,
                self.routing.get(relation_type, self.routing["association"]),
            ),
            self.routing["label"],
            strokeColor=self.palette["border"],
            fontColor=self.palette["ink"],
        )
