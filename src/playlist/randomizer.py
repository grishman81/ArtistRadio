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
        avoid_artists: bool = True,
        avoid_albums: bool = True,
    ):

        self.history = history

        self.avoid_last = avoid_last

        self.avoid_artists = avoid_artists

        self.avoid_albums = avoid_albums



    def choose(
        self,
        tracks: list[Track],
    ) -> Track | None:


        if not tracks:

            return None



        candidates = list(
            tracks
        )



        recent_paths = set(
            self.history.items()[
                -self.avoid_last:
            ]
        )


        candidates = [
            track
            for track in candidates
            if str(track.path)
            not in recent_paths
        ]



        if self.avoid_artists:

            recent_artists = set()


            if hasattr(
                self.history,
                "artists",
            ):

                recent_artists = set(
                    self.history.artists()[
                        -self.avoid_last:
                    ]
                )


            filtered = [
                track
                for track in candidates
                if track.artist
                not in recent_artists
            ]


            if filtered:

                candidates = filtered



        if self.avoid_albums:

            recent_albums = set()


            if hasattr(
                self.history,
                "albums",
            ):

                recent_albums = set(
                    self.history.albums()[
                        -self.avoid_last:
                    ]
                )


            filtered = [
                track
                for track in candidates
                if track.album
                not in recent_albums
            ]


            if filtered:

                candidates = filtered



        if not candidates:

            candidates = tracks



        return random.choice(
            candidates
        )