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
        queue_limit: int = 3,
    ):

        self.radio = radio

        self.queue = deque()

        self.history = []

        self.queue_limit = queue_limit



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



    def fill(
        self,
        count: Optional[int] = None,
    ):

        if self.radio is None:

            return 0


        target = (
            self.queue_limit
            if count is None
            else count
        )


        added = 0


        while len(self.queue) < target:

            track = self.radio.next()


            if track is None:

                break


            self.queue.append(
                track
            )


            added += 1


        return added



    def ensure_queue(
        self,
    ):

        return self.fill()



    def next(
        self,
    ) -> Optional[object]:


        if not self.queue:

            self.ensure_queue()



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

            self.ensure_queue()


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