"""
ArtistRadio Engine
Library Manager
"""

from pathlib import Path

from .database import LibraryDatabase
from .scanner import LibraryScanner
from .repositories.artist_repository import ArtistRepository
from .repositories.album_repository import AlbumRepository
from .repositories.track_repository import TrackRepository


class LibraryManager:

    def __init__(self, music_root: Path, database_folder: Path):
        self.db = LibraryDatabase(database_folder)

        self.artists = ArtistRepository(self.db)
        self.albums = AlbumRepository(self.db)
        self.tracks = TrackRepository(self.db)

        self.scanner = LibraryScanner(music_root)

    def build(self):
        self.db.create()

        count = 0

        for track in self.scanner.scan():

            artist_id = self.artists.get_or_create(track.artist)

            album_id = self.albums.get_or_create(
                artist_id=artist_id,
                title=track.album,
                year=track.year,
                genre=track.genre,
            )

            if not self.tracks.exists(str(track.path)):
                self.tracks.add(album_id, track)

            count += 1

            if count % 10 == 0:
                print(f"Indexed: {count}")

        self.db.commit()
        print(f"Done. Indexed {count} tracks.")

    def close(self):
        self.db.close()
