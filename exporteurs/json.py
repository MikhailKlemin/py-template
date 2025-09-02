import json
from dataclasses import asdict
from models.text import Result
from typing import cast


class ResultJSONExporter:
    def __init__(self, exclude_sources: bool = False,
                 pretty: bool = False) -> None:
        self.exclude_sources: bool = exclude_sources
        self.pretty: bool = pretty

    def to_dict(self, result: Result) -> dict[str, object]:
        """Convert Result dataclass to a plain dict, applying options."""
        result_dict: dict[str, object] = asdict(result)

        if self.exclude_sources:
            texts = cast(list[dict[str, object]], result_dict.get("texts", []))
            for text in texts:
                text.pop("sources", None)

        return result_dict

    def to_json(self, result: Result) -> str:
        """Convert Result dataclass to a JSON string."""
        result_dict = self.to_dict(result)
        return json.dumps(
            result_dict,
            indent=2 if self.pretty else None,
            ensure_ascii=False,
        )

    def export_to_file(self, path: str, result: Result) -> None:
        """Write JSON representation of Result to a file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json(result))
