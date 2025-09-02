import re
from pathlib import Path
from models.text import Text


class NlsTSParser:
    ts_regex: re.Pattern[str] = re.compile(
        r'nls\.tr\(\s*"(.*?)"\s*\)|nls\.tr\(\s*\'(.*?)\'\s*\)'
    )

    def __init__(self, path: str) -> None:
        self.results: list[Text] = []
        self.current_context: str = ""
        self.path = path

    def feed(self, data: str) -> None:
        matches = self.ts_regex.findall(data)
        for m in matches:
            key = m[0] if m[0] else m[1]
            self.results.append(
                Text(
                    key=key,
                    context=self.current_context,
                    sources=[self.path],
                )
            )


def parse_ts(parse_path: str) -> list[Text]:
    path_obj = Path(parse_path)
    if not path_obj.exists():
        raise FileNotFoundError(f"{parse_path} does not exist")

    parser = NlsTSParser(path=parse_path)
    content = path_obj.read_text(encoding="utf-8")
    parser.feed(content)

    return parser.results
