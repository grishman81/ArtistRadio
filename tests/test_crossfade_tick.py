"""
ArtistRadio Engine
Crossfade Tick Tests
"""

from src.audio.crossfade import CrossfadeEngine



def test_crossfade_tick_advances_time():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    engine.tick(
        2
    )

    assert engine.elapsed_time == 2



def test_crossfade_tick_updates_progress():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    engine.tick(
        5
    )

    assert engine.progress() == 0.5



def test_crossfade_tick_completes_transition():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    engine.tick(
        10
    )

    assert engine.is_complete() is True