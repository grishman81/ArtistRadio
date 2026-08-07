"""
ArtistRadio Engine
Station Generator Tests
"""

from pathlib import Path

from src.library.library import Library
from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine
from src.station.generator import StationGenerator


DATABASE = Path("database")


def test_station_generator_creates_artist_stations():

    library = Library(
        DATABASE
    )

    history = PlaylistHistory()

    randomizer = PlaylistRandomizer(
        history
    )

    playlist = PlaylistEngine(
        randomizer,
        history,
    )

    generator = StationGenerator(
        library,
        playlist,
    )

    stations = generator.generate()

    names = [
        station.name
        for station in stations
    ]

    assert "Jennifer Lopez Radio" in names
    assert "Madonna Radio" in names
    assert "Michael Jackson Radio" in names