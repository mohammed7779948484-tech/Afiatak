from pathlib import Path
from xml.etree import ElementTree as ET

from engine.pipeline import render

FIXTURES = Path(__file__).parents[1] / "fixtures" / "synthetic-library"


def test_use_case_has_boundary_actors_and_native_edges(tmp_path: Path) -> None:
    output = render(FIXTURES / "use-case.yaml", tmp_path / "use-case.drawio")
    root = ET.parse(output).getroot()
    wrappers = {item.get("id"): item for item in root.findall(".//object")}
    boundary = wrappers["system-boundary"].find("mxCell")
    assert "container=1" in boundary.get("style", "")
    actor = wrappers["sem-actor.member"].find("mxCell")
    use_case = wrappers["sem-uc.borrow_item"].find("mxCell")
    assert actor.get("parent") == "layer-nodes"
    assert use_case.get("parent") == "system-boundary"
    assert root.findall(".//mxCell[@edge='1']")
