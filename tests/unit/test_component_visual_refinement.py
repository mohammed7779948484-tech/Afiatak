from pathlib import Path
from xml.etree import ElementTree as ET

from engine.compositions.component_diagram_layouts import layout_for
from engine.core.io import ROOT, load_model, load_view
from engine.pipeline import model_path_for
from engine.svg.component_diagram import render_component_diagram_svg
from qa.component_svg_validation import validate_component_svg


VIEW_PATH = ROOT / "views" / "component" / "aafiatak-system-component-architecture.yaml"


def _render(tmp_path: Path) -> tuple[Path, object, object]:
    view = load_view(VIEW_PATH)
    model = load_model(model_path_for(VIEW_PATH, view.model))
    output = tmp_path / "cmp01.svg"
    render_component_diagram_svg(model, view, output)
    return output, model, view


def _codes(svg_path: Path, model, view) -> set[str]:
    return {diagnostic.code for diagnostic in validate_component_svg(svg_path, model, view)}


def _node(root: ET.Element, semantic_id: str) -> ET.Element:
    return next(node for node in root.iter() if node.attrib.get("data-semantic-id") == semantic_id)


def _rewrite(svg_path: Path, mutate) -> None:
    tree = ET.parse(svg_path)
    mutate(tree.getroot())
    tree.write(svg_path, encoding="utf-8", xml_declaration=True)


def test_component_renderer_emits_unified_standard_component_symbol(tmp_path: Path) -> None:
    output, _, _ = _render(tmp_path)
    source = output.read_text(encoding="utf-8")
    assert source.count('data-component-symbol="uml-module"') == 9
    assert 'class="component-module-tab"' in source


def test_component_layout_is_materially_more_compact_than_baseline() -> None:
    layout = layout_for("aafiatak-system-component-architecture")
    assert layout.width <= 12800
    assert layout.height <= 7600


def test_component_visual_qa_rejects_interface_label_over_component_name(tmp_path: Path) -> None:
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        backend = _node(root, "component.cmp01.aafiatak-backend")
        _node(root, "component.cmp01.pi.aafiatak-application-interface").attrib["data-label-bounds"] = backend.attrib["data-name-bounds"]

    _rewrite(output, mutate)
    assert "interface-label-own-component-name-overlap" in _codes(output, model, view)


def test_component_visual_qa_rejects_detached_interface_label(tmp_path: Path) -> None:
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        _node(root, "component.cmp01.pi.aafiatak-application-interface").attrib["data-label-bounds"] = "200.00,200.00,900.00,90.00"

    _rewrite(output, mutate)
    assert "interface-label-detached-from-glyph" in _codes(output, model, view)


def test_component_visual_qa_rejects_connector_through_label(tmp_path: Path) -> None:
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        points = _node(root, "relation.cmp01.assembly.patient-application").attrib["data-points"].split()
        x1, y1 = (float(value) for value in points[1].split(","))
        x2, y2 = (float(value) for value in points[2].split(","))
        mid_y = (y1 + y2) / 2
        _node(root, "component.cmp01.pi.aafiatak-application-interface").attrib["data-label-bounds"] = f"{x1 - 70:.2f},{mid_y - 70:.2f},140.00,140.00"

    _rewrite(output, mutate)
    assert "connector-interface-label-intersection" in _codes(output, model, view)


def test_component_visual_qa_rejects_long_shared_connector_segment(tmp_path: Path) -> None:
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        _node(root, "relation.cmp01.assembly.notification").attrib["data-points"] = _node(root, "relation.cmp01.assembly.payment").attrib["data-points"]

    _rewrite(output, mutate)
    assert "connector-shared-segment-ambiguity" in _codes(output, model, view)


def test_component_visual_qa_rejects_component_name_over_module_glyph(tmp_path: Path) -> None:
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        component = _node(root, "component.cmp01.patient-application")
        component.attrib["data-name-bounds"] = component.attrib.get("data-module-glyph-bounds", "0.00,0.00,500.00,180.00")

    _rewrite(output, mutate)
    assert "component-name-glyph-overlap" in _codes(output, model, view)


def test_component_visual_qa_rejects_detached_interface_stem(tmp_path: Path) -> None:
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        _node(root, "component.cmp01.ri.patient-application-interface").attrib["data-stem-boundary-point"] = "0.00,0.00"

    _rewrite(output, mutate)
    assert "interface-stem-detached-owner" in _codes(output, model, view)


def test_component_visual_qa_rejects_interface_label_inside_own_component(tmp_path: Path) -> None:
    output, model, view = _render(tmp_path)

    def mutate(root: ET.Element) -> None:
        _node(root, "component.cmp01.pi.aafiatak-application-interface").attrib["data-label-bounds"] = "6500.00,3900.00,700.00,90.00"

    _rewrite(output, mutate)
    assert "interface-label-own-component-intersection" in _codes(output, model, view)
