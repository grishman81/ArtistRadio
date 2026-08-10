from pathlib import Path

from src.radio.session import RadioSession


class FakePlayer:

    def __init__(self):

        self.current = None
        self.secondary = None


    def play_secondary(self, path):

        self.secondary = path


    def play(self, path):

        self.current = path


    def stop(self):

        pass


    def stop_secondary(self):

        self.secondary = None



class FakeHistory:

    def __init__(self):

        self.items = []


    def add(self, track):

        self.items.append(track)



def test_transition_finishes_on_new_track():

    session = object.__new__(
        RadioSession
    )

    session.player = FakePlayer()

    session.history = FakeHistory()

    session.state = type(
        "State",
        (),
        {
            "track": None,
            "position": 0.0,
        },
    )()


    track = type(
        "Track",
        (),
        {
            "path": Path(
                "next.mp3"
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
        track
    )


    assert (
        session.state.track
        ==
        str(track.path)
    )