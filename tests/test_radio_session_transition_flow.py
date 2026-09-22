"""Radio session transition integration tests."""

from types import SimpleNamespace
from pathlib import Path

from src.audio.crossfade import CrossfadeEngine
from src.radio.session import RadioSession


class FakePlayer:
    def __init__(self):
        self.current = None
        self.secondary = None
        self.primary_volume = 1.0
        self.secondary_volume = 0.0
        self.handoff_count = 0

    def play(self, path, position=0.0):
        self.current = path
        self.secondary = None

    def play_secondary(self, path):
        self.secondary = path

    def apply_primary_volume(self, value):
        self.primary_volume = value

    def apply_secondary_volume(self, value):
        self.secondary_volume = value

    def handoff_secondary(self):
        assert self.secondary is not None
        self.current = self.secondary
        self.secondary = None
        self.primary_volume = 1.0
        self.secondary_volume = 0.0
        self.handoff_count += 1

    def stop_secondary(self):
        self.secondary = None


class FakeHistory:
    def __init__(self):
        self.items = []

    def add(self, track):
        self.items.append(track)


def make_session():
    session = object.__new__(RadioSession)
    session.player = FakePlayer()
    session.crossfade = CrossfadeEngine(duration=5)
    session.crossfade_running = False
    session.next_track = None
    session.current_track = SimpleNamespace(path=Path("current.mp3"))
    session.history = FakeHistory()
    session.state = SimpleNamespace(
        track="current.mp3",
        position=12.0,
        crossfade_running=False,
        crossfade_progress=0.0,
        next_track=None,
    )
    session.save = lambda: None
    session.save_queue = lambda: None
    return session


def test_transition_starts_secondary_and_crossfade():
    session = make_session()
    next_track = SimpleNamespace(path=Path("next.mp3"))

    result = session.transition_to_next_track(next_track)

    assert result is next_track
    assert session.next_track is next_track
    assert session.crossfade_running is True
    assert session.player.current == Path("current.mp3")
    assert session.player.secondary == Path("next.mp3")
    assert session.player.primary_volume == 1.0
    assert session.player.secondary_volume == 0.0
    assert session.state.crossfade_running is True
    assert session.state.next_track == "next.mp3"


def test_check_playback_completes_handoff_after_crossfade():
    session = make_session()
    next_track = SimpleNamespace(path=Path("next.mp3"))

    session.transition_to_next_track(next_track)

    levels = session.check_playback(delta=2.5)

    assert levels["old"] == 0.5
    assert levels["new"] == 0.5
    assert session.crossfade_running is True
    assert session.player.current == Path("current.mp3")

    session.check_playback(delta=2.5)

    assert session.crossfade_running is False
    assert session.next_track is None
    assert session.current_track is next_track
    assert session.player.current == Path("next.mp3")
    assert session.player.secondary is None
    assert session.player.handoff_count == 1
    assert session.player.primary_volume == 1.0
    assert session.player.secondary_volume == 0.0
    assert session.state.track == "next.mp3"
    assert session.state.position == 0.0
    assert session.state.crossfade_running is False
    assert session.state.crossfade_progress == 0.0
    assert session.state.next_track is None
    assert session.history.items == [next_track]
