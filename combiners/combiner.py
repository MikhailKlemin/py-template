from models.text import Text


class TextMerger:
    """Merge Text objects by key and context, accumulating sources."""

    def __init__(self):
        self._merged: dict[tuple[str, str], Text] = {}

    def add_texts(self, texts: list[Text]) -> "TextMerger":
        """Add a list of Texts to the merger."""
        for t in texts:
            identifier = (t.Key, t.Context)
            if identifier not in self._merged:
                self._merged[identifier] = Text(
                    Key=t.Key, Context=t.Context, Sources=[])

            self._merged[identifier].Sources.extend(t.Sources)

        return self  # Allows chaining

    def get_merged(self) -> list[Text]:
        """Return the merged Text objects as a list."""
        return list(self._merged.values())
