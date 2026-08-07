"""
ArtistRadio Engine
Station
"""

from dataclasses import dataclass, field
from typing import Optional

from src.library.library import Library
from src.library.models import Track
from src.playlist.engine import PlaylistEngine
from src.playlist.mode import PlaylistMode


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

    history: list[Track] = field(
        default_factory=list
    )


    def next_track(self) -> Optional[Track]:

        tracks = self.library.get_tracks(
            self.artist
        )

        if not tracks:
            return None


        track = self.playlist.next_track(
            tracks
        )

        if track is None:
            return None


        self.current_track = track

        self.add_history(
            track
        )

        return track


    def skip(self) -> Optional[Track]:

        return self.next_track()


    def add_history(
        self,
        track: Track,
    ) -> None:

        self.history.append(
            track
        )

        if len(self.history) > 100:

            self.history.pop(0)


    def set_mode(
        self,
        mode: PlaylistMode,
    ) -> None:
        """
        Меняет режим воспроизведения станции.
        """

        self.playlist.mode = mode

        self.playlist.position = 0


    def get_mode(self) -> PlaylistMode:
        """
        Возвращает текущий режим станции.
        """

        return self.playlist.mode