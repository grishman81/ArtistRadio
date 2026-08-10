from pathlib import Path

from src.radio.session import RadioSession


class FakePlayer:

    def __init__(self):

        self.secondary = None
        self.duration = 240
        self.position = 230


    def current_position(self):

        return self.position


    def play_secondary(self, path):

        self.secondary = path


    def is_finished(self):

        return False



class FakeRadio:

    def next(self):

        return type(
            "Track",
            (),
            {
                "path": Path(
                    "next.mp3"
                )
            },
        )()



def test_live_runtime_prepares_next_track():

    session = object.__new__(
        RadioSession
    )

    session.player = FakePlayer()
    session.radio = FakeRadio()

    session.next_track = None

    session.crossfade_duration = 10


    session.check_transition(
        position=230,
        duration=240,
    )


    assert (
        session.player.secondary
        ==
        Path(
            "next.mp3"
        )
    )