from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

import engine.pipeline as pipeline

FIXTURES = Path(__file__).parents[1] / "fixtures" / "synthetic-library"


def test_requested_image_fails_when_drawio_is_unavailable(tmp_path: Path, monkeypatch) -> None:
    view = {
        "id": "synthetic-export-gate",
        "title": "TEST DATA",
        "diagramType": "use_case",
        "model": str((FIXTURES / "model.yaml").resolve()),
        "include": ["actor.member", "uc.borrow_item"],
        "relations": ["relation.member.borrow"],
        "approval": "approved",
        "outputTargets": ["drawio", "png"],
    }
    path = tmp_path / "view.yaml"
    path.write_text(yaml.safe_dump(view), encoding="utf-8")
    monkeypatch.setattr(pipeline, "find_drawio", lambda: None)
    monkeypatch.setattr(
        pipeline,
        "validate_inputs",
        lambda model_path, view_path: (SimpleNamespace(test_data=False), None, []),
    )
    with pytest.raises(RuntimeError, match="requires the draw.io"):
        pipeline.build(path)


def test_synthetic_model_cannot_be_released(tmp_path: Path, monkeypatch) -> None:
    view = {
        "id": "synthetic-release-gate",
        "title": "TEST DATA",
        "diagramType": "use_case",
        "model": str((FIXTURES / "model.yaml").resolve()),
        "include": ["actor.member", "uc.borrow_item"],
        "relations": ["relation.member.borrow"],
        "approval": "approved",
        "outputTargets": ["drawio"],
    }
    path = tmp_path / "view.yaml"
    path.write_text(yaml.safe_dump(view), encoding="utf-8")
    monkeypatch.setattr(pipeline, "find_drawio", lambda: None)
    with pytest.raises(ValueError, match="testData"):
        pipeline.build(path)
