"""
ArtistRadio Engine
Track Repository
"""

from ..database import LibraryDatabase
from ..models import Track


class TrackRepository:

    def __init__(self, database: LibraryDatabase):
        self.db = database

    def get(self, path: str):
        row = self.db.connection.execute(
            "SELECT id FROM tracks WHERE path=?",
            (path,),
        ).fetchone()
        return row

    def add(self, album_id: int, track: Track) -> int:
        cursor = self.db.connection.execute(
            """
            INSERT INTO tracks(
                album_id,
                title,
                track,
                disc,
                duration,
                bitrate,
                sample_rate,
                format,
                size,
                modified,
                path
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                album_id,
                track.title,
                track.track,
                track.disc,
                track.duration,
                track.bitrate,
                track.sample_rate,
                track.format,
                track.size,
                track.modified,
                str(track.path),
            ),
        )
        return cursor.lastrowid

    def exists(self, path: str) -> bool:
        return self.get(path) is not None
