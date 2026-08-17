from engine.core.ids import drawio_id
from engine.core.models import SemanticElement
from engine.renderers.base import BaseRenderer


class ActivityRenderer(BaseRenderer):
    diagram_type = "activity"

    def shape_for(self, element: SemanticElement) -> str:
        return {
            "initial": "ellipse;aspect=fixed",
            "final": "ellipse;aspect=fixed;strokeWidth=3",
            "decision": "rhombus",
            "fork": "shape=line;strokeWidth=6",
            "join": "shape=line;strokeWidth=6",
        }.get(element.type, "rounded=1")

    def render(self, model, view):
        profile = self.profile(view)
        if profile["orientation"] != "TB":
            raise ValueError("activity layout profile must use TB orientation")
        elements, relations = self.selected(model, view)
        document = self.new_document(view.title)
        geometries = self.layout.grid(elements, columns=1, origin=(650, 100), gap=(0, 90))
        for element in elements:
            document.vertex(
                drawio_id(element.id),
                element.name,
                self.design.node(self.role_for(element), self.shape_for(element)),
                geometries[element.id],
                metadata={"semanticId": element.id, "semanticType": element.type},
            )
        for relation in relations:
            document.edge(
                f"sem-{relation.id}",
                drawio_id(relation.source),
                drawio_id(relation.target),
                relation.name,
                self.design.edge("control_flow"),
            )
        return document
