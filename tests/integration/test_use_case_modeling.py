from pathlib import Path

from engine.use_case_modeling import render_markdown

FIXTURE = Path(__file__).parents[1] / "fixtures" / "synthetic-library" / "use-case-model.yaml"


def test_structured_use_case_model_renders_markdown(tmp_path: Path) -> None:
    output = render_markdown(FIXTURE, tmp_path / "use-case.md")
    text = output.read_text(encoding="utf-8")
    assert "## Main Flow" in text
    assert "### Item unavailable" in text
    assert "{'" not in text
