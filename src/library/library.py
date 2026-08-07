"""
ArtistRadio Engine
Library API
"""

from pathlib import Path

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

    def get_tracks(self, artist_name: str):
        """
        Возвращает все треки исполнителя.
        """

        artist = self.artists.get(artist_name)

        if not artist:
            return []

        return self.tracks.get_by_artist(
            artist["id"]
        )

    def get_artists(self):
        """
        Возвращает всех исполнителей.
        """

        return self.artists.get_all()

    def get_albums(self, artist_name: str):
        """
        Возвращает альбомы исполнителя.
        """

        artist = self.artists.get(artist_name)

        if not artist:
            return []

        return self.albums.get_by_artist(
            artist["id"]
        )

    def has_track(self, path: str) -> bool:
        return self.tracks.exists(path)

    def count_tracks(self) -> int:
        return self.tracks.count()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()