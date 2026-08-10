"""
ArtistRadio Engine
Automatic Crossfade Loop Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_crossfade_loop_advances():

    engine = CrossfadeEngine(
        duration=5
    )

    engine.start()

    engine.tick(
        1
    )

    levels = engine.update()

    assert levels["old"] == 0.8
    assert levels["new"] == 0.2



def test_crossfade_loop_finishes():

    engine = CrossfadeEngine(
        duration=5
    )

    engine.start()

    engine.tick(
        5
    )

    assert engine.is_complete() is True