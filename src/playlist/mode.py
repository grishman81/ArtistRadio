"""
ArtistRadio Engine
Playlist Modes
"""

from enum import Enum


class PlaylistMode(Enum):

    RANDOM = "random"

    SEQUENTIAL = "sequential"

    ALBUM = "album"