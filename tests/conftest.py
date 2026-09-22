from pathlib import Path

import pytest

from src.library.database import LibraryDatabase


DATABASE = Path("database")


@pytest.fixture(scope="session", autouse=True)
def ensure_test_library():
    database = LibraryDatabase(DATABASE)
    database.create()

    required_artists = [
        "Jennifer Lopez",
        "Madonna",
        "Michael Jackson",
    ]

    existing = {
        row["name"]
        for row in database.connection.execute(
            "SELECT name FROM artists"
        ).fetchall()
    }

    for artist_name in required_artists:
        if artist_name not in existing:
            artist_id = database.connection.execute(
                "INSERT INTO artists(name, folder) VALUES(?, ?)",
                (artist_name, "tests"),
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
                f"{artist_name} Test Album",
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
                    f"tests/{artist_name.lower().replace(' ', '_')}_track_{number}.mp3",
                ),
            )

        database.connection.commit()

    database.close()

    yield
