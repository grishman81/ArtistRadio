"""
ArtistRadio Engine
Crossfade Timer Tests
"""

from src.audio.crossfade import CrossfadeEngine



def test_crossfade_not_active_on_start():

    engine = CrossfadeEngine()

    assert engine.active is False



def test_crossfade_can_start():

    engine = CrossfadeEngine()

    engine.start()

    assert engine.active is True