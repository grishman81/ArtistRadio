"""
ArtistRadio Engine
Main
"""

from pathlib import Path

from src import config

from src.library.manager import LibraryManager
from src.library.library import Library

from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine

from src.station.manager import StationManager


STATIONS_CONFIG = Path("config/stations.json")


def main():
    manager = LibraryManager(
    music_root=config.MUSIC_ROOT,
    database_folder=config.DATABASE_FOLDER,
)

    try:
        manager.build()

        library = Library(config.DATABASE_FOLDER)

        history = PlaylistHistory()

        randomizer = PlaylistRandomizer(history)

        playlist = PlaylistEngine(
            randomizer,
            history,
        )

        stations = StationManager(
            library,
            playlist,
        )

        stations.load_from_file(
            STATIONS_CONFIG
        )

        print(
            f"Loaded stations: {stations.count}"
        )

    finally:
        manager.close()


if __name__ == "__main__":
    main()