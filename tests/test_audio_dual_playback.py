from pathlib import Path

from src.audio.player import AudioPlayer


class FakeProcess:
    _next_pid = 1000

    def __init__(self):
        self.pid = FakeProcess._next_pid
        FakeProcess._next_pid += 1
        self.terminated = False
        self.returncode = None

    def terminate(self):
        self.terminated = True
        self.returncode = 0

    def wait(self, timeout=None):
        return 0

    def poll(self):
        return self.returncode


def test_player_can_hold_secondary_track():
    player = AudioPlayer()
    path = Path("next_song.mp3")
    player.secondary = path
    assert player.secondary == path


def test_player_secondary_starts_empty():
    player = AudioPlayer()
    assert player.secondary is None


def test_handoff_secondary_becomes_primary(monkeypatch):
    monkeypatch.setattr(
        "subprocess.Popen",
        lambda *args, **kwargs: FakeProcess(),
    )

    player = AudioPlayer()
    primary = Path("current.mp3")
    secondary = Path("next.mp3")

    player.play(primary)
    player.play_secondary(secondary)

    old_primary_process = player.process
    secondary_process = player.secondary_process

    player.handoff_secondary()

    assert player.current == secondary
    assert player.process is secondary_process
    assert player.process is not old_primary_process
    assert player.secondary is None
    assert player.secondary_process is None


def test_handoff_secondary_preserves_playing_state(monkeypatch):
    monkeypatch.setattr(
        "subprocess.Popen",
        lambda *args, **kwargs: FakeProcess(),
    )

    player = AudioPlayer()
    player.play(Path("current.mp3"))
    player.play_secondary(Path("next.mp3"))
    player.handoff_secondary()

    assert player.playing is True
    assert player.paused is False


def test_handoff_secondary_does_not_start_new_process(monkeypatch):
    created = []

    def fake_popen(*args, **kwargs):
        process = FakeProcess()
        created.append(process)
        return process

    monkeypatch.setattr("subprocess.Popen", fake_popen)

    player = AudioPlayer()
    player.play(Path("current.mp3"))
    player.play_secondary(Path("next.mp3"))

    assert len(created) == 2

    player.handoff_secondary()

    assert len(created) == 2


def test_play_secondary_keeps_primary_alive(monkeypatch):
    created = []

    def fake_popen(*args, **kwargs):
        process = FakeProcess()
        created.append(process)
        return process

    monkeypatch.setattr("subprocess.Popen", fake_popen)

    player = AudioPlayer()
    player.play(Path("current.mp3"))
    primary_process = player.process

    player.play_secondary(Path("next.mp3"))

    assert player.process is primary_process
    assert player.process.poll() is None
    assert player.secondary_process is not None
    assert player.secondary_process.poll() is None
    assert len(created) == 2


def test_play_secondary_replaces_previous_secondary(monkeypatch):
    created = []

    def fake_popen(*args, **kwargs):
        process = FakeProcess()
        created.append(process)
        return process

    monkeypatch.setattr("subprocess.Popen", fake_popen)

    player = AudioPlayer()
    player.play_secondary(Path("first.mp3"))
    first = player.secondary_process

    player.play_secondary(Path("second.mp3"))

    assert first.terminated is True
    assert player.secondary == Path("second.mp3")
    assert player.secondary_process is not first
    assert len(created) == 2
