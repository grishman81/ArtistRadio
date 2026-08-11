"""
ArtistRadio Engine
CLI Entry Point
"""

from pathlib import Path
import sys

from src.library.library import Library

from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine

from src.station.station import Station

from src.radio.engine import RadioEngine
from src.radio.session import RadioSession
from src.radio.storage import RadioStorage
from src.radio.history import PlaybackHistory

from src.audio.player import AudioPlayer

from src.cli.app import RadioCLI


def create_session():

    library = Library(Path("database"))

    playlist_history = PlaylistHistory()

    randomizer = PlaylistRandomizer(playlist_history)

    playlist = PlaylistEngine(
        randomizer,
        playlist_history,
    )

    station = Station(
        name="Jennifer Lopez Radio",
        artist="Jennifer Lopez",
        library=library,
        playlist=playlist,
    )

    radio = RadioEngine(station)

    storage = RadioStorage(Path("radio_state.json"))

    history = PlaybackHistory(Path("radio_history.json"))

    player = AudioPlayer()

    return RadioSession(
        radio,
        storage,
        player,
        history,
    )


def main():

    if len(sys.argv) < 2:

        print("Usage: artist-radio <command>")

        return

    command = sys.argv[1]

    session = create_session()

    cli = RadioCLI(session)

    if command == "start":

        cli.start()

        print("Radio started")

    elif command == "stop":

        cli.stop()

        print("Radio stopped")

    elif command == "pause":

        cli.pause()

        print("Radio paused")

    elif command == "resume":

        cli.resume()

        print("Radio resumed")

    elif command == "next":

        track = cli.next()

        print(track)

    elif command == "queue":

        queue = cli.queue()

        print()
        print("📻 Queue")
        print("--------------------")

        if not queue:

            print("Queue is empty")

        else:

            for index, track in enumerate(
                queue,
                1,
            ):

                print(f"{index}. {track}")

    elif command == "history":

        history = cli.history()

        print()
        print("📜 History")
        print("--------------------")

        if not history:

            print("History is empty")

        else:

            for index, item in enumerate(
                history,
                1,
        ):

                print(
                    f"{index}. "
                    f"{item['artist']} - "
                    f"{item['title']} "
                    f"({item['year']})"
                )
    elif command == "run":

        cli.start()

        print()
        print("📻 ArtistRadio is running")
        print("Press Ctrl+C to stop")
        print()

        try:

            while True:

                cli.session.check_playback()

                import time

                time.sleep(1)

        except KeyboardInterrupt:

            print()
            print("Stopping radio...")

            cli.stop()

    else:

        print(f"Unknown command: {command}")


if __name__ == "__main__":

    main()
