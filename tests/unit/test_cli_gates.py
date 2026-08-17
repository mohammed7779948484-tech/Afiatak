import json
from argparse import Namespace

import engine.cli as cli


def test_qa_command_fails_while_visual_review_is_pending(tmp_path, monkeypatch) -> None:
    report = tmp_path / "qa.json"
    report.write_text(
        json.dumps({"gates": {"Q6": {"applicable": True, "status": "awaiting_review"}}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(cli, "qa", lambda path: (report, []))
    assert cli.command_qa(Namespace(view="view.yaml")) == 1
