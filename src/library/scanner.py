"""
ArtistRadio Engine
Library Scanner
"""

from pathlib import Path

from config import SUPPORTED_FORMATS
from .metadata import MetadataReader
from .models import Track


class LibraryScanner:

    def __init__(self, music_root: Path):
        self.music_root = Path(music_root)
        self.reader = MetadataReader()

    def scan(self):
        """Возвращает объекты Track для всех найденных аудиофайлов."""
        for file in self.music_root.rglob("*"):
            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_FORMATS:
                continue

            try:
                yield self.reader.read(file)
            except Exception as exc:
                print(f"[WARNING] {file}")
                print(f"          {exc}")
