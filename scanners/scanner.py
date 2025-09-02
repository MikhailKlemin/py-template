from pathlib import Path
from typing import List, Set
import os


class FileScanner:
    def __init__(self, skip_dirs: Set[str] | None = None,
                 allowed_exts: Set[str] | None = None):
        self.skip_dirs: Set[str] = skip_dirs or {
            "node_modules", ".git", "dist", "build"}
        self.allowed_exts: Set[str] = allowed_exts or {
            ".html", ".ts", ".qml", ".cpp", ".h"}

    def walk(self, root: Path) -> List[Path]:
        """
        Walk the given root directory and collect allowed files,
        skipping disallowed directories.
        """
        files: List[Path] = []

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in self.skip_dirs]

            for fname in filenames:
                ext = Path(fname).suffix.lower()
                if ext in self.allowed_exts:
                    files.append(Path(dirpath) / fname)

        return files
