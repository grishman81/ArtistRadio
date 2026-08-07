"""
ArtistRadio Engine
Library Tests
"""

from pathlib import Path

from src.library.library import Library
from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine
from src.station.station import Station


DATABASE = Path("database")


def create_station():
    library = Library(DATABASE)

    history = PlaylistHistory()

    randomizer = PlaylistRandomizer(history)

    playlist = PlaylistEngine(
        randomizer,
        history,
    )

    station = Station(
        name="Jennifer Lopez Radio",
        artist="Jennifer Lopez",
        library=library,
        playlist=playlist,
    )

    return library, station


def test_library_returns_tracks():
    library = Library(DATABASE)

    tracks = library.get_tracks("Jennifer Lopez")

    assert len(tracks) > 0
    assert tracks[0].title

    library.close()


def test_station_returns_next_track():
    library, station = create_station()

    track = station.next_track()

    assert track is not None
    assert track.title
    assert track.path

    library.close()


def test_playlist_avoids_repeat():
    library, station = create_station()

    track1 = station.next_track()
    track2 = station.next_track()

    assert track1.path != track2.path

    library.close()