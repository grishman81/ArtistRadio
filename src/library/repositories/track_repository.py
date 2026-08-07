"""
ArtistRadio Engine
Track Repository
"""

from pathlib import Path

from ..database import LibraryDatabase
from ..models import Track


class TrackRepository:

    def __init__(self, database: LibraryDatabase):
        self.db = database

    def _row_to_track(self, row) -> Track:
        return Track(
            id=row["id"],
            title=row["title"],
            track=row["track"],
            disc=row["disc"],
            duration=row["duration"],
            bitrate=row["bitrate"],
            sample_rate=row["sample_rate"],
            format=row["format"],
            size=row["size"],
            modified=row["modified"],
            path=Path(row["path"]),
        )

    def get_by_path(self, path: str):
        row = self.db.connection.execute(
            """
            SELECT *
            FROM tracks
            WHERE path=?
            """,
            (path,),
        ).fetchone()

        if row is None:
            return None

        return self._row_to_track(row)

    def get_by_id(self, track_id: int):
        row = self.db.connection.execute(
            """
            SELECT *
            FROM tracks
            WHERE id=?
            """,
            (track_id,),
        ).fetchone()

        if row is None:
            return None

        return self._row_to_track(row)

    def get_by_album(self, album_id: int):
        rows = self.db.connection.execute(
            """
            SELECT *
            FROM tracks
            WHERE album_id=?
            ORDER BY disc, track
            """,
            (album_id,),
        ).fetchall()

        return [
            self._row_to_track(row)
            for row in rows
        ]

    def get_by_artist(self, artist_id: int):
        rows = self.db.connection.execute(
            """
            SELECT tracks.*
            FROM tracks
            JOIN albums
                ON tracks.album_id = albums.id
            WHERE albums.artist_id=?
            ORDER BY albums.id, tracks.disc, tracks.track
            """,
            (artist_id,),
        ).fetchall()

        return [
            self._row_to_track(row)
            for row in rows
        ]

    def get_all(self):
        rows = self.db.connection.execute(
            """
            SELECT *
            FROM tracks
            ORDER BY id
            """
        ).fetchall()

        return [
            self._row_to_track(row)
            for row in rows
        ]

    def count(self) -> int:
        row = self.db.connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM tracks
            """
        ).fetchone()

        return row["count"]

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
        return self.get_by_path(path) is not None