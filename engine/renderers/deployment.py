from engine.core.ids import drawio_id
from engine.drawio import Geometry
from engine.renderers.base import BaseRenderer


class DeploymentRenderer(BaseRenderer):
    diagram_type = "deployment"

    def render(self, model, view):
        profile = self.profile(view)
        nodes, relations = self.selected(model, view)
        document = self.new_document(view.title)
        columns = 3 if profile["orientation"] == "LR" else 2
        geometries = self.layout.grid(nodes, width=280, height=220, columns=columns)
        for node in nodes:
            parent = drawio_id(node.id)
            document.vertex(
                parent,
                node.name,
                self.design.node("primary", "shape=cube;size=20;container=1;fontStyle=1"),
                geometries[node.id],
                metadata={"semanticId": node.id, "semanticType": node.type},
            )
            artifacts = (
                node.metadata.get("artifacts", []) if profile["show_deployed_artifacts"] else []
            )
            for index, artifact in enumerate(artifacts):
                document.vertex(
                    f"{parent}-artifact-{index}",
                    f"<<artifact>>\n{artifact}",
                    self.design.node("secondary", "shape=component"),
                    Geometry(35, 55 + index * 90, 200, 65),
                    parent=parent,
                    metadata={"deployedOn": node.id},
                )
        for relation in relations:
            document.edge(
                f"sem-{relation.id}",
                drawio_id(relation.source),
                drawio_id(relation.target),
                relation.name,
                self.design.edge("communication_path"),
            )
        return document
