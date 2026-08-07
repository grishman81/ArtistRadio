"""
ArtistRadio Engine
Radio Engine
"""

from src.station.station import Station


class RadioEngine:
    """
    Управляет эфиром станции.
    """

    def __init__(self, station: Station):
        self.station = station
        self.running = False

    def start(self):
        """
        Запускает эфир.
        """

        self.running = True

    def stop(self):
        """
        Останавливает эфир.
        """

        self.running = False

    def next(self):
        """
        Получает следующий трек.
        """

        if not self.running:
            return None

        return self.station.next_track()