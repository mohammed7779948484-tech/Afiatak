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
        self.root = root
        palette = load_yaml(root / "palette.yaml")
        self.palette = palette["colors"]
        self.palette_roles = palette.get("roles", {})
        self.typography = load_yaml(root / "typography.yaml")
        self.geometry = load_yaml(root / "geometry.yaml")
        self.appearance = load_yaml(root / "appearance.yaml")
        self.routing = load_yaml(root / "routing.yaml")
        self._profiles: dict[str, dict[str, Any]] = {}

    def node(self, role: str = "primary", shape: str = "rounded=1") -> str:
        return self.semantic_node(role, shape)

    def semantic_node(
        self,
        role: str = "primary",
        shape: str = "rounded=1",
        *,
        profile: str | None = None,
        text_role: str = "node",
        appearance_role: str | None = None,
    ) -> str:
        role = self.visual_role(profile, "nodes", role)
        node_roles = self.palette_roles.get("nodes", {})
        colors = node_roles.get(role, node_roles.get("primary", {}))
        typography = self.typography_role(text_role)
        appearance = self._appearance("node", appearance_role or role)
        return compile_style(
            shape,
            "whiteSpace=wrap;html=1;align=center;verticalAlign=middle",
            fillColor=self._color(colors.get("fill", "primary_fill")),
            strokeColor=self._color(colors.get("stroke", "primary_stroke")),
            strokeWidth=appearance.get("stroke_width"),
            opacity=appearance.get("opacity"),
            dashed=1 if appearance.get("dashed") else None,
            fontColor=self.palette[typography.get("color", "ink")],
            fontFamily=self.typography["font_family"],
            fontSize=typography["size"],
            fontStyle=1 if typography.get("bold") else 0,
        )

    def edge(self, relation_type: str) -> str:
        return self.semantic_edge(relation_type)

    def semantic_edge(self, role: str, *, profile: str | None = None) -> str:
        role = self.visual_role(profile, "edges", role)
        directed = {
            "control_flow": "endArrow=block;endFill=1",
            "transition": "endArrow=block;endFill=1",
            "message": "endArrow=block;endFill=1",
            "communication_path": "endArrow=none",
            "connector": "endArrow=none",
        }
        relation_style = directed.get(role, self.routing.get(role, self.routing["association"]))
        edge_role = role if role in self.palette_roles.get("edges", {}) else (
            "dependency" if role in {"include", "extend"} else "association"
        )
        color_key = self.palette_roles.get("edges", {}).get(edge_role, "border")
        appearance = self._appearance("edge", role)
        typography = self.typography_role("stereotype" if role in {"include", "extend"} else "edge")
        return compile_style(
            self.routing["default"],
            relation_style,
            self.routing["label"],
            strokeColor=self.palette[color_key],
            strokeWidth=appearance.get("stroke_width"),
            opacity=appearance.get("opacity"),
            labelBackgroundColor=self.background(profile=profile),
            fontColor=self.palette[typography.get("color", "ink")],
            fontFamily=self.typography["font_family"],
            fontSize=typography["size"],
        )

    def semantic_text(
        self,
        role: str,
        *,
        profile: str | None = None,
        align: str = "center",
        vertical_align: str = "middle",
    ) -> str:
        role = self.visual_role(profile, "text", role)
        typography = self.typography_role(role)
        return compile_style(
            "text;html=1;strokeColor=none;fillColor=none",
            align=align,
            verticalAlign=vertical_align,
            fontFamily=self.typography["font_family"],
            fontSize=typography["size"],
            fontStyle=1 if typography.get("bold") else 0,
            fontColor=self.palette[typography.get("color", "ink")],
            opacity=self.appearance["defaults"]["text"]["opacity"],
        )

    node_style = semantic_node
    text_style = semantic_text
    edge_style = semantic_edge

    def typography_role(self, role: str) -> dict[str, Any]:
        roles = self.typography.get("roles", {})
        return roles.get(role, roles.get("node", self.typography["node"]))

    def background(self, role: str = "default", *, profile: str | None = None) -> str:
        if profile is not None:
            composition = self.profile(profile).get("composition")
            if composition:
                role = composition.replace("-", "_")
        color_key = self.palette_roles.get("background", {}).get(role, "canvas")
        return self.palette[color_key]

    def profile(self, name: str) -> dict[str, Any]:
        if name not in self._profiles:
            self._profiles[name] = load_yaml(self.root / "profiles" / f"{name}.yaml")
        return self._profiles[name]

    def planner(self, profile: str) -> dict[str, Any]:
        return self.profile(profile).get("planner", {})

    def visual_role(self, profile: str | None, kind: str, role: str) -> str:
        if profile is None:
            return role
        mappings = self.profile(profile).get("visual_roles", {})
        return mappings.get(kind, {}).get(role, role)

    def _appearance(self, kind: str, role: str) -> dict[str, Any]:
        defaults = dict(self.appearance["defaults"][kind])
        defaults.update(self.appearance.get("roles", {}).get(f"{kind}s", {}).get(role, {}))
        if kind == "edge" and role in {"include", "extend"}:
            defaults.update(self.appearance.get("roles", {}).get("edges", {}).get(role, {}))
        return defaults

    def _color(self, token: str) -> str:
        return self.palette.get(token, token)
