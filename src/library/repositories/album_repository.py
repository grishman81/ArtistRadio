"""
ArtistRadio Engine
Album Repository
"""

from ..database import LibraryDatabase


class AlbumRepository:

    def __init__(self, database: LibraryDatabase):
        self.db = database

    def get(self, artist_id: int, title: str):
        row = self.db.connection.execute(
            "SELECT id, artist_id, title, year, genre, folder "
            "FROM albums WHERE artist_id=? AND title=?",
            (artist_id, title),
        ).fetchone()
        return row

    def add(
        self,
        artist_id: int,
        title: str,
        year=None,
        genre: str = "",
        folder: str = "",
    ) -> int:
        cursor = self.db.connection.execute(
            "INSERT INTO albums(artist_id,title,year,genre,folder) "
            "VALUES(?,?,?,?,?)",
            (artist_id, title, year, genre, folder),
        )
        return cursor.lastrowid

    def get_or_create(
        self,
        artist_id: int,
        title: str,
        year=None,
        genre: str = "",
        folder: str = "",
    ) -> int:
        row = self.get(artist_id, title)
        if row:
            return row["id"]
        return self.add(artist_id, title, year, genre, folder)
