"""
ArtistRadio Engine
Radio Storage
"""

import json
from pathlib import Path

from src.radio.state import RadioState


class RadioStorage:
    """
    Stores radio state.
    """

    def __init__(
        self,
        path: Path,
    ):

        self.path = path

    def save(
        self,
        state: RadioState,
    ) -> None:

        data = {
            "station": state.station,
            "track": state.track,
            "running": state.running,
            "command": state.command,
            "mode": state.mode,
            "position": state.position,
            "queue": state.queue,
            "crossfade_running": state.crossfade_running,
            "crossfade_progress": state.crossfade_progress,
            "next_track": state.next_track,
        }

        self.path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def load(
        self,
    ) -> RadioState:

        if not self.path.exists():

            return RadioState()

        data = json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

        return RadioState(
            station=data.get(
                "station",
                "",
            ),

            track=data.get(
                "track",
            ),

            running=data.get(
                "running",
                False,
            ),

            command=data.get(
                "command",
            ),

            mode=data.get(
                "mode",
                "random",
            ),

            position=data.get(
                "position",
                0.0,
            ),

            queue=data.get(
                "queue",
                [],
            ),

            crossfade_running=data.get(
                "crossfade_running",
                False,
            ),

            crossfade_progress=data.get(
                "crossfade_progress",
                0.0,
            ),

            next_track=data.get(
                "next_track",
            ),
        )