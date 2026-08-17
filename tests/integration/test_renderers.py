from pathlib import Path

import pytest

from engine.pipeline import render
from qa.drawio_validation import validate_drawio

FIXTURES = Path(__file__).parents[1] / "fixtures" / "synthetic-library"
VIEWS = [
    "use-case",
    "package",
    "class",
    "object",
    "activity",
    "sequence",
    "communication",
    "state",
    "component",
    "deployment",
]


@pytest.mark.parametrize("name", VIEWS)
def test_each_diagram_family_renders(name: str, tmp_path: Path) -> None:
    output = tmp_path / f"{name}.drawio"
    render(FIXTURES / f"{name}.yaml", output)
    assert output.is_file()
    assert not [item for item in validate_drawio(output) if item.severity == "error"]


def test_rendering_is_deterministic(tmp_path: Path) -> None:
    first = render(FIXTURES / "use-case.yaml", tmp_path / "first.drawio").read_bytes()
    second = render(FIXTURES / "use-case.yaml", tmp_path / "second.drawio").read_bytes()
    assert first == second
