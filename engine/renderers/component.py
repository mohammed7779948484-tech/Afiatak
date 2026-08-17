from engine.renderers.base import BaseRenderer


class ComponentRenderer(BaseRenderer):
    diagram_type = "component"
    default_shape = "shape=component"

    def shape_for(self, element):
        return {
            "provided_interface": "shape=lollipop;direction=south",
            "required_interface": "shape=requires;direction=north",
        }.get(element.type, self.default_shape)

    def render(self, model, view):
        profile = self.profile(view)
        selected, _ = self.selected(model, view)
        has_interfaces = any(
            item.type in {"provided_interface", "required_interface"} for item in selected
        )
        if has_interfaces and not profile["show_interfaces"]:
            raise ValueError("component profile disables interfaces selected by the view")
        return super().render(model, view)
