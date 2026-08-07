"""
ArtistRadio Engine
Crossfade Tests
"""

from src.audio.crossfade import CrossfadeEngine



def test_crossfade_default_duration():

    crossfade = CrossfadeEngine()

    assert crossfade.duration == 5



def test_crossfade_custom_duration():

    crossfade = CrossfadeEngine(
        duration=10
    )

    assert crossfade.duration == 10