"""
ArtistRadio Engine
Station Manager
"""

from pathlib import Path

from src.station.station import Station
from src.station.loader import StationLoader


class StationManager:
    """
    Управляет набором радиостанций.
    """

    def __init__(self, library=None, playlist=None):
        self._stations: dict[str, Station] = {}

        self.library = library
        self.playlist = playlist

    def add(self, station: Station) -> None:
        self._stations[station.name] = station

    def get(self, name: str) -> Station | None:
        return self._stations.get(name)

    def remove(self, name: str) -> None:
        self._stations.pop(name, None)

    def all(self) -> list[Station]:
        return list(self._stations.values())

    def load_from_file(self, path: Path) -> None:
        """
        Загружает станции из JSON файла.
        """

        loader = StationLoader(
            self.library,
            self.playlist,
        )

        stations = loader.load(path)

        for station in stations:
            self.add(station)

    @property
    def count(self) -> int:
        return len(self._stations)