"""
ArtistRadio Engine
CLI Entry Point
"""

from pathlib import Path
import sys
import time
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


def format_time(seconds: float) -> str:

    seconds = int(seconds)

    minutes = seconds // 60

    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


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

        cli.session.state.command = "pause"
        cli.session.save()

        print("Pause command sent")

    elif command == "resume":

        cli.session.state.command = "resume"
        cli.session.save()

        print("Resume command sent")

    elif command == "next":

        cli.session.state.command = "next"
        cli.session.save()

        print("Next command sent")

    elif command == "queue-clear":

        cli.session.state.command = "queue_clear"
        cli.session.save()

        print("Queue clear command sent")    

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

                track_obj = (
                    cli.session
                    .radio
                    .station
                    .library
                    .tracks
                    .get_by_path(
                        track
                    )
                )

                if track_obj:

                    print(
                        f"{index}. "
                        f"{track_obj.artist} - "
                        f"{track_obj.title}"
                    )

                else:

                    print(
                        f"{index}. {track}"
                    )

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

    elif command == "status":

        status = cli.status()

        print()
        print("📻 ArtistRadio Status")
        print("--------------------")
        print()

        if status["track"]:

            if status["running"]:
                print("▶ Playing")
            else:
                print("⏸ Paused")

            print()

            track = cli.session.radio.station.library.tracks.get_by_path(
                status["track"]
            )

            if track:

                print("Artist:")
                print(f"   {track.artist}")

                print()

                print("Track:")
                print(f"   {track.title}")

                print()

                print("💿 Album:")
                print(f"   {track.album}")

                print()

                print("📅 Year:")
                print(f"   {track.year}")

                print()

                print("🎵 Genre:")
                print(f"   {track.genre}")

                print()

                print("⏱ Position:")
                print(
                    f"   {format_time(status['position'])} / "
                    f"{format_time(track.duration)}"
                )

                print()

                if status["crossfade_running"]:

                    progress = (
                        status["crossfade_progress"]
                        * 100
                    )

                    print("🎚️ Crossfade:")
                    print(
                        f"   ACTIVE "
                        f"{progress:.0f}%"
                    )

                    if status["next_track"]:

                        print()

                        print("▶ Next:")
                        print(
                            f"   {status['next_track']}"
                        )

                else:

                    print("🎚️ Crossfade:")
                    print("   Inactive")

                print()

                print(
                    f"📋 Queue: "
                    f"{len(status['queue'])} tracks"
                )

        else:

            print("Radio is stopped")

    elif command == "run":

        cli.start()

        if cli.session.player.current is None:

            cli.session.play_next()

        print()
        print("📻 ArtistRadio Live")
        print("--------------------")
        print()

        last_track = None

        try:

            while True:

                cli.session.check_playback()

                state = cli.session.state

                track = cli.session.current_track

                if track:

                    print("\033[H\033[J", end="")

                    print()
                    print("📻 ArtistRadio Live")
                    print("--------------------")
                    print()

                    print("▶ Now:")
                    print(f"   {track.artist} - {track.title}")

                    print()

                    print("💿 Album:")
                    print(f"   {track.album}")

                    print()

                    print("📅 Year:")
                    print(f"   {track.year}")

                    print()

                    position = cli.session.player.current_position()

                    cli.session.state.position = position

                    cli.session.save()

                    print("⏱ Progress:")

                    print(
                        f"   {format_time(position)} / "
                        f"{format_time(track.duration)}"
                    )

                    bar_size = 20

                    filled = int(
                        bar_size
                        * position
                        / max(track.duration, 1)
                    )

                    bar = (
                        "█" * filled
                        + "░" * (bar_size - filled)
                    )

                    print(f"   {bar}")

                    print()

                    if cli.session.crossfade_running:

                        progress = (
                            cli.session.crossfade.progress()
                            * 100
                        )

                        print("🎚️ Crossfade:")
                        print(
                            f"   ACTIVE "
                            f"{progress:.0f}%"
                        )

                        if cli.session.next_track:

                            print()

                            print("▶ Next:")
                            print(
                                "   "
                                f"{cli.session.next_track.title}"
                            )

                    else:

                        print("🎚️ Crossfade:")
                        print("   Inactive")

                    print()
                    print()

                    print(
                        f"📋 Queue: "
                        f"{len(state.queue)} tracks"
                    )

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
