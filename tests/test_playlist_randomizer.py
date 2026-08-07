"""
ArtistRadio Engine
Playlist Randomizer Tests
"""

from pathlib import Path

from src.library.models import Track
from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer


def make_track(name: str) -> Track:
    return Track(
        title=name,
        path=Path(name + ".mp3"),
    )


def test_randomizer_avoids_recent_tracks():

    history = PlaylistHistory()

    history.add(
        Path("A.mp3")
    )

    history.add(
        Path("B.mp3")
    )

    history.add(
        Path("C.mp3")
    )

    randomizer = PlaylistRandomizer(
        history,
        avoid_last=3,
    )

    tracks = [
        make_track("A"),
        make_track("B"),
        make_track("C"),
        make_track("D"),
    ]

    selected = randomizer.choose(
        tracks
    )

    assert selected.title == "D"