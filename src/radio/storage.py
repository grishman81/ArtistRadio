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
            "mode": state.mode,
            "position": state.position,
        }


        self.path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )



    def load(self) -> RadioState:

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
                "track"
            ),

            running=data.get(
                "running",
                False,
            ),

            mode=data.get(
                "mode",
                "random",
            ),

            position=data.get(
                "position",
                0.0,
            ),
        )