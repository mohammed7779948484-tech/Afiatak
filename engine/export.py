from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET


def find_browser() -> str | None:
    candidates = [
        shutil.which("msedge"),
        shutil.which("chromium"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    return next((str(path) for value in candidates if value and (path := Path(value)).is_file()), None)


def find_edge() -> str | None:
    """Backward-compatible alias used by the existing diagnostic command."""
    return find_browser()


def _svg_size(source: Path) -> tuple[int, int]:
    root = ET.parse(source).getroot()
    width_value, height_value = root.get("width"), root.get("height")
    if width_value and height_value:
        try:
            width, height = int(float(width_value.rstrip("px"))), int(float(height_value.rstrip("px")))
        except ValueError:
            width = height = 0
        if width > 0 and height > 0:
            return width, height
    view_box = root.get("viewBox", "").split()
    if len(view_box) != 4:
        raise RuntimeError("SVG viewBox or numeric width/height are required for PNG rasterization")
    width, height = int(float(view_box[2])), int(float(view_box[3]))
    if width <= 0 or height <= 0:
        raise RuntimeError("SVG dimensions must be positive")
    return width, height


def export_svg_png(source: Path, output: Path) -> Path:
    width, height = _svg_size(source)
    browser = find_browser()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f"{output.stem}.tmp{output.suffix}")
    temporary.unlink(missing_ok=True)
    if browser:
        command = [
            browser,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={temporary}",
            source.resolve().as_uri(),
        ]
        environment = {**os.environ, "NO_PROXY": "localhost,127.0.0.1"}
        result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False, env=environment)
    else:
        convert = shutil.which("convert")
        if convert is None:
            raise RuntimeError("A Chromium-compatible browser or ImageMagick convert is required for SVG-to-PNG rasterization")
        result = subprocess.run(
            [convert, "-background", "#FAFAF8", str(source), str(temporary)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    if result.returncode or not temporary.is_file():
        raise RuntimeError((result.stdout + result.stderr).strip() or "SVG-to-PNG export failed")
    with temporary.open("rb") as stream:
        header = stream.read(24)
    if not header.startswith(b"\x89PNG\r\n\x1a\n") or len(header) < 24:
        temporary.unlink(missing_ok=True)
        raise RuntimeError("SVG rasterizer produced an invalid PNG")
    actual_width = int.from_bytes(header[16:20], "big")
    actual_height = int.from_bytes(header[20:24], "big")
    if (actual_width, actual_height) != (width, height):
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"SVG rasterizer produced {actual_width}×{actual_height}, expected {width}×{height}")
    temporary.replace(output)
    return output
