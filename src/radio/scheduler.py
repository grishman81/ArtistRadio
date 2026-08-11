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
        history=None,
        queue_limit: int = 3,
        refill_after_next: bool = True,
    ):

        self.radio = radio

        self.history = history

        self.queue = deque()

        self.queue_limit = queue_limit

        self.refill_after_next = refill_after_next



    def add(
        self,
        track,
    ):

        if track is None:

            return None


        if self.was_played_recently(
            track
        ):

            return None


        self.queue.append(
            track
        )


        return track



    def was_played_recently(
        self,
        track,
    ) -> bool:


        if (
            self.history is None
            or track is None
        ):

            return False


        return self.history.contains(
            track
        )



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

        attempts = 0


        while len(self.queue) < target:


            attempts += 1


            if attempts > target * 5:

                break


            track = self.radio.next()


            if track is None:

                break


            if self.was_played_recently(
                track
            ):

                continue


            self.queue.append(
                track
            )


            added += 1


        return added



    def refill(
        self,
    ):

        return self.fill()



    def ensure_queue(
        self,
    ):

        if len(self.queue) < self.queue_limit:

            return self.fill()


        return 0



    def next(
        self,
    ) -> Optional[object]:


        if not self.queue:

            self.ensure_queue()



        if self.queue:

            track = self.queue.popleft()


            if self.refill_after_next:

                self.ensure_queue()


            return track



        if self.radio is not None:

            track = self.radio.next()


            if track is not None:

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



    def export_queue(
        self,
    ) -> list[str]:


        return [
            str(
                track.path
            )
            for track in self.queue
        ]



    def restore_queue(
        self,
        tracks: list,
    ) -> None:


        self.queue.clear()


        if not tracks:

            return


        for track in tracks:

            self.queue.append(
                track
            )



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