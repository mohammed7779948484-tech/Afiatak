from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from engine.core.models import SemanticModel, ViewSpec

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return value


def validate_schema(data: dict[str, Any], schema_name: str) -> list[str]:
    schema_path = ROOT / "engine" / "schemas" / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = Draft202012Validator(schema).iter_errors(data)
    return [f"{'/'.join(str(p) for p in error.path) or '$'}: {error.message}" for error in errors]


def load_model(path: Path) -> SemanticModel:
    data = load_yaml(path)
    errors = validate_schema(data, "semantic-model.schema.json")
    if errors:
        raise ValueError("\n".join(errors))
    return SemanticModel.from_dict(data)


def load_view(path: Path) -> ViewSpec:
    data = load_yaml(path)
    errors = validate_schema(data, "view.schema.json")
    if errors:
        raise ValueError("\n".join(errors))
    return ViewSpec.from_dict(data)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    records = {
        str(item.relative_to(path)).replace("\\", "/"): sha256_file(item)
        for item in sorted(
            candidate
            for candidate in path.rglob("*")
            if candidate.is_file()
            and "__pycache__" not in candidate.parts
            and candidate.suffix not in {".pyc", ".pyo"}
        )
    }
    return canonical_hash(records)


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()
