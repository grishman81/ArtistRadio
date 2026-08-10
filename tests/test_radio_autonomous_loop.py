from pathlib import Path

from src.radio.session import RadioSession


class FakeRadio:

    def __init__(self):

        self.index = 0

        self.tracks = [
            Path("track_b.mp3"),
            Path("track_c.mp3"),
        ]


    def next(self):

        track = type(
            "Track",
            (),
            {
                "path": self.tracks[self.index]
            },
        )()

        self.index += 1

        return track



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



def test_autonomous_radio_loop():

    session = object.__new__(
        RadioSession
    )


    session.radio = FakeRadio()

    session.player = FakePlayer()

    session.history = FakeHistory()

    session.next_track = None

    session.crossfade_duration = 10


    first = session.check_transition(
        230,
        240,
    )


    assert first.path == Path(
        "track_b.mp3"
    )


    session.transition_to_next_track(
        first
    )


    second = session.check_transition(
        230,
        240,
    )


    assert second.path == Path(
        "track_c.mp3"
    )