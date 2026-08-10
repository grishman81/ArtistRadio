"""
ArtistRadio Engine
Playlist History
"""

from collections import deque
from pathlib import Path


class PlaylistHistory:
    """
    Хранит историю недавно воспроизведённых треков.
    """


    def __init__(
        self,
        limit: int = 100,
    ):

        self._items = deque(
            maxlen=limit
        )



    def add(
        self,
        track,
    ) -> None:


        if hasattr(
            track,
            "path",
        ):

            item = {
                "path": str(track.path),
                "artist": getattr(
                    track,
                    "artist",
                    None,
                ),
                "album": getattr(
                    track,
                    "album",
                    None,
                ),
            }


        else:

            item = {
                "path": str(track),
                "artist": None,
                "album": None,
            }


        self._items.append(
            item
        )



    def contains(
        self,
        track_path: Path,
    ) -> bool:

        path = str(
            track_path
        )


        return any(
            item["path"] == path
            for item in self._items
        )



    def contains_artist(
        self,
        artist: str,
    ) -> bool:

        if artist is None:

            return False


        return any(
            item["artist"] == artist
            for item in self._items
        )



    def contains_album(
        self,
        album: str,
    ) -> bool:

        if album is None:

            return False


        return any(
            item["album"] == album
            for item in self._items
        )



    def clear(
        self,
    ) -> None:

        self._items.clear()



    def items(
        self,
    ) -> list[str]:

        """
        Возвращает историю путей треков.
        Совместимость со старой логикой.
        """

        return [
            item["path"]
            for item in self._items
        ]



    def details(
        self,
    ) -> list[dict]:

        return list(
            self._items
        )



    def artists(
        self,
    ) -> list[str]:

        return [
            item["artist"]
            for item in self._items
            if item["artist"] is not None
        ]



    def albums(
        self,
    ) -> list[str]:

        return [
            item["album"]
            for item in self._items
            if item["album"] is not None
        ]



    def last(
        self,
    ) -> str | None:

        if not self._items:

            return None


        return self._items[-1]["path"]



    def last_artist(
        self,
    ) -> str | None:

        if not self._items:

            return None


        return self._items[-1]["artist"]



    def last_album(
        self,
    ) -> str | None:

        if not self._items:

            return None


        return self._items[-1]["album"]



    @property
    def size(
        self,
    ) -> int:

        return len(
            self._items
        )