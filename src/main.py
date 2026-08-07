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


def select_station(stations):

    available = stations.all()

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
        )

        try:
            return available[
                int(choice) - 1
            ]

        except (
            ValueError,
            IndexError,
        ):
            print(
                "Invalid selection"
            )


def restore_station(
    stations,
    storage,
):
    state = storage.load()

    if not state.station:
        return None

    station = stations.get(
        state.station
    )

    if not station:
        return None

    print()
    print(
        f"Last station: {station.name}"
    )
    print(
        "1. Continue"
    )
    print(
        "2. Choose another"
    )

    choice = input(
        "> "
    )

    if choice == "1":
        return station

    return None


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

        storage = RadioStorage(
            RADIO_STATE_FILE
        )

        station = restore_station(
            stations,
            storage,
        )

        if station is None:
            station = select_station(
                stations
            )

        radio = RadioEngine(
            station
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