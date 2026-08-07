"""
ArtistRadio Engine
Radio Crossfade Apply Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_crossfade_apply_returns_volume_levels():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=2
    )

    assert levels["old"] == 0.8
    assert levels["new"] == 0.2