"""
ArtistRadio Engine
Crossfade Update Tests
"""

from src.audio.crossfade import CrossfadeEngine



def test_crossfade_update_at_start():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=0
    )

    assert levels["old"] == 1.0
    assert levels["new"] == 0.0



def test_crossfade_update_halfway():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=5
    )

    assert levels["old"] == 0.5
    assert levels["new"] == 0.5



def test_crossfade_update_complete():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=10
    )

    assert levels["old"] == 0.0
    assert levels["new"] == 1.0