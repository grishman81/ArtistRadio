from pathlib import Path

from src.radio.session import RadioSession


class FakeRadio:

    def next(self):

        return type(
            "Track",
            (),
            {
                "path": Path(
                    "auto_next.mp3"
                )
            },
        )()



class FakePlayer:

    def __init__(self):

        self.secondary = None


    def play_secondary(self, path):

        self.secondary = path



def test_session_auto_selects_next_track():

    session = object.__new__(
        RadioSession
    )

    session.radio = FakeRadio()

    session.player = FakePlayer()

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
            "auto_next.mp3"
        )
    )