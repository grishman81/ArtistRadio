"""
ArtistRadio Engine
Playlist Engine
"""

from src.library.models import Track

from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.mode import PlaylistMode


class PlaylistEngine:


    def __init__(
        self,
        randomizer: PlaylistRandomizer,
        history: PlaylistHistory,
        mode: PlaylistMode = PlaylistMode.RANDOM,
    ):

        self.randomizer = randomizer
        self.history = history
        self.mode = mode

        self.position = 0
        self.album_tracks = []
        self.album_name = None



    def next_track(
        self,
        tracks: list[Track],
    ) -> Track | None:


        if not tracks:

            return None



        if self.mode == PlaylistMode.SEQUENTIAL:


            track = tracks[
                self.position % len(tracks)
            ]

            self.position += 1



        elif self.mode == PlaylistMode.ALBUM:


            current_album = tracks[0].album


            if (
                not self.album_tracks
                or self.album_name != current_album
            ):

                self.album_tracks = [
                    track
                    for track in tracks
                    if track.album == current_album
                ]

                self.album_name = current_album
                self.position = 0



            track = self.album_tracks[
                self.position % len(self.album_tracks)
            ]

            self.position += 1



        else:


            track = self.randomizer.choose(
                tracks
            )



        if track is None:

            return None



        self.history.add(
            track.path
        )


        return track