from pathlib import Path
from engine.core.models import SemanticModel, ViewSpec
from engine.compositions import aafiatak_booking_reception_staff_part_3 as composition
from engine.svg.booking_reception_staff_use_case import render_booking_reception_staff_svg

def render_booking_reception_staff_part_3_svg(model: SemanticModel, view: ViewSpec, output: Path) -> Path:
    if view.id != "aafiatak-booking-reception-staff-part-3":
        raise ValueError(f"no curated SVG composition for {view.id}")
    return render_booking_reception_staff_svg(model, view, output, composition, "Detailed UML Booking & Reception Staff Package Use Case Diagram.")
