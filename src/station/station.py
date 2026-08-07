"""
ArtistRadio Engine
Station
"""

from dataclasses import dataclass
from typing import Optional

from ..library.library import Library
from ..library.models import Track
from ..playlist.engine import PlaylistEngine


@dataclass
class Station:
    """
    Представляет одну радиостанцию.
    """

    name: str
    artist: str
    library: Library
    playlist: PlaylistEngine

    bitrate: int = 320

    current_track: Optional[Track] = None

    def next_track(self) -> Optional[Track]:
        """
        Выбирает следующий трек станции.
        """

        tracks = self.library.get_tracks(self.artist)

        if not tracks:
            return None

        self.current_track = self.playlist.next_track(tracks)

        return self.current_track