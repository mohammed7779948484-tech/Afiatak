from pathlib import Path

from engine.drawio import Document, Geometry
from qa.geometry import validate_geometry


def test_overlap_is_detected(tmp_path: Path) -> None:
    path = tmp_path / "overlap.drawio"
    document = Document("TEST DATA")
    document.vertex("a", "A", "rounded=1", Geometry(100, 100, 100, 50))
    document.vertex("b", "B", "rounded=1", Geometry(150, 120, 100, 50))
    document.write(str(path))
    assert "overlap" in {item.code for item in validate_geometry(str(path))}


def test_connector_through_node_is_detected(tmp_path: Path) -> None:
    path = tmp_path / "route.drawio"
    document = Document("TEST DATA")
    document.vertex("a", "A", "rounded=1", Geometry(100, 100, 100, 50))
    document.vertex("b", "B", "rounded=1", Geometry(300, 100, 100, 50))
    document.vertex("c", "C", "rounded=1", Geometry(500, 100, 100, 50))
    document.edge("edge", "a", "c", "", "endArrow=block", waypoints=((350, 125),))
    document.write(str(path))
    assert "connector-clearance" in {item.code for item in validate_geometry(str(path))}
