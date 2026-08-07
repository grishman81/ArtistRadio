"""
ArtistRadio Engine
Radio Session Crossfade Tick Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_radio_crossfade_tick_progress():

    engine = CrossfadeEngine(
        duration=5
    )

    engine.start()

    engine.tick(
        1
    )

    assert engine.progress() == 0.2



def test_radio_crossfade_tick_finish():

    engine = CrossfadeEngine(
        duration=5
    )

    engine.start()

    engine.tick(
        5
    )

    assert engine.is_complete() is True