"""
ArtistRadio Engine
Crossfade Engine
"""

import time


class CrossfadeEngine:
    """
    Controls track transitions.
    """

    def __init__(
        self,
        duration: int = 5,
    ):

        self.duration = duration

        self.active = False

        self.start_time = None

        self.elapsed_time = 0



    def start(self):

        self.active = True

        self.start_time = time.time()

        self.elapsed_time = 0

        return True



    def stop(self):

        self.active = False

        self.start_time = None

        self.elapsed_time = 0

        return True



    def elapsed(self):

        if not self.active:

            return self.elapsed_time


        if self.elapsed_time >= self.duration:

            return self.elapsed_time


        if self.start_time is None:

            return 0


        return (
            time.time()
            -
            self.start_time
        )



    def progress(self):

        if not self.active:

            return 0.0


        value = (
            self.elapsed()
            /
            self.duration
        )


        return max(
            0.0,
            min(
                1.0,
                value,
            )
        )



    def is_complete(self):

        return (
            self.progress()
            >=
            1.0
        )



    def fade_out_old(
        self,
        player,
    ):

        self.start()

        player.fade_out(
            steps=self.duration
        )



    def fade_in_new(
        self,
        player,
    ):

        player.fade_in(
            steps=self.duration
        )

        self.stop()