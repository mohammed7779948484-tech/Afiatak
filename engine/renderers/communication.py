from engine.renderers.base import BaseRenderer


class CommunicationRenderer(BaseRenderer):
    diagram_type = "communication"

    def relation_label(self, relation):
        sequence = relation.metadata.get("sequence", "?")
        return f"{sequence}: {relation.name or relation.type}"
