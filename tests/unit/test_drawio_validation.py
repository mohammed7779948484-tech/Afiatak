from pathlib import Path

from qa.drawio_validation import validate_drawio

FIXTURES = Path(__file__).parents[1] / "fixtures"


def test_invalid_parent_is_rejected() -> None:
    diagnostics = validate_drawio(
        FIXTURES / "invalid" / "broken-parent.drawio", run_skill_validator=False
    )
    assert "invalid-parent" in {item.code for item in diagnostics}
