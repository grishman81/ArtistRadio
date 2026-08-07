"""
ArtistRadio Engine
Station Manager
"""

from .station import Station


class StationManager:
    """
    Управляет набором радиостанций.
    """

    def __init__(self):
        self._stations: dict[str, Station] = {}

    def add(self, station: Station) -> None:
        self._stations[station.name] = station

    def get(self, name: str) -> Station | None:
        return self._stations.get(name)

    def remove(self, name: str) -> None:
        self._stations.pop(name, None)

    def all(self) -> list[Station]:
        return list(self._stations.values())

    @property
    def count(self) -> int:
        return len(self._stations)