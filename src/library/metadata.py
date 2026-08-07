"""
ArtistRadio Engine
Metadata Reader
"""

from pathlib import Path

from mutagen import File

from .models import Track


class MetadataReader:

    def read(
        self,
        filename: Path,
    ) -> Track:

        audio = File(filename)

        if audio is None:
            raise ValueError(
                f"Unsupported file: {filename}"
            )

        track = Track()

        track.path = filename
        track.format = (
            filename.suffix.lower()
            .lstrip(".")
        )

        stat = filename.stat()

        track.size = stat.st_size
        track.modified = stat.st_mtime

        tags = audio.tags or {}

        def get_tag(*names):

            for name in names:

                if name in tags:

                    value = tags[name]

                    if isinstance(value, list):
                        return str(value[0])

                    return str(value)

            return ""

        #
        # Artist from folder structure
        #
        # D:\TestLibrary\Artist\Album\Track.mp3
        # D:\TestLibrary\Artist\Track.mp3
        #

        parts = filename.parts

        try:
            root_index = parts.index("TestLibrary")
            track.artist = parts[root_index + 1]

        except ValueError:

            track.artist = get_tag(
                "TPE1",
                "ARTIST",
                "\xa9ART",
            )


        #
        # Album
        #

        track.album = get_tag(
            "TALB",
            "ALBUM",
            "\xa9alb",
        )

        if not track.album:

            if len(filename.parts) >= 2:
                track.album = filename.parent.name


        #
        # Title
        #

        track.title = (
            get_tag(
                "TIT2",
                "TITLE",
                "\xa9nam",
            )
            or filename.stem
        )


        #
        # Genre
        #

        track.genre = get_tag(
            "TCON",
            "GENRE",
            "\xa9gen",
        )


        #
        # Year
        #

        year = get_tag(
            "TDRC",
            "DATE",
            "\xa9day",
        )

        if year:

            try:
                track.year = int(
                    year[:4]
                )

            except ValueError:
                track.year = None


        #
        # Audio info
        #

        if hasattr(audio, "info"):

            info = audio.info

            track.duration = round(
                getattr(
                    info,
                    "length",
                    0.0,
                ),
                2,
            )

            track.bitrate = int(
                getattr(
                    info,
                    "bitrate",
                    0,
                )
                / 1000
            )

            track.sample_rate = getattr(
                info,
                "sample_rate",
                0,
            )


        return track