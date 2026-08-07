"""
ArtistRadio Engine
Library Models
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class Artwork:
    embedded: bool = False
    source: Optional[Path] = None
    cache: Optional[Path] = None


@dataclass(slots=True)
class Artist:
    id: int = 0
    name: str = ""
    folder: Optional[Path] = None


@dataclass(slots=True)
class Album:
    id: int = 0
    artist: str = ""
    title: str = ""
    year: Optional[int] = None
    genre: Optional[str] = None
    folder: Optional[Path] = None
    artwork: Artwork = field(default_factory=Artwork)


@dataclass(slots=True)
class Track:
    id: int = 0
    artist: str = ""
    album: str = ""
    title: str = ""
    track: int = 0
    disc: int = 1
    year: Optional[int] = None
    genre: Optional[str] = None
    duration: float = 0.0
    bitrate: int = 0
    sample_rate: int = 0
    format: str = ""
    size: int = 0
    modified: float = 0.0
    path: Optional[Path] = None
    artwork: Artwork = field(default_factory=Artwork)
