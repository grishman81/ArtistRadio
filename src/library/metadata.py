"""
ArtistRadio Engine
Metadata Reader
"""

from pathlib import Path
from mutagen import File

from .models import Track


class MetadataReader:

    def read(self, filename: Path) -> Track:
        audio = File(filename)

        if audio is None:
            raise ValueError(f"Unsupported file: {filename}")

        track = Track()
        track.path = filename
        track.format = filename.suffix.lower().lstrip(".")
        track.size = filename.stat().st_size
        track.modified = filename.stat().st_mtime

        tags = audio.tags or {}

        def get_tag(*names):
            for name in names:
                if name in tags:
                    value = tags[name]
                    if isinstance(value, list):
                        return str(value[0])
                    return str(value)
            return ""

        track.artist = get_tag("TPE1", "ARTIST", "\xa9ART")
        track.album = get_tag("TALB", "ALBUM", "\xa9alb")
        track.title = get_tag("TIT2", "TITLE", "\xa9nam") or filename.stem
        track.genre = get_tag("TCON", "GENRE", "\xa9gen")
        track.year = get_tag("TDRC", "DATE", "\xa9day") or None

        if hasattr(audio, "info"):
            info = audio.info
            track.duration = round(getattr(info, "length", 0.0), 2)
            track.bitrate = int(getattr(info, "bitrate", 0) / 1000)
            track.sample_rate = getattr(info, "sample_rate", 0)

        return track
