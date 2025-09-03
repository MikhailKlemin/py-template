from os import path
import re
from html.parser import HTMLParser
from typing import Tuple, Optional, Sequence
from pathlib import Path
from models.text import Text


class NlsHTMLParser(HTMLParser):
    nls_pipe_regex: re.Pattern[str] = re.compile(
        r"\{\{\s*['\"](.+?)['\"]\s*\|\s*nls\s*\}\}")
    nls_func_regex: re.Pattern[str] = re.compile(
        r"\{\{\s*nls\.tr\(\s*['\"](.+?)['\"]\s*\)\s*\}\}")

    def __init__(self, path: str, base_path:str) -> None:
        super().__init__()
        self.results: list[Text] = []
        self.current_context: str = ""
        #self.path = path 
        base_path_resolved = Path(base_path).resolve()
        file_path_resolved = Path(path).resolve()
        self.rel_path =  file_path_resolved.relative_to(base_path_resolved.parent).as_posix()
        

    def handle_starttag(self, tag: str,
                        attrs: Sequence[Tuple[str, Optional[str]]]) -> None:
        for attr, value in attrs:
            if attr.lower() == "nlscontext" and value is not None:
                self.current_context = value

    def handle_data(self, data: str) -> None:
        matches: list[str] = self.nls_pipe_regex.findall(data)
        if matches:
            for match in matches:
                self.results.append(
                    Text(key=match, context=self.current_context,
                         sources=[self.rel_path]))
        else:
            matches_func: list[str] = self.nls_func_regex.findall(data)
            for match in matches_func:
                self.results.append(
                    Text(key=match, context=self.current_context,
                         sources=[self.rel_path]))


def parse_html(parse_path: str, base_path:str) -> list[Text]:
    path_obj: Path = Path(parse_path)
    if not path_obj.exists():
        raise FileNotFoundError(f"{path} does not exist")

    parser: NlsHTMLParser = NlsHTMLParser(path=parse_path, base_path=base_path)
    with path_obj.open("r", encoding="utf-8") as f:
        content: str = f.read()

        parser.feed(content)

    return parser.results
