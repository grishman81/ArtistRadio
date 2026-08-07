"""
ArtistRadio Engine
Console Controller
"""

from src.radio.session import RadioSession
from src.station.manager import StationManager


class ConsoleApp:
    """
    Консольный пульт управления радио.
    """

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
                        f"Current: {track.name}"
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

    def show_history(self) -> None:
        station = self.session.radio.station

        print()
        print("Playback history:")

        if not station.history:
            print(
                "History is empty"
            )
            return

        for index, track in enumerate(
            reversed(station.history),
            start=1,
        ):
            print(
                f"{index}. {track.title}"
            )

    def change_station(self) -> None:
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
            index = int(choice) - 1

            station = stations[index]

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