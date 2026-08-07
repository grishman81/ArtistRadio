"""
ArtistRadio Engine
Station Loader Tests
"""

import json
from pathlib import Path

from src.library.library import Library
from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine
from src.station.loader import StationLoader


def test_station_loader(tmp_path):
    config_file = tmp_path / "stations.json"

    config_file.write_text(
        json.dumps(
            [
                {
                    "name": "Jennifer Lopez Radio",
                    "artist": "Jennifer Lopez",
                    "bitrate": 320,
                }
            ]
        ),
        encoding="utf-8",
    )

    library = Library(Path("database"))

    history = PlaylistHistory()

    randomizer = PlaylistRandomizer(history)

    playlist = PlaylistEngine(
        randomizer,
        history,
    )

    loader = StationLoader(
        library,
        playlist,
    )

    stations = loader.load(config_file)

    assert len(stations) == 1
    assert stations[0].name == "Jennifer Lopez Radio"
    assert stations[0].artist == "Jennifer Lopez"