"""
ArtistRadio Engine
Album Mode Tests
"""

from pathlib import Path

from src.library.models import Track
from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine
from src.playlist.mode import PlaylistMode


def create_track(
    title,
    album="Test Album",
    number=1,
):

    return Track(
        title=title,
        album=album,
        track=number,
        path=Path(title),
    )


def test_album_mode_plays_album_in_order():

    history = PlaylistHistory()

    randomizer = PlaylistRandomizer(
        history
    )

    engine = PlaylistEngine(
        randomizer,
        history,
        PlaylistMode.ALBUM,
    )


    tracks = [
        create_track(
            "Track 1",
            number=1,
        ),
        create_track(
            "Track 2",
            number=2,
        ),
        create_track(
            "Track 3",
            number=3,
        ),
    ]


    first = engine.next_track(
        tracks
    )

    second = engine.next_track(
        tracks
    )

    third = engine.next_track(
        tracks
    )


    assert first.title == "Track 1"
    assert second.title == "Track 2"
    assert third.title == "Track 3"