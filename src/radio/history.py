"""
ArtistRadio Engine
Playback History Storage
"""

import json

from pathlib import Path


class PlaybackHistory:

    def __init__(
        self,
        path: Path,
        limit: int = 100,
    ):
        self.path = path
        self.limit = limit
        self._items: list[str] = []

        self.load()

    def add(
        self,
        track: str,
    ) -> None:

        self._items.append(
            track
        )

        if len(self._items) > self.limit:
            self._items.pop(0)

        self.save()

    def items(self) -> list[str]:
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

        self._items = json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )