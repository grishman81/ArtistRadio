"""
ArtistRadio Engine
Console Controller
"""

from src.radio.session import RadioSession


class ConsoleApp:
    """
    Консольный пульт управления радио.
    """

    def __init__(self, session: RadioSession):
        self.session = session

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
            print("6. Exit")

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
                self.session.stop()
                print("Bye")
                break

            else:
                print("Unknown command")