from engine.renderers.base import BaseRenderer


class PackageRenderer(BaseRenderer):
    diagram_type = "package"
    default_shape = "shape=folder;tabWidth=50;tabHeight=20"
