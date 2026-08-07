"""
ArtistRadio Engine
Audio Player
"""

from pathlib import Path


class AudioPlayer:
    """
    Проигрыватель аудио файлов.
    """

    def __init__(self):
        self.current: Path | None = None
        self.playing = False

    def play(self, path: Path) -> None:
        """
        Запускает воспроизведение.
        """

        self.current = path
        self.playing = True

        print(
            f"Playing: {path.name}"
        )

    def stop(self) -> None:
        """
        Останавливает воспроизведение.
        """

        self.playing = False

    def is_playing(self) -> bool:
        return self.playing