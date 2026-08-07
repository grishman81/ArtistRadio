"""
ArtistRadio Engine
Audio Player
"""

import subprocess
from pathlib import Path


class AudioPlayer:
    """
    Реальный аудиоплеер через ffplay.
    """

    def __init__(self):
        self.current: Path | None = None
        self.process = None
        self.playing = False

    def play(self, path: Path) -> None:
        """
        Запускает воспроизведение файла.
        """

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

    def stop(self) -> None:
        """
        Останавливает воспроизведение.
        """

        if self.process:
            self.process.terminate()
            self.process = None

        self.playing = False

    def is_playing(self) -> bool:
        return self.playing