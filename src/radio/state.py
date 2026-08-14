"""
ArtistRadio Engine
Radio State
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RadioState:
    """
    Current radio state.
    """


    station: str = ""

    track: Optional[str] = None

    running: bool = False

    command: Optional[str] = None

    mode: str = "random"

    position: float = 0.0

    queue: list[str] = field(
        default_factory=list
    )

    crossfade_running: bool = False
    crossfade_progress: float = 0.0
    next_track: Optional[str] = None