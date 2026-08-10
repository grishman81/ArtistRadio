"""
ArtistRadio Engine
Runtime Crossfade Session Tests
"""


def test_session_crossfade_engine_runs():

    from src.audio.crossfade import CrossfadeEngine


    engine = CrossfadeEngine(
        duration=5
    )


    engine.start()


    engine.tick(
        2
    )


    levels = engine.update()


    assert levels["old"] == 0.6
    assert levels["new"] == 0.4