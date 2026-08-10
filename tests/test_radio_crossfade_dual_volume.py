"""
ArtistRadio Engine
Dual Volume Crossfade Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_crossfade_controls_both_volumes():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    engine.tick(
        5
    )

    levels = engine.update()

    assert levels["old"] == 0.5
    assert levels["new"] == 0.5