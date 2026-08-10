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

        self.secondary: Path | None = None


        self.process = None

        self.secondary_process = None


        self.playing = False

        self.paused = False


        # общий уровень (старый API)
        self.volume = 1.0


        # уровни для crossfade
        self.primary_volume = 1.0

        self.secondary_volume = 0.0


        self.position = 0.0



    def play(
        self,
        path: Path,
        position: float = 0.0,
    ) -> None:


        self.stop()


        self.current = path

        self.position = position


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



    def play_secondary(
        self,
        path: Path,
    ) -> None:


        self.secondary = path


        self.secondary_process = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                str(path),
            ]
        )



    def stop_secondary(self) -> None:


        if self.secondary_process:

            self.secondary_process.terminate()

            self.secondary_process = None


        self.secondary = None

        self.secondary_volume = 0.0



    def stop(self) -> None:


        if self.process:

            self.process.terminate()

            self.process = None


        self.stop_secondary()


        self.playing = False

        self.paused = False


        self.primary_volume = 1.0



    def pause(self) -> None:


        if self.playing:

            self.paused = True



    def resume(self) -> None:


        if self.playing:

            self.paused = False



    def seek(
        self,
        position: float,
    ) -> None:

        self.position = position



    def current_position(self) -> float:

        return self.position



    def set_volume(
        self,
        volume: float,
    ) -> None:


        self.volume = max(
            0.0,
            min(
                1.0,
                volume,
            )
        )



    def apply_volume(
        self,
        volume: float,
    ) -> None:


        self.set_volume(
            volume
        )



    def apply_primary_volume(
        self,
        volume: float,
    ) -> None:


        self.primary_volume = max(
            0.0,
            min(
                1.0,
                volume,
            )
        )



    def apply_secondary_volume(
        self,
        volume: float,
    ) -> None:


        self.secondary_volume = max(
            0.0,
            min(
                1.0,
                volume,
            )
        )



    def fade_out(
        self,
        steps: int = 10,
    ) -> None:


        step = (
            self.volume
            /
            max(
                steps,
                1,
            )
        )


        for _ in range(steps):

            self.volume = max(
                0.0,
                self.volume - step,
            )


        self.volume = 0.0



    def fade_in(
        self,
        steps: int = 10,
    ) -> None:


        step = (
            1.0
            /
            max(
                steps,
                1,
            )
        )


        for _ in range(steps):

            self.volume = min(
                1.0,
                self.volume + step,
            )



    def is_finished(self) -> bool:


        if not self.process:

            return False


        return (
            self.process.poll()
            is not None
        )



    def is_playing(self) -> bool:

        return self.playing



    def current_track(self) -> Path | None:

        return self.current