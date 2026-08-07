"""
ArtistRadio Engine
Station Generator
"""

from src.station.station import Station

from src.library.library import Library
from src.playlist.engine import PlaylistEngine


class StationGenerator:

    def __init__(
        self,
        library: Library,
        playlist: PlaylistEngine,
    ):
        self.library = library
        self.playlist = playlist

    def generate(self) -> list[Station]:

        stations = []

        for artist in self.library.get_artists():

            name = artist["name"]

            stations.append(
                Station(
                    name=f"{name} Radio",
                    artist=name,
                    library=self.library,
                    playlist=self.playlist,
                )
            )

        return stations