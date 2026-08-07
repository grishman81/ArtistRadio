"""
ArtistRadio Engine
Playlist Randomizer
"""

import random

from ..library.models import Track
from .history import PlaylistHistory


class PlaylistRandomizer:
    """
    Выбирает случайный трек, которого нет в истории.
    """

    def __init__(self, history: PlaylistHistory):
        self.history = history

    def choose(self, tracks: list[Track]) -> Track | None:

        if not tracks:
            return None

        candidates = [
            track
            for track in tracks
            if not self.history.contains(track.path)
        ]

        if not candidates:
            self.history.clear()
            candidates = tracks

        return random.choice(candidates)