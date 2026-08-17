from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceRef:
    source: str
    section: str | None = None
    heading: str | None = None
    page: int | None = None
    line_start: int | None = None
    line_end: int | None = None
    requirement_id: str | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SourceRef:
        return cls(**value)


@dataclass(frozen=True)
class SemanticElement:
    id: str
    name: str
    type: str
    description: str
    status: str = "approved"
    source_refs: tuple[SourceRef, ...] = ()
    tags: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SemanticElement:
        data = dict(value)
        data["source_refs"] = tuple(SourceRef.from_dict(v) for v in data.pop("sourceRefs", []))
        data["tags"] = tuple(data.get("tags", []))
        return cls(**data)


@dataclass(frozen=True)
class SemanticRelation:
    id: str
    type: str
    source: str
    target: str
    name: str = ""
    source_refs: tuple[SourceRef, ...] = ()
    rationale: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SemanticRelation:
        data = dict(value)
        data["source_refs"] = tuple(SourceRef.from_dict(v) for v in data.pop("sourceRefs", []))
        return cls(**data)


@dataclass(frozen=True)
class SemanticModel:
    model_id: str
    version: str
    elements: tuple[SemanticElement, ...]
    relations: tuple[SemanticRelation, ...]
    test_data: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SemanticModel:
        return cls(
            model_id=value["modelId"],
            version=str(value["version"]),
            elements=tuple(SemanticElement.from_dict(v) for v in value.get("elements", [])),
            relations=tuple(SemanticRelation.from_dict(v) for v in value.get("relations", [])),
            test_data=bool(value.get("testData", False)),
        )

    @property
    def by_id(self) -> dict[str, SemanticElement]:
        return {item.id: item for item in self.elements}


@dataclass(frozen=True)
class ViewSpec:
    id: str
    title: str
    diagram_type: str
    model: str
    include: tuple[str, ...]
    relations: tuple[str, ...]
    layout_profile: str
    output_targets: tuple[str, ...] = ("drawio",)
    approval: str = "draft"
    visual_review: dict[str, Any] | None = None
    options: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ViewSpec:
        return cls(
            id=value["id"],
            title=value["title"],
            diagram_type=value["diagramType"],
            model=value["model"],
            include=tuple(value.get("include", [])),
            relations=tuple(value.get("relations", [])),
            layout_profile=value.get("layoutProfile", value["diagramType"]),
            output_targets=tuple(value.get("outputTargets", ["drawio"])),
            approval=value.get("approval", "draft"),
            visual_review=value.get("visualReview"),
            options=dict(value.get("options", {})),
        )
