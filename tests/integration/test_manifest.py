from pathlib import Path

from engine.manifests import create_manifest, stale_reasons


def test_manifest_captures_output_hash_and_is_current(tmp_path: Path) -> None:
    output = tmp_path / "synthetic.drawio"
    output.write_text("TEST DATA", encoding="utf-8")
    manifest = create_manifest(
        diagram_id="synthetic",
        diagram_type="use_case",
        model_data={"testData": True},
        outputs=[output],
        qa={"result": "pass"},
    )
    assert manifest["outputs"]
    assert stale_reasons(manifest) == []
    output.write_text("changed", encoding="utf-8")
    assert any("output changed" in item for item in stale_reasons(manifest))
