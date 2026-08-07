"""
ArtistRadio Engine
Station Tests
"""

from pathlib import Path

from src.library.library import Library
from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine
from src.station.station import Station
from src.station.manager import StationManager


DATABASE = Path("database")


def create_station(name="Jennifer Lopez Radio"):
    library = Library(DATABASE)

    history = PlaylistHistory()

    randomizer = PlaylistRandomizer(history)

    playlist = PlaylistEngine(
        randomizer,
        history,
    )

    return Station(
        name=name,
        artist="Jennifer Lopez",
        library=library,
        playlist=playlist,
    )


def test_station_manager_add_and_get():
    manager = StationManager()

    station = create_station()

    manager.add(station)

    assert manager.count == 1
    assert manager.get("Jennifer Lopez Radio") is station


def test_station_manager_remove():
    manager = StationManager()

    station = create_station()

    manager.add(station)
    manager.remove(station.name)

    assert manager.count == 0


def test_station_next_track():
    station = create_station()

    track = station.next_track()

    assert track is not None
    assert track.title
    assert station.current_track == track