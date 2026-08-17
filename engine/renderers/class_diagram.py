from engine.core.ids import drawio_id
from engine.drawio import Geometry
from engine.drawio.styles import compile_style
from engine.renderers.base import BaseRenderer


class ClassRenderer(BaseRenderer):
    diagram_type = "class"

    def relation_label(self, relation):
        return relation.name or relation.type.replace("_", " ")

    def render(self, model, view):
        profile = self.profile(view)
        elements, relations = self.selected(model, view)
        document = self.new_document(view.title)
        columns = 3 if profile["orientation"] == "LR" else 2
        geometries = self.layout.grid(elements, width=260, height=190, columns=columns)
        compartment_style = compile_style(
            "text;html=1;align=left;verticalAlign=top;spacingLeft=8;whiteSpace=wrap",
            fillColor="none",
            strokeColor=self.design.palette["border"],
            fontFamily=self.design.typography["font_family"],
            fontSize=self.design.typography["node"]["size"],
        )
        for element in elements:
            parent = drawio_id(element.id)
            document.vertex(
                parent,
                element.name,
                self.design.node("primary", "swimlane;startSize=30;container=1;fontStyle=1"),
                geometries[element.id],
                metadata={"semanticId": element.id, "semanticType": element.type},
            )
            sections = (
                ("attributes", 30, 55),
                ("operations", 85, 55),
                ("responsibilities", 140, 50),
            )
            for name, y, height in sections if profile["show_compartments"] else ():
                values = element.metadata.get(name, [])
                document.vertex(
                    f"{parent}-{name}",
                    "\n".join(values),
                    compartment_style,
                    Geometry(0, y, 260, height),
                    parent=parent,
                    metadata={"compartment": name},
                )
        for relation in relations:
            edge_id = f"sem-{relation.id}"
            document.edge(
                edge_id,
                drawio_id(relation.source),
                drawio_id(relation.target),
                self.relation_label(relation),
                self.design.edge(relation.type),
            )
            source = relation.metadata.get("sourceMultiplicity")
            target = relation.metadata.get("targetMultiplicity")
            if source:
                document.edge_label(f"{edge_id}-source-multiplicity", edge_id, str(source), -0.8)
            if target:
                document.edge_label(f"{edge_id}-target-multiplicity", edge_id, str(target), 0.8)
        return document
