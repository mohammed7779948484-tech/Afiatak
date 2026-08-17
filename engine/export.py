from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def find_edge() -> str | None:
    candidates = [
        shutil.which("msedge"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    return next((str(path) for value in candidates if value and (path := Path(value)).is_file()), None)


def export_svg_png(source: Path, output: Path) -> Path:
    edge = find_edge()
    if edge is None:
        raise RuntimeError("Microsoft Edge is required for local SVG-to-PNG rasterization")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f"{output.stem}.tmp{output.suffix}")
    temporary.unlink(missing_ok=True)
    command = [
        edge,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=1920,1080",
        f"--screenshot={temporary}",
        source.resolve().as_uri(),
    ]
    environment = {**os.environ, "NO_PROXY": "localhost,127.0.0.1"}
    result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False, env=environment)
    if result.returncode or not temporary.is_file():
        raise RuntimeError((result.stdout + result.stderr).strip() or "SVG-to-PNG export failed")
    with temporary.open("rb") as stream:
        header = stream.read(24)
    if not header.startswith(b"\x89PNG\r\n\x1a\n") or header[16:24] != b"\x00\x00\x07\x80\x00\x00\x048":
        temporary.unlink(missing_ok=True)
        raise RuntimeError("SVG rasterizer produced an invalid or unexpected PNG")
    temporary.replace(output)
    return output
