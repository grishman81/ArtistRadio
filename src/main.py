"""
ArtistRadio Engine
Main
"""

from pathlib import Path

from config import MUSIC_ROOT, DATABASE_FOLDER

from library.manager import LibraryManager
from library.library import Library

from playlist.history import PlaylistHistory
from playlist.randomizer import PlaylistRandomizer
from playlist.engine import PlaylistEngine

from station.manager import StationManager


STATIONS_CONFIG = Path("config/stations.json")


def main():
    manager = LibraryManager(
        music_root=MUSIC_ROOT,
        database_folder=DATABASE_FOLDER,
    )

    try:
        manager.build()

        library = Library(DATABASE_FOLDER)

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