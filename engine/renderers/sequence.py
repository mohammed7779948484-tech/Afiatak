from engine.core.ids import drawio_id
from engine.drawio import Geometry
from engine.drawio.styles import compile_style
from engine.renderers.base import BaseRenderer


class SequenceRenderer(BaseRenderer):
    diagram_type = "sequence"

    def render(self, model, view):
        participants, messages = self.selected(model, view)
        messages.sort(key=lambda item: item.metadata["sequence"])
        document = self.new_document(view.title)
        profile = self.profile(view)
        if profile["orientation"] != "LR" or profile["time_direction"] != "TB":
            raise ValueError("sequence profile requires LR participants and TB time")
        participant_gap = int(profile["participant_gap"])
        x_by_id = {
            item.id: 180 + index * (180 + participant_gap)
            for index, item in enumerate(participants)
        }
        lifeline_style = self.design.node(
            "primary",
            "shape=umlLifeline;perimeter=lifelinePerimeter;container=1;"
            "collapsible=0;recursiveResize=0",
        )
        height = max(500, 160 + 90 * len(messages))
        for item in participants:
            document.vertex(
                drawio_id(item.id),
                item.name,
                lifeline_style,
                Geometry(x_by_id[item.id], 90, 180, height),
                metadata={"semanticId": item.id, "semanticType": item.type},
            )
        active: dict[str, str] = {}
        target_activation: dict[str, str] = {}
        for index, message in enumerate(messages):
            if message.type == "return_message":
                continue
            y = 200 + index * 90
            activation_id = f"sem-{message.id}-activation"
            target_activation[message.id] = activation_id
            active[message.target] = activation_id
            document.vertex(
                activation_id,
                "",
                self.design.node("secondary", "shape=umlFrame;strokeWidth=1"),
                Geometry(85, y - 90, 10, 60),
                parent=drawio_id(message.target),
                metadata={"activationFor": message.id},
            )
        for index, message in enumerate(messages):
            y = 200 + index * 90
            style = self.design.edge(message.type)
            if message.type == "return_message":
                style = compile_style(
                    style,
                    "dashed=1;endArrow=open;endFill=0;strokeColor=#64748B",
                )
            document.edge(
                f"sem-{message.id}",
                active.get(message.source, drawio_id(message.source)),
                (
                    active.get(message.target, drawio_id(message.target))
                    if message.type == "return_message"
                    else target_activation[message.id]
                ),
                f"{message.metadata['sequence']}. {message.name}",
                style,
                waypoints=(
                    (x_by_id[message.source] + 90, y),
                    (x_by_id[message.target] + 90, y),
                ),
            )
        return document
