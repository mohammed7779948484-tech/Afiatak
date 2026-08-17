from pathlib import Path

from engine.compositions import aafiatak_facility_administrator_part_2 as composition
from engine.core.models import SemanticModel, ViewSpec
from engine.svg.facility_administrator_use_case import render_facility_administrator_svg

def render_facility_administrator_part_2_svg(model: SemanticModel, view: ViewSpec, output: Path) -> Path:
    if view.id != "aafiatak-facility-administrator-part-2":
        raise ValueError(f"no curated SVG composition for {view.id}")
    return render_facility_administrator_svg(model, view, output, composition, "Detailed UML Facility Administrator Package Use Case Diagram.")
