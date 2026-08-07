"""
ArtistRadio Engine
Playlist Randomizer
"""

import random

from src.library.models import Track

from .history import PlaylistHistory


class PlaylistRandomizer:

    def __init__(
        self,
        history: PlaylistHistory,
        avoid_last: int = 5,
    ):
        self.history = history
        self.avoid_last = avoid_last


    def choose(
        self,
        tracks: list[Track],
    ) -> Track | None:

        if not tracks:
            return None


        recent = set(
            self.history.items()[
                -self.avoid_last:
            ]
        )


        candidates = [
            track
            for track in tracks
            if str(track.path)
            not in recent
        ]


        if not candidates:
            candidates = tracks


        return random.choice(
            candidates
        )