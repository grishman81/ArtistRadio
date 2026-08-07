"""
ArtistRadio Engine
Radio State
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RadioState:
    """
    Current radio state.
    """

    station: str = ""

    track: Optional[str] = None

    running: bool = False

    mode: str = "random"

    position: float = 0.0