"""
ArtistRadio Engine
Crossfade Engine
"""


class CrossfadeEngine:


    def __init__(
        self,
        duration: float = 5,
    ):

        self.duration = float(
            duration
        )

        # старое API
        self.elapsed_time = 0.0

        self.active = False


        # внутренние значения
        self.elapsed = 0.0

        self.running = False



    def start(self):

        self.elapsed_time = 0.0

        self.elapsed = 0.0


        self.active = True

        self.running = True



    def stop(self):

        self.active = False

        self.running = False


        self.elapsed_time = 0.0

        self.elapsed = 0.0



    def tick(
        self,
        seconds: float,
    ):


        if not self.active:

            return self.elapsed_time


        self.elapsed_time += seconds


        if self.elapsed_time > self.duration:

            self.elapsed_time = self.duration


        self.elapsed = self.elapsed_time


        return self.elapsed_time



    def progress(self) -> float:


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



    def update(
        self,
        elapsed: float | None = None,
    ):


        if elapsed is not None:

            self.elapsed_time = elapsed

            self.elapsed = elapsed


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



    def is_complete(self):

        return (
            self.elapsed_time
            >=
            self.duration
        )



    def trigger_time(
        self,
        track_length: float,
    ) -> float:


        return max(
            0.0,
            track_length - self.duration,
        )



    def fade_out_old(
        self,
        player,
    ):

        player.apply_primary_volume(
            0.0
        )



    def fade_in_new(
        self,
        player,
    ):

        player.apply_secondary_volume(
            1.0
        )