"""
ArtistRadio Engine
Crossfade Engine
"""


class CrossfadeEngine:


    def __init__(
        self,
        duration: float = 5.0,
    ):

        self.duration = duration

        self.elapsed_time = 0.0

        self.active = False



    def start(self):

        self.active = True

        self.elapsed_time = 0.0



    def stop(self):

        self.active = False

        self.elapsed_time = 0.0



    def tick(
        self,
        seconds: float,
    ):

        if not self.active:

            return 0.0


        self.elapsed_time += seconds


        if self.elapsed_time >= self.duration:

            self.elapsed_time = self.duration


        return self.progress()



    def progress(self):

        if self.duration <= 0:

            return 1.0


        value = (
            self.elapsed_time
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
            self.active
            and
            self.elapsed_time >= self.duration
        )



    def update(
        self,
        elapsed: float = None,
    ):

        if elapsed is not None:

            self.elapsed_time = elapsed


        value = self.progress()


        return {
            "old": round(
                1.0 - value,
                10,
            ),

            "new": round(
                value,
                10,
            ),
        }



    def fade_out_old(
        self,
        player,
    ):

        player.fade_out()



    def fade_in_new(
        self,
        player,
    ):

        player.fade_in()