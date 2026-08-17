from engine.core.ids import drawio_id
from engine.core.models import SemanticElement
from engine.renderers.base import BaseRenderer


class StateRenderer(BaseRenderer):
    diagram_type = "state"

    def shape_for(self, element: SemanticElement) -> str:
        return {
            "initial": "ellipse;aspect=fixed;fillColor=#1F2937",
            "final": "ellipse;aspect=fixed;strokeWidth=3",
        }.get(element.type, "rounded=1")

    def render(self, model, view):
        profile = self.profile(view)
        if profile["orientation"] != "LR":
            raise ValueError("state layout profile must use LR orientation")
        elements, relations = self.selected(model, view)
        document = self.new_document(view.title)
        geometries = self.layout.grid(
            elements,
            columns=max(1, len(elements)),
            origin=(120, 360),
            gap=(130, 0),
        )
        for element in elements:
            document.vertex(
                drawio_id(element.id),
                element.name,
                self.design.node("primary", self.shape_for(element)),
                geometries[element.id],
                metadata={"semanticId": element.id, "semanticType": element.type},
            )
        for relation in relations:
            document.edge(
                f"sem-{relation.id}",
                drawio_id(relation.source),
                drawio_id(relation.target),
                relation.name,
                self.design.edge("transition"),
            )
        return document
