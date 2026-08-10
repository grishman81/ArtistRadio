"""
ArtistRadio Engine
Automatic Transition Tests
"""


from pathlib import Path

from src.radio.session import RadioSession



class FakePlayer:


    def __init__(self):

        self.secondary = None


    def play_secondary(
        self,
        path,
    ):

        self.secondary = path



class FakeRadio:


    def next(self):

        return type(
            "Track",
            (),
            {
                "path": Path(
                    "next_track.mp3"
                )
            },
        )()



def test_auto_transition_prepares_next_track():


    session = object.__new__(
        RadioSession
    )


    session.player = FakePlayer()

    session.radio = FakeRadio()

    session.next_track = None


    session.prepare_next_track(
        session.radio.next()
    )


    assert (
        session.player.secondary
        ==
        Path(
            "next_track.mp3"
        )
    )