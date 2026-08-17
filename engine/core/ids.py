from __future__ import annotations

import re

ID_PATTERN = re.compile(
    r"^(actor|uc|package|class|object|state|component|node|scenario|relation|activity|message)\.[a-z0-9][a-z0-9._-]*$"
)


def validate_id(value: str) -> bool:
    return bool(ID_PATTERN.fullmatch(value))


def drawio_id(value: str) -> str:
    """Stable, XML-safe ID distinct from draw.io's reserved numeric roots."""
    if not validate_id(value):
        raise ValueError(f"invalid semantic id: {value}")
    return f"sem-{value}"
