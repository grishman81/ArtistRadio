"""
ArtistRadio Engine
Playback History Storage
"""

import json

from pathlib import Path

from src.library.models import Track


class PlaybackHistory:

    def __init__(
        self,
        path: Path,
        limit: int = 100,
    ):
        self.path = path
        self.limit = limit
        self._items: list[dict] = []

        self.load()

    def add(
        self,
        track: Track,
    ) -> None:

        item = {
            "artist": track.artist,
            "album": track.album,
            "title": track.title,
            "year": track.year,
            "path": str(track.path),
        }

        self._items.append(
            item
        )

        if len(self._items) > self.limit:
            self._items.pop(0)

        self.save()

    def items(self) -> list[dict]:
        return list(
            reversed(self._items)
        )

    def clear(self) -> None:
        self._items.clear()
        self.save()

    def save(self) -> None:

        self.path.write_text(
            json.dumps(
                self._items,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load(self) -> None:

        if not self.path.exists():
            return

        data = json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

        self._items = data