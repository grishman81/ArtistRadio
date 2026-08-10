"""
ArtistRadio Engine
Automatic Transition Runtime Tests
"""

from pathlib import Path

from src.radio.session import RadioSession



class FakePlayer:

    def __init__(self):

        self.secondary = None
        self.position = 230


    def current_position(self):

        return self.position


    def play_secondary(self, path):

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



def test_runtime_check_prepares_transition():

    session = object.__new__(
        RadioSession
    )


    session.player = FakePlayer()

    session.radio = FakeRadio()

    session.next_track = None


    session.crossfade_duration = 10


    result = session.check_transition(
        position=230,
        duration=240,
    )


    assert result is not None

    assert (
        session.player.secondary
        ==
        Path(
            "next_track.mp3"
        )
    )