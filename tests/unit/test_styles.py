from engine.drawio.styles import compile_style, parse_style


def test_style_compilation_overrides_without_duplicates() -> None:
    style = compile_style("rounded=1;fillColor=#000000", "fillColor=#FFFFFF;html=1")
    parsed = parse_style(style)
    assert parsed["fillColor"] == "#FFFFFF"
    assert style.count("fillColor=") == 1
