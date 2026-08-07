"""
ArtistRadio Engine
Artist Repository
"""

from ..database import LibraryDatabase


class ArtistRepository:

    def __init__(self, database: LibraryDatabase):
        self.db = database

    def get(self, name: str):
        row = self.db.connection.execute(
            "SELECT id, name, folder FROM artists WHERE name = ?",
            (name,),
        ).fetchone()
        return row

    def add(self, name: str, folder: str = "") -> int:
        cursor = self.db.connection.execute(
            "INSERT INTO artists(name, folder) VALUES(?, ?)",
            (name, folder),
        )
        return cursor.lastrowid

    def get_or_create(self, name: str, folder: str = "") -> int:
        row = self.get(name)

        if row:
            return row["id"]

        artist_id = self.add(name, folder)
        return artist_id
