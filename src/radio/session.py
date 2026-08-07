"""
ArtistRadio Engine
Radio Session
"""

from typing import Optional

from src.radio.engine import RadioEngine
from src.library.models import Track


class RadioSession:
    """
    Управляет эфирной сессией.
    """

    def __init__(self, radio: RadioEngine):
        self.radio = radio
        self.running = False

    def start(self) -> None:
        """
        Запускает эфир.
        """

        self.running = True
        self.radio.start()

    def stop(self) -> None:
        """
        Останавливает эфир.
        """

        self.running = False
        self.radio.stop()

    def play_next(self) -> Optional[Track]:
        """
        Получает следующий трек.
        """

        if not self.running:
            return None

        return self.radio.next()