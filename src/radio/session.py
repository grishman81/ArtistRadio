"""
ArtistRadio Engine
Radio Session
"""

from typing import Optional

from src.radio.engine import RadioEngine
from src.radio.state import RadioState
from src.library.models import Track


class RadioSession:
    """
    Управляет эфирной сессией.
    """

    def __init__(self, radio: RadioEngine):
        self.radio = radio

        self.state = RadioState(
            station=radio.station.name
        )

    def start(self) -> None:
        self.state.running = True
        self.radio.start()

    def stop(self) -> None:
        self.state.running = False
        self.radio.stop()

    def play_next(self) -> Optional[Track]:
        if not self.state.running:
            return None

        track = self.radio.next()

        if track:
            self.state.track = str(track.path)

        return track