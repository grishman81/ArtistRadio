"""
ArtistRadio Engine
CLI Tests
"""

from flask import session

from src.cli.app import RadioCLI


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