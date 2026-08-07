"""
ArtistRadio Engine
Library API
"""

from pathlib import Path
from typing import Optional

from .database import LibraryDatabase
from .repositories.artist_repository import ArtistRepository
from .repositories.album_repository import AlbumRepository
from .repositories.track_repository import TrackRepository


class Library:
    """
    Главная точка входа для работы с музыкальной библиотекой.
    """

    def __init__(self, database_folder: Path):
        self.db = LibraryDatabase(database_folder)
        self.db.create()

        self.artists = ArtistRepository(self.db)
        self.albums = AlbumRepository(self.db)
        self.tracks = TrackRepository(self.db)

    def get_artist(self, name: str):
        return self.artists.get(name)

    def get_album(self, artist_id: int, title: str):
        return self.albums.get(artist_id, title)

    def has_track(self, path: str) -> bool:
        return self.tracks.exists(path)

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
