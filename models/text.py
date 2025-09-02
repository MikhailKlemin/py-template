from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Text:
    key: str
    value: Optional[str] = None
    context: str = ""
    comment: str = ""
    sources: list[str] = field(default_factory=lambda: [])
    state: str = ""


@dataclass
class Result:
    language: str = "en"
    texts: list[Text] = field(default_factory=lambda: [])
