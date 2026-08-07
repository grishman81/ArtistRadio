"""
ArtistRadio Engine
Artist Repository
"""

from ..database import LibraryDatabase


class ArtistRepository:

    def __init__(
        self,
        database: LibraryDatabase
    ):
        self.db = database

    def get(
        self,
        name: str
    ):
        row = self.db.connection.execute(
            """
            SELECT id, name, folder
            FROM artists
            WHERE name = ?
            """,
            (name,),
        ).fetchone()

        return row

    def get_all(self):
        rows = self.db.connection.execute(
            """
            SELECT id, name, folder
            FROM artists
            ORDER BY name
            """
        ).fetchall()

        return rows

    def add(
        self,
        name: str,
        folder: str = ""
    ) -> int:

        cursor = self.db.connection.execute(
            """
            INSERT INTO artists(name, folder)
            VALUES(?, ?)
            """,
            (name, folder),
        )

        return cursor.lastrowid

    def get_or_create(
        self,
        name: str,
        folder: str = ""
    ) -> int:

        row = self.get(name)

        if row:
            return row["id"]

        return self.add(
            name,
            folder
        )