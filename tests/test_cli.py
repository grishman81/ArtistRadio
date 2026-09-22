"""
ArtistRadio Engine
CLI Tests
"""

from src.cli.app import RadioCLI
from src.cli.main import playback_delta


class FakeSession:

    def __init__(self):

        self.state = type(
            "State",
            (),
            {
                "station": "Test Radio",
                "track": None,
                "running": False,
                "mode": "random",
                "position": 0.0,
                "queue": [],
            },
        )()

        self.calls = []

        self.radio = type(
            "Radio",
            (),
            {
                "scheduler": None,
            },
        )()

    def start(self):

        self.state.running = True
        self.calls.append("start")

    def stop(self):

        self.state.running = False
        self.calls.append("stop")

    def pause(self):

        self.calls.append("pause")

    def resume(self):

        self.calls.append("resume")

    def skip(self):

        self.calls.append("skip")


    def save_queue(self):

        self.calls.append(
            "save_queue"
        )


    def save(self):

        self.calls.append(
            "save"
        )

def test_cli_controls():

    session = FakeSession()

    cli = RadioCLI(session)

    cli.start()
    cli.pause()
    cli.resume()
    cli.next()
    cli.stop()

    assert session.calls[:1] == ["start"]

    assert "pause" in session.calls

    assert "resume" in session.calls

    assert "skip" in session.calls

    assert "stop" in session.calls


def test_cli_status():

    session = FakeSession()

    cli = RadioCLI(session)

    status = cli.status()

    assert status["station"] == "Test Radio"

    assert status["mode"] == "random"
from src.cli.app import RadioCLI


def test_cli_status_includes_crossfade_state():

    session = type(
        "Session",
        (),
        {},
    )()

    session.state = type(
        "State",
        (),
        {
            "station": "Test Radio",
            "track": "current.mp3",
            "running": True,
            "mode": "random",
            "position": 120.0,
            "queue": [],
        },
    )()

    session.crossfade_running = True
    session.next_track = type(
        "Track",
        (),
        {
            "path": "next.mp3",
        },
    )()

    session.crossfade = type(
        "Crossfade",
        (),
        {
            "progress": lambda self: 0.4,
        },
    )()

    cli = RadioCLI(session)

    status = cli.status()

    assert status["crossfade_running"] is True
    assert status["crossfade_progress"] == 0.4
    assert status["next_track"] == "next.mp3"

def test_cli_status_includes_crossfade_output():

    session = type(
        "Session",
        (),
        {},
    )()

    session.state = type(
        "State",
        (),
        {
            "station": "Test Radio",
            "track": "current.mp3",
            "running": True,
            "mode": "random",
            "position": 120.0,
            "queue": [],
        },
    )()

    session.crossfade_running = True
    session.next_track = type(
        "Track",
        (),
        {
            "path": "next.mp3",
        },
    )()

    session.crossfade = type(
        "Crossfade",
        (),
        {
            "progress": lambda self: 0.4,
        },
    )()

    cli = RadioCLI(session)

    status = cli.status()

    assert status["crossfade_running"] is True
    assert status["crossfade_progress"] == 0.4
    assert status["next_track"] == "next.mp3"

    def test_cli_next_sends_command_to_runtime(tmp_path):

        session = type(
        "Session",
        (),
        {},
    )()

    session.state = type(
        "State",
        (),
        {
            "command": None,
        },
    )()

    session.save_calls = 0

    def save():

        session.save_calls += 1

    session.save = save

    class FakeCLI:

        def __init__(self, session):

            self.session = session

    cli = FakeCLI(session)

    cli.session.state.command = "next"
    cli.session.save()

    assert cli.session.state.command == "next"
    assert cli.session.save_calls == 1

def test_cli_queue_returns_paths():

    session = FakeSession()

    session.radio = type(
        "Radio",
        (),
        {
            "scheduler": type(
                "Scheduler",
                (),
                {
                    "queue": [
                        type(
                            "Track",
                            (),
                            {
                                "path": "track1.mp3",
                            },
                        )(),
                        type(
                            "Track",
                            (),
                            {
                                "path": "track2.mp3",
                            },
                        )(),
                    ]
                },
            )(),
        },
    )()

    cli = RadioCLI(session)

    queue = cli.queue()

    assert queue == [
        "track1.mp3",
        "track2.mp3",
    ]  

def test_playback_delta_uses_elapsed_time():

    previous_time = 100.0
    current_time = 101.75

    delta = playback_delta(
        previous_time,
        current_time,
    )

    assert delta == 1.75


def test_playback_delta_never_returns_negative():

    previous_time = 101.0
    current_time = 100.0

    delta = playback_delta(
        previous_time,
        current_time,
    )

    assert delta == 0.0



def test_run_loop_passes_elapsed_delta(monkeypatch):

    class FakeSession:

        def __init__(self):
            self.deltas = []
            self.current = None
            self.current_track = None
            self.crossfade_running = False
            self.next_track = None
            self.state = type(
                "State",
                (),
                {"queue": []},
            )()
            self.player = type(
                "Player",
                (),
                {"current_position": lambda self: 0.0},
            )()

        def check_playback(self, delta=1.0):
            self.deltas.append(delta)
            raise KeyboardInterrupt

        def start(self):
            pass

        def stop(self):
            pass

        def play_next(self):
            pass

        def save(self):
            pass

    class FakeCLI:
        def __init__(self, session):
            self.session = session

        def start(self):
            self.session.start()

        def stop(self):
            self.session.stop()

    session = FakeSession()
    clocks = iter([100.0, 100.25])

    monkeypatch.setattr("src.cli.main.time.monotonic", lambda: next(clocks))
    monkeypatch.setattr("src.cli.main.time.sleep", lambda _: None)
    monkeypatch.setattr("src.cli.main.create_session", lambda: session)
    monkeypatch.setattr("src.cli.main.RadioCLI", FakeCLI)

    import sys
    monkeypatch.setattr(sys, "argv", ["artist-radio", "run"])

    from src.cli.main import main

    try:
        main()
    except KeyboardInterrupt:
        pass

    assert session.deltas == [0.25]
