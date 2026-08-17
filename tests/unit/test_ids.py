import pytest

from engine.core.ids import drawio_id, validate_id


def test_stable_ids_are_namespaced() -> None:
    assert validate_id("actor.library_member")
    assert drawio_id("actor.library_member") == "sem-actor.library_member"
    assert not validate_id("Library Member")


def test_invalid_id_is_rejected() -> None:
    with pytest.raises(ValueError):
        drawio_id("0")
