"""
ArtistRadio Engine
Audio Player
"""

import subprocess
from pathlib import Path


class AudioPlayer:
    """
    Управление воспроизведением через ffplay.
    """

    def __init__(self):
        self.current: Path | None = None
        self.process = None
        self.playing = False
        self.paused = False

    def play(self, path: Path) -> None:
        self.stop()

        self.current = path

        self.process = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                str(path),
            ]
        )

        self.playing = True
        self.paused = False

    def stop(self) -> None:
        if self.process:
            self.process.terminate()
            self.process = None

        self.playing = False
        self.paused = False

    def pause(self) -> None:
        if self.playing:
            self.paused = True

    def resume(self) -> None:
        if self.playing:
            self.paused = False

    def is_playing(self) -> bool:
        return self.playing

    def current_track(self) -> Path | None:
        return self.current