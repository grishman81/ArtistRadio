"""
ArtistRadio Engine
Radio Dual Crossfade Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_radio_dual_crossfade_levels():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=5
    )

    assert levels["old"] == 0.5
    assert levels["new"] == 0.5



def test_radio_dual_crossfade_completion():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=10
    )

    assert levels["old"] == 0.0
    assert levels["new"] == 1.0