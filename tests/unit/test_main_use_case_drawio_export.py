from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.aafiatak_main_use_case_drawio import ACTORS, BOUNDARY, ROUTES, USE_CASES
from engine.core.io import ROOT, load_model, load_view
from engine.main_use_case_drawio_export import export_main_use_case_drawio
from engine.pipeline import model_path_for


VIEW_PATH = ROOT / "views" / "use-case" / "aafiatak-main-use-case.yaml"
HUMAN_ACTORS = {
    "actor.visitor",
    "actor.patient",
    "actor.facility-administrator",
    "actor.booking-reception-staff",
    "actor.doctor",
    "actor.platform-administrator",
}
EXTERNAL_SYSTEMS = set(ACTORS) - HUMAN_ACTORS


def _export(tmp_path: Path) -> tuple[Path, object, object]:
    view = load_view(VIEW_PATH)
    model = load_model(model_path_for(VIEW_PATH, view.model))
    output = tmp_path / "main-use-case.drawio"
    export_main_use_case_drawio(model, view, output)
    return output, model, view


def _cells(path: Path) -> dict[str, ET.Element]:
    cells = list(ET.parse(path).getroot().iter("mxCell"))
    return {cell.attrib["id"]: cell for cell in cells}


def _node_id(semantic_id: str) -> str:
    return "node-" + semantic_id.replace(".", "-")


def _edge_id(relation_id: str) -> str:
    return "edge-" + relation_id.replace(".", "-")


def _inside(inner, outer) -> bool:
    return inner.x >= outer.x and inner.y >= outer.y and inner.right <= outer.right and inner.bottom <= outer.bottom


def _overlaps(a, b) -> bool:
    return not (a.right <= b.x or b.right <= a.x or a.bottom <= b.y or b.bottom <= a.y)


def _port_point(box, x_ratio: float, y_ratio: float) -> tuple[float, float]:
    return box.x + box.width * x_ratio, box.y + box.height * y_ratio


def _segment_intersects_box(a: tuple[float, float], b: tuple[float, float], box) -> bool:
    xmin, ymin, xmax, ymax = box.x + 1, box.y + 1, box.right - 1, box.bottom - 1
    x1, y1 = a
    x2, y2 = b
    dx, dy = x2 - x1, y2 - y1
    p = (-dx, dx, -dy, dy)
    q = (x1 - xmin, xmax - x1, y1 - ymin, ymax - y1)
    lower, upper = 0.0, 1.0
    for pi, qi in zip(p, q):
        if abs(pi) < 1e-9:
            if qi < 0:
                return False
            continue
        ratio = qi / pi
        if pi < 0:
            if ratio > upper:
                return False
            lower = max(lower, ratio)
        else:
            if ratio < lower:
                return False
            upper = min(upper, ratio)
    return lower <= upper


def test_native_drawio_export_is_well_formed_and_complete(tmp_path: Path) -> None:
    output, _, view = _export(tmp_path)
    root = ET.parse(output).getroot()
    assert root.tag == "mxfile"
    graph = root.find("./diagram/mxGraphModel")
    assert graph is not None
    cells = list(graph.findall("./root/mxCell"))
    ids = [cell.attrib["id"] for cell in cells]
    assert len(ids) == len(set(ids))
    by_id = {cell.attrib["id"]: cell for cell in cells}
    assert by_id["0"].get("parent") is None
    assert by_id["1"].get("parent") == "0"
    assert {"layer-relationships", "layer-elements", "layer-labels"} <= set(by_id)
    assert {_node_id(item_id) for item_id in view.include} <= set(by_id)
    expected_edges = {_edge_id(relation_id) for relation_id in view.relations}
    assert expected_edges == {cell_id for cell_id, cell in by_id.items() if cell.get("edge") == "1"}
    for edge_id in expected_edges:
        edge = by_id[edge_id]
        assert edge.get("vertex") is None
        assert edge.get("source") in by_id
        assert edge.get("target") in by_id
        geometry = edge.find("mxGeometry")
        assert geometry is not None and geometry.get("relative") == "1"


def test_export_preserves_the_approved_main_view_without_leaking_hidden_use_cases(tmp_path: Path) -> None:
    output, _, view = _export(tmp_path)
    by_id = _cells(output)
    assert {_node_id(item_id) for item_id in view.include} == {cell_id for cell_id in by_id if cell_id.startswith("node-")}
    for hidden in ("uc.muc-07", "uc.muc-08", "uc.muc-10", "uc.muc-17", "uc.muc-18", "uc.muc-23", "uc.muc-24", "uc.muc-30"):
        assert _node_id(hidden) not in by_id


def test_associations_and_dependencies_use_correct_uml_notation_and_direction(tmp_path: Path) -> None:
    output, model, view = _export(tmp_path)
    by_id = _cells(output)
    relations = {relation.id: relation for relation in model.relations if relation.id in set(view.relations)}
    for relation_id, relation in relations.items():
        edge = by_id[_edge_id(relation_id)]
        style = edge.attrib["style"]
        assert edge.get("source") == _node_id(relation.source)
        assert edge.get("target") == _node_id(relation.target)
        if relation.type == "association":
            assert "dashed=1" not in style
            assert "endArrow=none" in style and "startArrow=none" in style
        else:
            assert relation.type in {"include", "extend"}
            assert "dashed=1" in style and "endArrow=open" in style and "endFill=0" in style
            assert "startArrow=none" in style
    assert by_id[_edge_id("relation.inc-01")].get("source") == _node_id("uc.muc-03")
    assert by_id[_edge_id("relation.inc-01")].get("target") == _node_id("uc.muc-05")
    assert by_id[_edge_id("relation.inc-02")].get("source") == _node_id("uc.muc-04")
    assert by_id[_edge_id("relation.inc-02")].get("target") == _node_id("uc.muc-05")
    assert by_id[_edge_id("relation.ext-01")].get("source") == _node_id("uc.muc-09")
    assert by_id[_edge_id("relation.ext-01")].get("target") == _node_id("uc.muc-06")
    assert by_id["label-relation-inc-01"].attrib["value"] == "«include»"
    assert by_id["label-relation-inc-02"].attrib["value"] == "«include»"
    assert by_id["label-relation-ext-01"].attrib["value"] == "«extend»"
    assert by_id["label-relation-ext-01-condition"].attrib["value"] == "[Booking policy = FULL_PAYMENT_REQUIRED]"


def test_geometry_keeps_use_cases_inside_and_all_actors_outside_the_system_boundary() -> None:
    assert all(_inside(box, BOUNDARY) for box in USE_CASES.values())
    assert all(not _inside(box, BOUNDARY) for box in ACTORS.values())
    for box in [BOUNDARY, *ACTORS.values(), *USE_CASES.values()]:
        assert all(value % 10 == 0 for value in (box.x, box.y, box.width, box.height))
    entries = list(USE_CASES.items())
    for index, (left_id, left) in enumerate(entries):
        for right_id, right in entries[index + 1 :]:
            assert not _overlaps(left, right), f"overlap: {left_id} / {right_id}"


def test_actor_notation_distinguishes_people_from_external_systems(tmp_path: Path) -> None:
    output, _, _ = _export(tmp_path)
    by_id = _cells(output)
    for semantic_id in HUMAN_ACTORS:
        cell = by_id[_node_id(semantic_id)]
        assert "shape=umlActor" in cell.attrib["style"]
        assert "external system" not in cell.attrib["value"]
    for semantic_id in EXTERNAL_SYSTEMS:
        cell = by_id[_node_id(semantic_id)]
        assert "shape=umlActor" not in cell.attrib["style"]
        assert "«external system»" in cell.attrib["value"]


def test_authored_route_corridors_do_not_traverse_unrelated_nodes() -> None:
    nodes = {**ACTORS, **USE_CASES}
    endpoints = {
        "relation.visitor-muc-01": ("actor.visitor", "uc.muc-01"),
        "relation.visitor-muc-02": ("actor.visitor", "uc.muc-02"),
        "relation.visitor-muc-03": ("actor.visitor", "uc.muc-03"),
        "relation.visitor-muc-04": ("actor.visitor", "uc.muc-04"),
        "relation.patient-muc-04": ("actor.patient", "uc.muc-04"),
        "relation.patient-muc-06": ("actor.patient", "uc.muc-06"),
        "relation.patient-muc-09": ("actor.patient", "uc.muc-09"),
        "relation.patient-muc-11": ("actor.patient", "uc.muc-11"),
        "relation.patient-muc-12": ("actor.patient", "uc.muc-12"),
        "relation.patient-muc-13": ("actor.patient", "uc.muc-13"),
        "relation.facility-admin-muc-15": ("actor.facility-administrator", "uc.muc-15"),
        "relation.facility-admin-muc-16": ("actor.facility-administrator", "uc.muc-16"),
        "relation.facility-admin-muc-19": ("actor.facility-administrator", "uc.muc-19"),
        "relation.facility-admin-muc-21": ("actor.facility-administrator", "uc.muc-21"),
        "relation.reception-muc-19": ("actor.booking-reception-staff", "uc.muc-19"),
        "relation.reception-muc-20": ("actor.booking-reception-staff", "uc.muc-20"),
        "relation.reception-muc-21": ("actor.booking-reception-staff", "uc.muc-21"),
        "relation.reception-muc-22": ("actor.booking-reception-staff", "uc.muc-22"),
        "relation.reception-muc-26": ("actor.booking-reception-staff", "uc.muc-26"),
        "relation.doctor-muc-25": ("actor.doctor", "uc.muc-25"),
        "relation.doctor-muc-26": ("actor.doctor", "uc.muc-26"),
        "relation.platform-admin-muc-27": ("actor.platform-administrator", "uc.muc-27"),
        "relation.platform-admin-muc-28": ("actor.platform-administrator", "uc.muc-28"),
        "relation.platform-admin-muc-29": ("actor.platform-administrator", "uc.muc-29"),
        "relation.payment-gateway-muc-09": ("actor.payment-gateway", "uc.muc-09"),
        "relation.notification-service-muc-14": ("actor.notification-service", "uc.muc-14"),
        "relation.map-service-muc-02": ("actor.map-service", "uc.muc-02"),
        "relation.whatsapp-provider-muc-05": ("actor.whatsapp-auth-provider", "uc.muc-05"),
        "relation.inc-01": ("uc.muc-03", "uc.muc-05"),
        "relation.inc-02": ("uc.muc-04", "uc.muc-05"),
        "relation.ext-01": ("uc.muc-09", "uc.muc-06"),
    }
    assert set(endpoints) == set(ROUTES)
    for relation_id, (source_id, target_id) in endpoints.items():
        route = ROUTES[relation_id]
        points = [
            _port_point(nodes[source_id], route.exit_x, route.exit_y),
            *route.waypoints,
            _port_point(nodes[target_id], route.entry_x, route.entry_y),
        ]
        for x, y in route.waypoints:
            assert x % 10 == 0 and y % 10 == 0
        for start, end in zip(points, points[1:]):
            for node_id, box in nodes.items():
                if node_id in {source_id, target_id}:
                    continue
                assert not _segment_intersects_box(start, end, box), (relation_id, node_id, start, end)
        last, target = points[-2], points[-1]
        assert abs(last[0] - target[0]) + abs(last[1] - target[1]) >= 20


def test_export_is_deterministic_and_xml_escapes_special_characters(tmp_path: Path) -> None:
    first, model, view = _export(tmp_path)
    first_bytes = first.read_bytes()
    second = tmp_path / "main-use-case-second.drawio"
    export_main_use_case_drawio(model, view, second)
    assert first_bytes == second.read_bytes()
    text = first_bytes.decode("utf-8")
    assert text.startswith("<?xml version='1.0' encoding='utf-8'?>")
    assert "Booking &amp; Reception Staff" in text
    assert "<!--" not in text
