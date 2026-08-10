from pathlib import Path

from src.radio.session import RadioSession


class FakePlayer:

    def __init__(self):
        self.secondary = None
        self.current = None


    def play_secondary(self, path):

        self.secondary = path


    def play(self, path):

        self.current = path


    def stop_secondary(self):

        self.secondary = None



class FakeHistory:

    def add(self, track):

        pass



def test_radio_can_continue_after_handoff():

    session = object.__new__(
        RadioSession
    )


    session.player = FakePlayer()

    session.history = FakeHistory()

    session.next_track = None


    session.state = type(
        "State",
        (),
        {
            "track": None,
            "position": 0.0,
        },
    )()


    track_b = type(
        "Track",
        (),
        {
            "path": Path(
                "track_b.mp3"
            )
        },
    )()


    session.crossfade = type(
        "Fade",
        (),
        {
            "start": lambda self: None,
            "is_complete": lambda self: True,
        },
    )()


    session.transition_to_next_track(
        track_b
    )


    assert (
        session.state.track
        ==
        str(track_b.path)
    )


    track_c = type(
        "Track",
        (),
        {
            "path": Path(
                "track_c.mp3"
            )
        },
    )()


    session.prepare_next_track(
        track_c
    )


    assert (
        session.player.secondary
        ==
        track_c.path
    )