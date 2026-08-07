"""
ArtistRadio Engine
Playlist Engine
"""

from library.models import Track

from playlist.history import PlaylistHistory
from playlist.randomizer import PlaylistRandomizer


class PlaylistEngine:
    """
    Выбирает следующий трек для станции.
    """

    def __init__(
        self,
        randomizer: PlaylistRandomizer,
        history: PlaylistHistory,
    ):
        self.randomizer = randomizer
        self.history = history

    def next_track(self, tracks: list[Track]) -> Track | None:

        track = self.randomizer.choose(tracks)

        if track is None:
            return None

        self.history.add(track.path)

        return track