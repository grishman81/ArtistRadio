"""
ArtistRadio Engine
Playlist Engine
"""

from library.models import Track
from .history import PlaylistHistory
from .randomizer import PlaylistRandomizer


class PlaylistEngine:
    """
    Выбирает следующий трек для станции.
    """

    def __init__(self, randomizer: PlaylistRandomizer):
        self.history = PlaylistHistory()
        self.randomizer = randomizer

    def next_track(self, tracks: list[Track]) -> Track | None:
        track = self.randomizer.choose(tracks)

        if track is None:
            return None

        self.history.add(track.path)
        return track
