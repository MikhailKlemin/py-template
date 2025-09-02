from models.text import Text


class TextMerger:
    """Merge Text objects by key and context, accumulating sources."""

    def __init__(self):
        self._merged: dict[tuple[str, str], Text] = {}

    def add_texts(self, texts: list[Text]) -> "TextMerger":
        """Add a list of Texts to the merger."""
        for t in texts:
            identifier = (t.key, t.context)
            if identifier not in self._merged:
                self._merged[identifier] = Text(
                    key=t.key, context=t.context, sources=[])

            self._merged[identifier].sources.extend(t.sources)

        return self  # Allows chaining

    def get_merged(self) -> list[Text]:
        """Return the merged Text objects as a list."""
        return list(self._merged.values())
