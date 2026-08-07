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

from src.radio.engine import RadioEngine
from src.radio.session import RadioSession
from src.radio.storage import RadioStorage

from src.audio.player import AudioPlayer

from src.console.app import ConsoleApp


STATIONS_CONFIG = Path(
    "config/stations.json"
)

RADIO_STATE_FILE = Path(
    "radio_state.json"
)


def main():
    manager = LibraryManager(
        music_root=config.MUSIC_ROOT,
        database_folder=config.DATABASE_FOLDER,
    )

    try:
        manager.build()

        library = Library(
            config.DATABASE_FOLDER
        )

        history = PlaylistHistory()

        randomizer = PlaylistRandomizer(
            history
        )

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

        station = stations.all()[0]

        radio = RadioEngine(
            station
        )

        storage = RadioStorage(
            RADIO_STATE_FILE
        )

        player = AudioPlayer()

        session = RadioSession(
            radio,
            storage,
            player,
        )

        session.start()

        console = ConsoleApp(
            session,
            stations,
        )

        console.run()

    finally:
        manager.close()


if __name__ == "__main__":
    main()