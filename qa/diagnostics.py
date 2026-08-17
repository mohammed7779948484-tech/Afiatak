from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnostic:
    gate: str
    code: str
    message: str
    severity: str = "error"
    subject: str | None = None

    def __str__(self) -> str:
        where = f" [{self.subject}]" if self.subject else ""
        return f"{self.gate} {self.severity.upper()} {self.code}{where}: {self.message}"
