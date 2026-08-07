"""
ArtistRadio Engine
Main
"""

from config import MUSIC_ROOT, DATABASE_FOLDER
from library.manager import LibraryManager


def main():
    manager = LibraryManager(
        music_root=MUSIC_ROOT,
        database_folder=DATABASE_FOLDER,
    )

    try:
        manager.build()
    finally:
        manager.close()


if __name__ == "__main__":
    main()