"""
ArtistRadio Engine
Station
"""

from dataclasses import dataclass, field
from typing import Optional

from library.library import Library
from library.models import Track


@dataclass
class Station:
    """
    Представляет одну радиостанцию.
    """

    name: str
    artist: str

    bitrate: int = 320

    current_track: Optional[Track] = None

    history: list[Track] = field(default_factory=list)

    def next_track(self, library: Library) -> Optional[Track]:
        """
        Пока заглушка.

        В следующем пакете будет выбирать случайный трек
        исполнителя и следить за историей.
        """
        return None

    def add_history(self, track: Track) -> None:
        self.history.append(track)

        if len(self.history) > 100:
            self.history.pop(0)
