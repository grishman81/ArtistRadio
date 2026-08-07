"""
ArtistRadio Engine
Radio State
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RadioState:
    """
    Состояние текущего эфира.
    """

    station: str = ""

    track: Optional[str] = None

    running: bool = False

    mode: str = "random"