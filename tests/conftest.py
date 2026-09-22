from pathlib import Path

import pytest

from src.library.database import LibraryDatabase


DATABASE = Path("database")


@pytest.fixture(scope="session", autouse=True)
def ensure_test_library():
    database = LibraryDatabase(DATABASE)
    database.create()

    artist = database.connection.execute(
        "SELECT id FROM artists WHERE name = ?",
        ("Jennifer Lopez",),
    ).fetchone()

    if artist is None:
        artist_id = database.connection.execute(
            "INSERT INTO artists(name, folder) VALUES(?, ?)",
            ("Jennifer Lopez", "tests"),
        ).lastrowid

        album_id = database.connection.execute(
            """
            INSERT INTO albums(
                artist_id, title, year, genre, folder
            )
            VALUES(?, ?, ?, ?, ?)
            """,
            (
                artist_id,
                "Test Album",
                2026,
                "Pop",
                "tests",
            ),
        ).lastrowid

        for number in range(1, 6):
            database.connection.execute(
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
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    album_id,
                    f"Test Track {number}",
                    number,
                    1,
                    240.0,
                    192,
                    44100,
                    "mp3",
                    1000000,
                    0.0,
                    f"tests/track_{number}.mp3",
                ),
            )

        database.connection.commit()

    database.close()

    yield
