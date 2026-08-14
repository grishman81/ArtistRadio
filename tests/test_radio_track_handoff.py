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

def test_transition_crossfade_completes_and_hands_off():

    session = object.__new__(
        RadioSession
    )

    session.player = FakePlayer()

    session.player.primary_volume = None
    session.player.secondary_volume = None

    session.player.apply_primary_volume = (
        lambda value:
        setattr(
            session.player,
            "primary_volume",
            value,
        )
    )

    session.player.apply_secondary_volume = (
        lambda value:
        setattr(
            session.player,
            "secondary_volume",
            value,
        )
    )

    session.history = FakeHistory()

    session.state = type(
        "State",
        (),
        {
            "track": None,
            "position": 0.0,
            "command": None,
            "running": True,
        },
    )()

    session.crossfade_running = False
    session.next_track = None
    session.restoring = False

    class FakeStorage:

        def load(self):
            return session.state

    session.storage = FakeStorage()

    from src.audio.crossfade import CrossfadeEngine

    session.crossfade = CrossfadeEngine(
        duration=2
    )

    track = type(
        "Track",
        (),
        {
            "path": Path(
                "next.mp3"
            )
        },
    )()

    session.transition_to_next_track(
        track
    )

    assert session.crossfade_running is True

    session.check_playback(
        delta=1
    )

    assert session.crossfade_running is True
    assert session.player.primary_volume == 0.5
    assert session.player.secondary_volume == 0.5

    session.check_playback(
        delta=1
    )

    assert session.crossfade_running is False
    assert session.player.secondary is None