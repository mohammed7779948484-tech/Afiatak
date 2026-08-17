from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from engine.core.io import ROOT
from qa.diagnostics import Diagnostic


def validate_drawio(path: Path, *, run_skill_validator: bool = True) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if path.stat().st_size > 50 * 1024 * 1024:
        return [Diagnostic("Q4", "file-too-large", "Diagram exceeds 50 MiB", subject=str(path))]
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [Diagnostic("Q4", "malformed-xml", str(exc), subject=str(path))]
    cells = root.findall(".//mxCell")
    wrapper_ids = [wrapper.get("id") for wrapper in root.findall(".//object") if wrapper.get("id")]
    ids = [cell.get("id") for cell in cells if cell.get("id")] + wrapper_ids
    if "0" not in ids or "1" not in ids:
        diagnostics.append(
            Diagnostic("Q4", "missing-root", "Required root cells 0 and 1 are absent")
        )
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    for item in duplicates:
        diagnostics.append(
            Diagnostic("Q4", "duplicate-cell-id", "Duplicate draw.io cell ID", subject=item)
        )
    known = set(ids) | {wrapper.get("id", "") for wrapper in root.findall(".//object")}
    for cell in cells:
        parent = cell.get("parent")
        if parent and parent not in known:
            diagnostics.append(
                Diagnostic("Q4", "invalid-parent", "Unknown parent cell", subject=cell.get("id"))
            )
        if cell.get("edge") == "1":
            if cell.find("mxGeometry") is None:
                diagnostics.append(
                    Diagnostic(
                        "Q4", "edge-geometry", "Edge is missing mxGeometry", subject=cell.get("id")
                    )
                )
            for endpoint in ("source", "target"):
                if cell.get(endpoint) not in known:
                    diagnostics.append(
                        Diagnostic(
                            "Q4", "dangling-edge", f"Unknown {endpoint}", subject=cell.get("id")
                        )
                    )
    if run_skill_validator:
        validator = ROOT / ".agents" / "skills" / "drawio" / "scripts" / "validate.py"
        try:
            result = subprocess.run(
                [sys.executable, str(validator), str(path)],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            diagnostics.append(
                Diagnostic("Q4", "skill-validator-timeout", "Vendored validator timed out")
            )
            return diagnostics
        if result.returncode:
            diagnostics.append(
                Diagnostic(
                    "Q4",
                    "skill-validator",
                    (result.stdout + result.stderr).strip(),
                    subject=str(path),
                )
            )
    return diagnostics
