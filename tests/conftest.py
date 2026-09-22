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

    for artist_name in required_artists:
        row = database.connection.execute(
            "SELECT id FROM artists WHERE name = ?",
            (artist_name,),
        ).fetchone()

        if row is None:
            artist_id = database.connection.execute(
                "INSERT INTO artists(name, folder) VALUES(?, ?)",
                (artist_name, "tests"),
            ).lastrowid
        else:
            artist_id = row["id"]

        album = database.connection.execute(
            "SELECT id FROM albums WHERE artist_id = ? LIMIT 1",
            (artist_id,),
        ).fetchone()

        if album is None:
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
        else:
            album_id = album["id"]

        count = database.connection.execute(
            "SELECT COUNT(*) AS count FROM tracks WHERE album_id = ?",
            (album_id,),
        ).fetchone()["count"]

        for number in range(count + 1, 6):
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


@pytest.fixture(autouse=True)
def clean_test_state():
    for path in (
        Path("test_radio_state.json"),
        Path("test_radio_history.json"),
    ):
        if path.exists():
            path.unlink()

    yield
