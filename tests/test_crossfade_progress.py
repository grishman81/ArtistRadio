"""
ArtistRadio Engine
Crossfade Progress Tests
"""

from src.audio.crossfade import CrossfadeEngine



def test_crossfade_starts_with_zero_progress():

    engine = CrossfadeEngine()

    assert engine.progress() == 0.0



def test_crossfade_progress_after_start():

    engine = CrossfadeEngine()

    engine.start()

    assert engine.progress() >= 0.0



def test_crossfade_complete_after_duration():

    engine = CrossfadeEngine()

    engine.start()

    engine.elapsed_time = engine.duration

    assert engine.is_complete() is True