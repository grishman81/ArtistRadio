"""
ArtistRadio Engine
CLI Tests
"""

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



def test_cli_controls():

    session = FakeSession()

    cli = RadioCLI(session)


    cli.start()
    cli.pause()
    cli.resume()
    cli.next()
    cli.stop()


    assert session.calls == [
        "start",
        "pause",
        "resume",
        "skip",
        "stop",
    ]



def test_cli_status():

    session = FakeSession()

    cli = RadioCLI(session)


    status = cli.status()


    assert status["station"] == "Test Radio"

    assert status["mode"] == "random"