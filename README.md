# py-template

# Translation String Extractor

This tool scans `.ts` and `.html` source files to collect translation keys and metadata, then exports them into a structured JSON file.  
It is intended to be used as part of an internationalization (i18n) workflow, where the extracted strings can be translated with other applications.

---

## Features

- Recursively scans a directory for `.ts` and `.html` files
- Extracts translation strings with metadata:
  - **key** – translation key
  - **value** – optional default value
  - **context** – additional context for translators
  - **comment** – developer notes
  - **sources** – list of files where the key is used
  - **state** – state of the translation
- Merges duplicate keys across files
- Exports results to JSON (optionally pretty-printed)

Example output structure:

```python
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
```

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/translation-extractor.git
cd translation-extractor
pip install -r requirements.txt
```

---

## Usage

Run the CLI tool with:

```bash
python cli.py [OPTIONS]
```

### Options

- `--dir PATH`  
  Directory to scan (default: `.`)

- `--out PATH`  
  Output JSON file (default: `translations.json`)

- `--pretty`  
  Pretty-print JSON output

- `--nosources`  
  Exclude source file references from the output

- `--debug`  
  Show detailed scan and parsing logs

---

### Examples

Scan the current directory and write to `translations.json`:

```bash
python cli.py
```

Scan a specific project folder and pretty-print the JSON:

```bash
python cli.py --dir ./src --out result.json --pretty
```

Exclude source file paths:

```bash
python cli.py --nosources
```

Enable debug output:

```bash
python cli.py --debug
```

---

## Output

A generated `translations.json` file might look like this:

```json
{
  "language": "en",
  "texts": [
    {
      "key": "hello_world",
      "value": "",
      "context": "",
      "comment": "Displayed on home page",
      "sources": ["src/app/app.component.html"],
      "state": ""
    },
    {
      "key": "logout",
      "value": "",
      "context": "",
      "comment": "",
      "sources": ["src/components/navbar.ts"],
      "state": ""
    }
  ]
}
```

---

## Project Structure

```
.
├── cli.py                 # CLI entry point
├── scanners/
│   └── scanner.py         # File scanner
├── parsers/
│   ├── html.py            # HTML parser
│   └── ts.py              # TS parser
├── combiners/
│   └── combiner.py        # Merges duplicate translation keys
├── exporteurs/
│   └── json.py            # JSON exporter
├── models/
│   └── text.py            # Data models (Text, Result)
└── requirements.txt       # Dependencies
```
