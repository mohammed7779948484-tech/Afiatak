from __future__ import annotations

import shutil
import subprocess
import sys
import os
from xml.etree import ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from engine.core.io import ROOT, load_yaml


@dataclass(frozen=True)
class Tool:
    path: str
    version: str


def find_drawio() -> Tool | None:
    candidates = [
        shutil.which("drawio"),
        shutil.which("draw.io"),
        str(Path(os.environ["LOCALAPPDATA"]) / "Programs" / "draw.io" / "draw.io.exe")
        if os.environ.get("LOCALAPPDATA")
        else None,
        r"C:\Program Files\draw.io\draw.io.exe",
    ]
    for candidate in filter(None, candidates):
        path = Path(candidate)
        if not path.exists():
            continue
        try:
            result = subprocess.run(
                [str(path), "--version"],
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        version = (result.stdout or result.stderr).strip()
        if result.returncode == 0 and version:
            return Tool(str(path), version)
    return None


def export_drawio(source: Path, output: Path, *, preview: bool = False) -> Path:
    tool = find_drawio()
    if tool is None:
        raise RuntimeError("draw.io desktop CLI is unavailable")
    output.parent.mkdir(parents=True, exist_ok=True)
    extension = output.suffix.lstrip(".").lower()
    command = [tool.path, "-x", "-f", extension]
    if preview:
        command.extend(["--width", "2000"])
    elif extension in {"png", "svg", "pdf"}:
        command.append("-e")
        if extension == "png":
            export_tokens = load_yaml(ROOT / "design" / "geometry.yaml")["export"]
            scale = int(export_tokens["png_scale"])
            model = ET.parse(source).getroot().find(".//mxGraphModel")
            if model is not None:
                largest = max(float(model.get("pageWidth", 0)), float(model.get("pageHeight", 0)))
                maximum = float(export_tokens["maximum_raster_dimension"])
                while scale > 1 and largest * scale > maximum:
                    scale -= 1
            command.extend(["-s", str(scale)])
    command.extend(["-o", str(output), str(source)])
    result = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
    if result.returncode or not output.exists():
        raise RuntimeError((result.stdout + result.stderr).strip() or "draw.io export failed")
    if not preview and extension == "png":
        repair = ROOT / ".agents" / "skills" / "drawio" / "scripts" / "repair_png.py"
        subprocess.run([sys.executable, str(repair), str(output)], check=True)
    return output


def browser_edit_url(source: Path) -> str:
    script = ROOT / ".agents" / "skills" / "drawio" / "scripts" / "encode_drawio_url.py"
    result = subprocess.run(
        [sys.executable, str(script), "--edit", str(source)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def assign_edge_ports(source: Path) -> None:
    script = ROOT / ".agents" / "skills" / "drawio" / "scripts" / "edgeports.py"
    result = subprocess.run(
        [sys.executable, str(script), str(source), "-o", str(source)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr).strip() or "edge-port assignment failed")
