"""
ArtistRadio Engine
Crossfade Engine
"""


class CrossfadeEngine:
    """
    Controls transition between tracks.
    """

    def __init__(
        self,
        duration: int = 5,
    ):

        self.duration = duration


    def start(self):

        return True


    def fade_out_old(
        self,
        player,
    ):

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