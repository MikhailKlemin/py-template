from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Text:
    Key: str
    Value: Optional[str] = None
    Context: str = ""
    Comment: str = ""
    Sources: list[str] = field(default_factory=lambda: [])
    State: str = ""


@dataclass
class Result:
    Language: str = "en"
    Texts: list[Text] = field(default_factory=lambda: [])
