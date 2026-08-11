"""
ArtistRadio Engine
CLI Controller
"""


class RadioCLI:
    """
    Управление радио через команды.
    """

    def __init__(
        self,
        session,
    ):

        self.session = session


    def start(self):

        return self.session.start()


    def stop(self):

        return self.session.stop()


    def pause(self):

        return self.session.pause()


    def resume(self):

        return self.session.resume()


    def next(self):

        return self.session.skip()


    def status(self):

        state = self.session.state

        return {
            "station": state.station,
            "track": state.track,
            "running": state.running,
            "mode": state.mode,
            "position": state.position,
            "queue": state.queue,
        }