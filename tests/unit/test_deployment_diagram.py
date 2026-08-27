from importlib import import_module
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.io import ROOT, load_model, load_view
from engine.deployment_drawio_export import export_deployment_drawio
from engine.pipeline import model_path_for, render


VIEW_PATH = ROOT / "views" / "deployment" / "aafiatak-mvp-deployment.yaml"
EXPECTED_NODES = {
    "node.dep01.patient-mobile-device",
    "node.dep01.facility-client-device",
    "node.dep01.platform-admin-client-device",
    "node.dep01.aafiatak-centralized-server",
    "node.dep01.postgresql-environment",
    "node.dep01.whatsapp-auth-provider",
    "node.dep01.payment-gateway",
    "node.dep01.notification-service",
    "node.dep01.map-service",
}
EXPECTED_PATHS = {
    "relation.dep01.communication.patient-mobile-to-server",
    "relation.dep01.communication.facility-client-to-server",
    "relation.dep01.communication.platform-admin-client-to-server",
    "relation.dep01.communication.server-to-postgresql",
    "relation.dep01.communication.server-to-whatsapp-auth",
    "relation.dep01.communication.server-to-payment-gateway",
    "relation.dep01.communication.server-to-notification-service",
}


def _render(tmp_path: Path) -> tuple[Path, object, object]:
    output = tmp_path / "dep01.svg"
    render(VIEW_PATH, output)
    view = load_view(VIEW_PATH)
    model = load_model(model_path_for(VIEW_PATH, view.model))
    return output, model, view


def _node(root: ET.Element, semantic_id: str) -> ET.Element:
    return next(node for node in root.iter() if node.attrib.get("data-semantic-id") == semantic_id)


def _rewrite(svg_path: Path, mutate) -> None:
    tree = ET.parse(svg_path)
    mutate(tree.getroot())
    tree.write(svg_path, encoding="utf-8", xml_declaration=True)


def test_dep01_pipeline_renders_the_exact_logical_topology(tmp_path: Path) -> None:
    """Catches a missing render dispatch or a changed DEP-01 node/path inventory."""
    output, _, _ = _render(tmp_path)
    root = ET.parse(output).getroot()
    assert root.attrib["data-kind"] == "deployment-diagram"
    nodes = {node.attrib["data-semantic-id"] for node in root.iter() if node.attrib.get("data-kind") == "deployment-node"}
    paths = {node.attrib["data-semantic-id"] for node in root.iter() if node.attrib.get("data-kind") == "communication-path"}
    assert nodes == EXPECTED_NODES
    assert paths == EXPECTED_PATHS
    assert "marker-end" not in output.read_text(encoding="utf-8")


def test_dep01_renderer_keeps_map_service_intentionally_disconnected(tmp_path: Path) -> None:
    """Catches an invented Map Service connection in the generated deployment topology."""
    output, _, _ = _render(tmp_path)
    root = ET.parse(output).getroot()
    map_id = "node.dep01.map-service"
    assert _node(root, map_id).attrib["data-kind"] == "deployment-node"
    endpoints = {
        endpoint
        for relation in root.iter()
        if relation.attrib.get("data-kind") == "communication-path"
        for endpoint in (relation.attrib.get("data-source-id"), relation.attrib.get("data-target-id"))
    }
    assert map_id not in endpoints


def test_dep01_qa_rejects_an_arrowhead_on_a_communication_path(tmp_path: Path) -> None:
    """Catches an accidental directed arrow on an undirected UML communication path."""
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        path = _node(root, "relation.dep01.communication.patient-mobile-to-server")
        path.attrib["marker-end"] = "url(#forbidden-arrow)"

    _rewrite(output, mutate)
    validate = import_module("qa.deployment_svg_validation").validate_deployment_svg
    codes = {diagnostic.code for diagnostic in validate(output, model, view)}
    assert "communication-path-arrowhead" in codes


def test_dep01_qa_rejects_a_path_through_an_unrelated_node(tmp_path: Path) -> None:
    """Catches a connector route that crosses a visible deployment node unrelated to it."""
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        path = _node(root, "relation.dep01.communication.patient-mobile-to-server")
        unrelated = _node(root, "node.dep01.facility-client-device")
        bounds = unrelated.attrib["data-bounds"].split(",")
        x = float(bounds[0]) + float(bounds[2]) / 2
        y = float(bounds[1]) + float(bounds[3]) / 2
        points = path.attrib["data-points"].split()
        path.attrib["data-points"] = f"{points[0]} {x:.2f},{y:.2f} {points[-1]}"

    _rewrite(output, mutate)
    validate = import_module("qa.deployment_svg_validation").validate_deployment_svg
    codes = {diagnostic.code for diagnostic in validate(output, model, view)}
    assert "communication-path-through-unrelated-node" in codes


def test_dep01_renderer_distinguishes_runtime_environment_from_deployed_artifacts(tmp_path: Path) -> None:
    """Catches Android/iOS or browser content rendered as the same module-like software item as an artifact."""
    output, _, _ = _render(tmp_path)
    root = ET.parse(output).getroot()
    rendered = [node for node in root.iter() if node.attrib.get("data-kind") in {"execution-environment", "deployed-artifact", "device-context"}]
    by_name = {node.attrib["data-item-name"]: node for node in rendered}

    assert {name for name, node in by_name.items() if node.attrib["data-uml-kind"] == "executionEnvironment"} == {"Android / iOS", "Web Browser"}
    assert by_name["Desktop / Tablet"].attrib["data-uml-kind"] == "device-context"
    assert {name for name, node in by_name.items() if node.attrib["data-uml-kind"] == "artifact"} == {
        "Patient Application",
        "Facility Web Dashboard",
        "Aafiatak Platform Administration Dashboard",
        "Aafiatak Backend",
        "PostgreSQL Database",
    }
    assert not [node for node in root.iter() if node.attrib.get("data-kind") == "deployed-item"]


def test_dep01_renderer_marks_logical_execution_environment_nodes_without_renaming(tmp_path: Path) -> None:
    """Catches a logical server/database grouping that is rendered as an unexplained physical-machine assertion."""
    output, _, _ = _render(tmp_path)
    root = ET.parse(output).getroot()
    assert _node(root, "node.dep01.aafiatak-centralized-server").attrib["data-node-stereotype"] == "executionEnvironment"
    assert _node(root, "node.dep01.postgresql-environment").attrib["data-node-stereotype"] == "executionEnvironment"
    assert _node(root, "node.dep01.patient-mobile-device").attrib["data-node-stereotype"] == "device"
    assert _node(root, "node.dep01.aafiatak-centralized-server").attrib["data-node-name"] == "Aafiatak Centralized Server"


def test_dep01_qa_rejects_a_runtime_rendered_as_an_artifact(tmp_path: Path) -> None:
    """Catches execution environments accidentally regressing to deployed-artifact notation."""
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        runtime = next(node for node in root.iter() if node.attrib.get("data-item-name") == "Android / iOS")
        runtime.attrib["data-kind"] = "deployed-artifact"
        runtime.attrib["data-uml-kind"] = "artifact"

    _rewrite(output, mutate)
    validate = import_module("qa.deployment_svg_validation").validate_deployment_svg
    codes = {diagnostic.code for diagnostic in validate(output, model, view)}
    assert "contained-item-notation" in codes


def test_dep01_drawio_export_uses_the_same_runtime_and_artifact_notation(tmp_path: Path) -> None:
    """Catches SVG/draw.io parity drift where execution environments fall back to generic module cells."""
    _, model, view = _render(tmp_path)
    drawio_path = tmp_path / "dep01.drawio"
    export_deployment_drawio(model, view, drawio_path)
    cells = ET.parse(drawio_path).getroot().iter("mxCell")
    by_id = {cell.attrib["id"]: cell for cell in cells if "id" in cell.attrib}
    runtime_cells = [cell for cell_id, cell in by_id.items() if cell_id.startswith("runtime-")]
    artifact_cells = [cell for cell_id, cell in by_id.items() if cell_id.startswith("artifact-")]
    context_cells = [cell for cell_id, cell in by_id.items() if cell_id.startswith("device-context-")]

    assert {cell.attrib["value"].split("<br>")[-1] for cell in runtime_cells} == {"Android / iOS", "Web Browser"}
    assert all("«executionEnvironment»" in cell.attrib["value"] for cell in runtime_cells)
    assert all("shape=module" not in cell.attrib["style"] and "shape=cube" in cell.attrib["style"] for cell in runtime_cells)
    assert {"Patient Application", "Facility Web Dashboard", "Aafiatak Platform Administration Dashboard", "Aafiatak Backend", "PostgreSQL Database"} == {
        cell.attrib["value"].split("<br>")[-1] for cell in artifact_cells
    }
    assert all("shape=note" in cell.attrib["style"] and "«artifact»" in cell.attrib["value"] for cell in artifact_cells)
    assert len(context_cells) == 1 and "Desktop / Tablet" in context_cells[0].attrib["value"]


def test_dep01_composition_is_compact_and_keeps_the_server_central() -> None:
    """Catches an oversized or directionally incorrect deterministic deployment composition."""
    layout = import_module("engine.compositions.deployment_diagram_layouts").layout_for("aafiatak-mvp-deployment")
    assert layout.width <= 13000
    assert layout.height <= 7600
    server = layout.nodes["node.dep01.aafiatak-centralized-server"]
    patient = layout.nodes["node.dep01.patient-mobile-device"]
    whatsapp = layout.nodes["node.dep01.whatsapp-auth-provider"]
    assert patient.box.x < server.box.x < whatsapp.box.x


def test_dep01_layout_uses_compact_separate_communication_corridors() -> None:
    """Catches the line-dominated wide layout and a client/server corridor that is longer than necessary."""
    layout = import_module("engine.compositions.deployment_diagram_layouts").layout_for("aafiatak-mvp-deployment")
    server = layout.nodes["node.dep01.aafiatak-centralized-server"].box
    client_right_edges = [
        layout.nodes["node.dep01.patient-mobile-device"].box.right,
        layout.nodes["node.dep01.facility-client-device"].box.right,
        layout.nodes["node.dep01.platform-admin-client-device"].box.right,
    ]
    segment_lengths = [
        abs(second[0] - first[0]) + abs(second[1] - first[1])
        for path in layout.communication_paths.values()
        for first, second in zip(path, path[1:])
    ]

    assert layout.width <= 11000
    assert layout.height <= 6400
    assert layout.title_y <= 200
    assert server.x - max(client_right_edges) <= 1200
    assert max(segment_lengths) <= 1550
