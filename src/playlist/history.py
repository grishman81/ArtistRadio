"""
ArtistRadio Engine
Playlist History
"""

from collections import deque
from pathlib import Path

class PlaylistHistory:
    """Хранит историю недавно воспроизведённых треков."""

    def __init__(self, limit:int=100):
        self._items=deque(maxlen=limit)

    def add(self, track_path: Path)->None:
        self._items.append(str(track_path))

    def contains(self, track_path: Path)->bool:
        return str(track_path) in self._items

    def clear(self)->None:
        self._items.clear()

    @property
    def size(self)->int:
        return len(self._items)
