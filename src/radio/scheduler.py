"""
ArtistRadio Engine
Radio Scheduler
"""

from collections import deque
from typing import Optional


class RadioScheduler:


    def __init__(
        self,
        radio=None,
    ):

        self.radio = radio

        self.queue = deque()


        self.history = []



    def add(
        self,
        track,
    ):

        if track is None:

            return None


        self.queue.append(
            track
        )


        return track



    def next(
        self,
    ) -> Optional[object]:

        if self.queue:

            track = self.queue.popleft()

            self.history.append(
                track
            )

            return track



        if self.radio is not None:

            track = self.radio.next()


            if track is not None:

                self.history.append(
                    track
                )


            return track



        return None



    def peek(
        self,
    ):

        if not self.queue:

            return None


        return self.queue[0]



    def clear(
        self,
    ):

        self.queue.clear()



    def size(
        self,
    ) -> int:

        return len(
            self.queue
        )