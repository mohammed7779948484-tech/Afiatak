from pathlib import Path
from xml.etree import ElementTree as ET

from engine.pipeline import render

FIXTURES = Path(__file__).parents[1] / "fixtures" / "synthetic-library"


def _root(name: str, tmp_path: Path):
    output = render(FIXTURES / f"{name}.yaml", tmp_path / f"{name}.drawio")
    return ET.parse(output).getroot()


def test_sequence_uses_lifelines_ordered_messages_and_returns(tmp_path: Path) -> None:
    root = _root("sequence", tmp_path)
    styles = [
        item.find("mxCell").get("style", "")
        for item in root.findall(".//object")
        if item.get("semanticType") in {"participant", "component"}
    ]
    assert all("umlLifeline" in style for style in styles)
    edges = root.findall(".//mxCell[@edge='1']")
    assert [edge.get("value", "").split(".", 1)[0] for edge in edges] == ["1", "2", "3"]
    assert "dashed=1" in edges[-1].get("style", "")
    assert all(edge.find("mxGeometry/Array") is not None for edge in edges)
    activations = [
        item for item in root.findall(".//object") if item.get("activationFor") is not None
    ]
    assert len(activations) == 2


def test_state_and_activity_flows_are_directed(tmp_path: Path) -> None:
    for name in ("state", "activity"):
        root = _root(name, tmp_path)
        assert all(
            "endArrow=block" in edge.get("style", "")
            for edge in root.findall(".//mxCell[@edge='1']")
        )


def test_class_renders_responsibility_and_multiplicity(tmp_path: Path) -> None:
    root = _root("class", tmp_path)
    labels = [item.get("label", "") for item in root.findall(".//object")]
    assert any("Track catalog identity" in label for label in labels)
    edge_labels = [
        item.get("value", "")
        for item in root.findall(".//mxCell[@style]")
        if "edgeLabel" in item.get("style", "")
    ]
    assert "0..*" in edge_labels
    assert "1" in edge_labels
