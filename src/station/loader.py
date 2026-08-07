"""
ArtistRadio Engine
Station Loader
"""

import json
from pathlib import Path

from .station import Station


class StationLoader:
    """
    Загружает станции из JSON-конфигурации.
    """

    def __init__(self, library, playlist):
        self.library = library
        self.playlist = playlist

    def load(self, path: Path) -> list[Station]:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        stations = []

        for item in data:
            station = Station(
                name=item["name"],
                artist=item["artist"],
                bitrate=item.get("bitrate", 320),
                library=self.library,
                playlist=self.playlist,
            )

            stations.append(station)

        return stations