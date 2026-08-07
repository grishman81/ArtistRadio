"""
ArtistRadio Engine
Radio Crossfade Volume Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_crossfade_volume_levels():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=5
    )

    assert levels["old"] == 0.5
    assert levels["new"] == 0.5