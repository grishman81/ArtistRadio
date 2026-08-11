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
