from pathlib import Path

from engine.core.io import canonical_hash, sha256_file


def test_hashes_are_deterministic(tmp_path: Path) -> None:
    path = tmp_path / "data.txt"
    path.write_text("stable", encoding="utf-8")
    assert sha256_file(path) == sha256_file(path)
    assert canonical_hash({"b": 2, "a": 1}) == canonical_hash({"a": 1, "b": 2})
