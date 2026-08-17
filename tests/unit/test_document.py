from xml.etree import ElementTree as ET

from engine.drawio import Document, Geometry


def test_document_escapes_labels_and_emits_edge_geometry() -> None:
    document = Document("TEST DATA")
    document.vertex("a", "A & B", "rounded=1;html=1;", Geometry(100, 100, 100, 50))
    document.vertex("b", "B", "rounded=1;html=1;", Geometry(300, 100, 100, 50))
    document.edge("e", "a", "b", "x < y", "endArrow=open;")
    xml = document.to_bytes()
    root = ET.fromstring(xml)
    assert b"A &amp; B" in xml
    assert root.find(".//mxCell[@id='e']/mxGeometry") is not None


def test_document_rejects_duplicate_ids() -> None:
    document = Document("TEST DATA")
    document.vertex("a", "A", "rounded=1", Geometry(0, 0, 10, 10))
    try:
        document.vertex("a", "Again", "rounded=1", Geometry(20, 0, 10, 10))
    except ValueError as exc:
        assert "duplicate" in str(exc)
    else:
        raise AssertionError("duplicate ID accepted")
