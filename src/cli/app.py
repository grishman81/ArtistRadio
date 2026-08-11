"""
ArtistRadio Engine
CLI Controller
"""

from sched import scheduler
from unittest import result


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

        result = self.session.start()

        scheduler = getattr(
            self.session.radio,
            "scheduler",
            None,
        )

        if scheduler is not None:

            scheduler.ensure_queue()

            self.session.save_queue()

        self.session.save()

        return result

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

    def queue(self):

        scheduler = getattr(
            self.session.radio,
            "scheduler",
            None,
        )

        if scheduler is None:

            return []

        return [str(track.path) for track in scheduler.queue]

    def history(self):

        history = self.session.history

        if history is None:

            return []

        if hasattr(history, "get_all"):

            return history.get_all()

        if hasattr(history, "items"):

            items = history.items

            if callable(items):

                return items()

            return items

        return []
