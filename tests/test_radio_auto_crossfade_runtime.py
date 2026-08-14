from pathlib import Path

from src.radio.session import RadioSession


class FakePlayer:

    def __init__(self):
        self.secondary = None
        self.position = 230.0

    def current_position(self):
        return self.position

    def play_secondary(self, path):
        self.secondary = path

    def is_finished(self):
        return False

    def apply_primary_volume(self, value):
        pass

    def apply_secondary_volume(self, value):
        pass


class FakeRadio:

    def next(self):
        return type(
            "Track",
            (),
            {
                "path": Path("next.mp3"),
                "duration": 240.0,
            },
        )()


def test_check_playback_starts_crossfade_when_track_near_end():

    session = object.__new__(RadioSession)

    session.player = FakePlayer()
    session.radio = FakeRadio()

    session.state = type(
        "State",
        (),
        {
            "running": True,
            "command": None,
            "track": "current.mp3",
            "position": 230.0,
        },
    )()

    session.restoring = False
    session.crossfade = __import__(
        "src.audio.crossfade",
        fromlist=["CrossfadeEngine"],
    ).CrossfadeEngine(
        duration=10,
    )

    session.crossfade_duration = 10
    session.crossfade_running = False
    session.next_track = None

    session.storage = type(
        "Storage",
        (),
        {
            "load": lambda self: session.state,
            "save": lambda self, state: None,
        },
    )()

    session.history = type(
        "History",
        (),
        {
            "add": lambda self, track: None,
        },
    )()

    session.current_track = type(
        "Track",
        (),
        {
            "path": Path("current.mp3"),
            "duration": 240.0,
        },
    )()

    session.check_playback(
        delta=1.0,
    )

    assert session.crossfade_running is True

    assert session.next_track is not None

    assert session.player.secondary == Path("next.mp3")
