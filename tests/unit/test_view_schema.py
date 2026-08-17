from engine.core.io import validate_schema


def test_view_id_rejects_path_traversal() -> None:
    data = {
        "id": "../escape",
        "title": "TEST DATA",
        "diagramType": "use_case",
        "model": "model.yaml",
        "include": [],
    }
    assert validate_schema(data, "view.schema.json")
