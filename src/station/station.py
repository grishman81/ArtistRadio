"""
ArtistRadio Engine
Station
"""

from dataclasses import dataclass, field
from typing import Optional

from src.library.library import Library
from src.library.models import Track
from src.playlist.engine import PlaylistEngine


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

    history: list[Track] = field(default_factory=list)

    def next_track(self) -> Optional[Track]:
        """
        Выбирает следующий трек станции.
        """

        tracks = self.library.get_tracks(self.artist)

        if not tracks:
            return None

        track = self.playlist.next_track(tracks)

        if track is None:
            return None

        self.current_track = track
        self.add_history(track)

        return track

    def skip(self) -> Optional[Track]:
        """
        Пропустить текущий трек.
        """

        return self.next_track()

    def add_history(self, track: Track) -> None:
        """
        Добавляет трек в историю эфира.
        """

        self.history.append(track)

        if len(self.history) > 100:
            self.history.pop(0)