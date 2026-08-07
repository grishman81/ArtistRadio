"""
ArtistRadio Engine
Library Database
"""

from pathlib import Path
import sqlite3

DB_NAME = "library.db"


class LibraryDatabase:
    def __init__(self, database_folder: Path):
        self.database_folder = Path(database_folder)
        self.database_folder.mkdir(parents=True, exist_ok=True)

        self.database_path = self.database_folder / DB_NAME
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

    def create(self):
        cur = self.connection.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS artists(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            folder TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS albums(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            folder TEXT,
            UNIQUE(artist_id,title)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS tracks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id INTEGER NOT NULL,
            title TEXT,
            track INTEGER,
            disc INTEGER,
            duration REAL,
            bitrate INTEGER,
            sample_rate INTEGER,
            format TEXT,
            size INTEGER,
            modified REAL,
            path TEXT UNIQUE
        )
        """)

        self.connection.commit()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
