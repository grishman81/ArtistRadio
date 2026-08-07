"""
ArtistRadio Engine
Console Controller
"""

from src.radio.session import RadioSession
from src.station.manager import StationManager


class ConsoleApp:

    def __init__(
        self,
        session: RadioSession,
        stations: StationManager,
    ):
        self.session = session
        self.stations = stations

    def run(self) -> None:

        while True:

            print()
            print("====================")
            print(" ArtistRadio Console")
            print("====================")
            print("1. Next track")
            print("2. Pause")
            print("3. Resume")
            print("4. Stop")
            print("5. Current track")
            print("6. Change station")
            print("7. History")
            print("8. Exit")

            command = input("> ").strip()

            if command == "1":

                track = self.session.play_next()

                if track:
                    print(
                        f"Now playing: {track.title}"
                    )

            elif command == "2":

                self.session.player.pause()
                print("Paused")

            elif command == "3":

                self.session.player.resume()
                print("Resumed")

            elif command == "4":

                self.session.stop()
                print("Stopped")

            elif command == "5":

                track = (
                    self.session.player.current_track()
                )

                if track:
                    print(
                        f"Current: {track.title}"
                    )
                else:
                    print(
                        "Nothing playing"
                    )

            elif command == "6":

                self.change_station()

            elif command == "7":

                self.show_history()

            elif command == "8":

                self.session.stop()
                print("Bye")
                break

            else:

                print(
                    "Unknown command"
                )

    def show_history(self):

        print()
        print("Playback history:")
        print()

        history = self.session.history.items()

        if not history:

            print(
                "History is empty"
            )

            return

        for index, item in enumerate(
            history,
            start=1,
        ):

            print(
                f"{index}. {item['artist']}"
            )
            print(
                f"   {item['title']}"
            )
            print(
                f"   {item['album']}"
            )
            print()

        choice = input(
            "Select track (0 cancel): "
        ).strip()

        try:

            number = int(choice)

            if number == 0:
                return

            track = self.session.play_history_item(
                number - 1
            )

            if track:

                print(
                    f"Now playing: {track.title}"
                )

        except ValueError:

            print(
                "Invalid selection"
            )

    def change_station(self):

        stations = self.stations.all()

        if not stations:
            print(
                "No stations available"
            )
            return

        print()
        print("Available stations:")

        for index, station in enumerate(
            stations,
            start=1,
        ):
            print(
                f"{index}. {station.name}"
            )

        choice = input(
            "Select station: "
        ).strip()

        try:

            station = stations[
                int(choice) - 1
            ]

            self.session.switch_station(
                station
            )

            self.session.start()

            print(
                f"Switched to: {station.name}"
            )

        except (
            ValueError,
            IndexError,
        ):

            print(
                "Invalid station"
            )