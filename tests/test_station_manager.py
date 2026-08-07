"""
ArtistRadio Engine
Station Manager Tests
"""

import json
from pathlib import Path

from src.library.library import Library
from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine
from src.station.manager import StationManager


def test_manager_load_from_file(tmp_path):
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

    manager = StationManager(
        library,
        playlist,
    )

    manager.load_from_file(config_file)

    assert manager.count == 1
    assert manager.get("Jennifer Lopez Radio") is not None