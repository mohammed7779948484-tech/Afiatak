from engine.core.models import SemanticElement
from engine.renderers.base import BaseRenderer


class ObjectRenderer(BaseRenderer):
    diagram_type = "object"
    default_shape = "rounded=0;fontStyle=4"

    def label_for(self, element: SemanticElement) -> str:
        values = element.metadata.get("values", {})
        return "\n".join([element.name, *(f"{key} = {value}" for key, value in values.items())])
