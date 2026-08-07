"""
ArtistRadio Engine
Crossfade Stop Tests
"""

from src.audio.crossfade import CrossfadeEngine



def test_crossfade_can_stop():

    engine = CrossfadeEngine()

    engine.start()

    assert engine.active is True


    engine.stop()

    assert engine.active is False