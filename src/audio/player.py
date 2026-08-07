"""
ArtistRadio Engine
Audio Player
"""

import subprocess
import time

from pathlib import Path


class AudioPlayer:
    """
    Audio playback controller.
    """

    def __init__(self):

        self.current: Path | None = None

        self.process = None

        self.playing = False

        self.paused = False

        self.started_at: float | None = None

        self.position: float = 0.0

        self.volume: float = 1.0



    def play(
        self,
        path: Path,
        position: float = 0.0,
    ) -> None:

        self.stop()

        self.current = path

        self.position = position


        command = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
        ]


        if position > 0:

            command.extend(
                [
                    "-ss",
                    str(position),
                ]
            )


        command.append(
            str(path)
        )


        self.process = subprocess.Popen(
            command
        )


        self.started_at = time.time()

        self.playing = True

        self.paused = False



    def stop(self) -> None:

        if self.playing:

            self.position = (
                self.current_position()
            )


        if self.process:

            self.process.terminate()

            self.process = None


        self.playing = False

        self.paused = False

        self.started_at = None



    def pause(self) -> None:

        if self.playing:

            self.position = (
                self.current_position()
            )

            self.paused = True



    def resume(self) -> None:

        if self.playing:

            self.started_at = time.time()

            self.paused = False



    def seek(
        self,
        position: float,
    ) -> None:

        self.position = position



    def current_position(self) -> float:

        if not self.playing:

            return self.position


        if self.paused:

            return self.position


        if self.started_at is None:

            return self.position


        return (
            self.position
            +
            time.time()
            -
            self.started_at
        )



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


    def fade_out(
        self,
        steps: int = 10,
    ) -> None:

        if steps <= 0:

            self.volume = 0.0

            return


        step = (
            self.volume / steps
        )


        for _ in range(steps):

            self.volume -= step


        self.volume = 0.0



    def fade_in(
        self,
        steps: int = 10,
    ) -> None:

        if steps <= 0:

            self.volume = 1.0

            return


        step = (
            (1.0 - self.volume)
            /
            steps
        )


        for _ in range(steps):

            self.volume += step


        self.volume = 1.0



    def is_finished(self) -> bool:

        if self.process is None:

            return False


        return self.process.poll() is not None



    def is_playing(self) -> bool:

        return self.playing



    def current_track(self) -> Path | None:

        return self.current