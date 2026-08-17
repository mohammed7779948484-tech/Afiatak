from __future__ import annotations

from engine.core.ids import drawio_id
from engine.core.io import ROOT, load_yaml
from engine.core.models import SemanticElement, SemanticModel, SemanticRelation, ViewSpec
from engine.drawio import Document
from engine.drawio.styles import DesignSystem
from engine.layout import LayoutEngine


class BaseRenderer:
    diagram_type = "base"
    default_shape = "rounded=1"
    default_role = "primary"

    def __init__(self, design: DesignSystem | None = None) -> None:
        self.design = design or DesignSystem()
        self.layout = LayoutEngine()

    def profile(self, view: ViewSpec) -> dict:
        path = ROOT / "design" / "profiles" / f"{view.layout_profile}.yaml"
        if not path.is_file():
            raise ValueError(f"unknown layout profile: {view.layout_profile}")
        profile = load_yaml(path)
        if profile.get("diagram_type") != view.diagram_type:
            raise ValueError(
                f"layout profile {view.layout_profile} is for {profile.get('diagram_type')}"
            )
        return profile

    def new_document(self, title: str) -> Document:
        clearance = self.design.geometry["quality"]["minimum_connector_clearance"]
        return Document(title, connector_clearance=float(clearance))

    def selected(
        self, model: SemanticModel, view: ViewSpec
    ) -> tuple[list[SemanticElement], list[SemanticRelation]]:
        by_id = model.by_id
        elements = [by_id[item] for item in view.include if item in by_id]
        rel_by_id = {relation.id: relation for relation in model.relations}
        relations = [rel_by_id[item] for item in view.relations if item in rel_by_id]
        return elements, relations

    def shape_for(self, element: SemanticElement) -> str:
        return self.default_shape

    def role_for(self, element: SemanticElement) -> str:
        return self.default_role

    def label_for(self, element: SemanticElement) -> str:
        return element.name

    def render(self, model: SemanticModel, view: ViewSpec) -> Document:
        profile = self.profile(view)
        elements, relations = self.selected(model, view)
        document = self.new_document(view.title)
        columns = 4 if profile["orientation"] == "LR" else 2
        geometries = self.layout.grid(elements, columns=columns)
        for element in elements:
            document.vertex(
                drawio_id(element.id),
                self.label_for(element),
                self.design.node(self.role_for(element), self.shape_for(element)),
                geometries[element.id],
                metadata={"semanticId": element.id, "semanticType": element.type},
            )
        for relation in relations:
            document.edge(
                f"sem-{relation.id}",
                drawio_id(relation.source),
                drawio_id(relation.target),
                relation.name or self.relation_label(relation),
                self.design.edge(relation.type),
            )
        return document

    def relation_label(self, relation: SemanticRelation) -> str:
        return relation.type.replace("_", " ")
