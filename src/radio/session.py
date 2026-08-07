"""
ArtistRadio Engine
Radio Session
"""

from typing import Optional

from src.radio.engine import RadioEngine
from src.radio.state import RadioState
from src.radio.storage import RadioStorage

from src.audio.player import AudioPlayer

from src.station.station import Station

from src.library.models import Track


class RadioSession:
    """
    Управляет эфирной сессией.
    """

    def __init__(
        self,
        radio: RadioEngine,
        storage: RadioStorage,
        player: AudioPlayer,
    ):
        self.radio = radio
        self.storage = storage
        self.player = player

        self.state = RadioState(
            station=radio.station.name
        )

        self.save()

    def save(self):
        self.storage.save(
            self.state
        )

    def start(self):
        self.state.running = True

        self.radio.start()

        self.save()

    def stop(self):
        self.state.running = False

        self.player.stop()

        self.radio.stop()

        self.save()

    def play_next(self) -> Optional[Track]:
        if not self.state.running:
            return None

        track = self.radio.next()

        if track:
            self.state.track = str(track.path)

            self.player.play(
                track.path
            )

            self.save()

        return track

    def switch_station(
        self,
        station: Station
    ):
        """
        Переключает эфир на другую станцию.
        """

        self.player.stop()

        self.radio = RadioEngine(
            station
        )

        self.state.station = (
            station.name
        )

        self.state.track = None

        self.save()