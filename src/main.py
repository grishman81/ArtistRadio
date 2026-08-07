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
from src.station.generator import StationGenerator

from src.radio.engine import RadioEngine
from src.radio.session import RadioSession
from src.radio.storage import RadioStorage

from src.audio.player import AudioPlayer

from src.console.app import ConsoleApp


RADIO_STATE_FILE = Path(
    "radio_state.json"
)


def select_station(
    stations: StationManager
):
    available = stations.all()

    if not available:
        raise RuntimeError(
            "No stations available"
        )

    print()
    print("Available stations:")

    for index, station in enumerate(
        available,
        start=1,
    ):
        print(
            f"{index}. {station.name}"
        )

    while True:
        choice = input(
            "Select station: "
        ).strip()

        try:
            index = int(choice) - 1

            return available[index]

        except (
            ValueError,
            IndexError,
        ):
            print(
                "Invalid selection"
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

        generator = StationGenerator(
            library,
            playlist,
        )

        for station in generator.generate():
            stations.add(
                station
            )

        print(
            f"Loaded stations: {stations.count}"
        )

        station = select_station(
            stations
        )

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