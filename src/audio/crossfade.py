"""
ArtistRadio Engine
Crossfade Engine
"""


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



    def start(self):

        self.active = True

        return True



    def stop(self):

        self.active = False

        return True



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