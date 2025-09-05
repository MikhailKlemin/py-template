import typer
from pathlib import Path
from scanners.scanner import FileScanner
from parsers.html import parse_html
from parsers.ts import parse_ts
from combiners.combiner import TextMerger
from models.text import Result, Text
from exporteurs.json import ResultJSONExporter


def main(
    dir: Path = typer.Option(".", help="Directory to scan"),
    out: Path = typer.Option("translations.json", help="Output JSON file"),
    pretty: bool = typer.Option(False, help="Pretty-print JSON"),
    nosources: bool = typer.Option(False, help="Exlude sources files"),

    debug: bool = typer.Option(
        False, help="Include debug info (sources, etc.)"),
):
    scanner = FileScanner()
    files: list[Path] = scanner.walk(dir)

    if debug:
        typer.echo(f"Found {len(files)} files")
        for f in files:
            typer.echo(f"- {f}")

    all_results: list[Text] = []

    for f in files:
        if f.suffix.lower() == ".html":
            if debug:
                typer.echo(f"Parsing HTML file: {f}")
            try:
                h:  list[Text] = parse_html(str(f), base_path=dir.as_posix())
                all_results.extend(h)
            except Exception as e:
                typer.echo(f"Error parsing {f}: {e}")
        elif f.suffix.lower() == ".ts":
            if debug:
                typer.echo(f"Parsing HTML file: {f}")
            try:
                t:  list[Text] = parse_ts(str(f), base_path=dir.as_posix())
                all_results.extend(t)
            except Exception as e:
                typer.echo(f"Error parsing {f}: {e}")

    merged_texts = TextMerger().add_texts(all_results).get_merged()
    sorted_texts = sorted(merged_texts, key=lambda x: (x.Key, x.Context))
    result: Result = Result(Texts=sorted_texts)

    exporter = ResultJSONExporter(exclude_sources=nosources, pretty=pretty)
    json_output: str = exporter.to_json(result)
    robust_write(json_output, out)


def robust_write(text: str, filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    except IOError as e:
        print(f'Write failed: {e}')


if __name__ == "__main__":
    typer.run(main)
