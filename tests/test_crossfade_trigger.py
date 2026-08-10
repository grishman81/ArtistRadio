"""
ArtistRadio Engine
Crossfade Trigger Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_crossfade_trigger_time():

    engine = CrossfadeEngine(
        duration=10
    )


    trigger = engine.trigger_time(
        track_length=240
    )


    assert trigger == 230



def test_crossfade_trigger_short_track():

    engine = CrossfadeEngine(
        duration=10
    )


    trigger = engine.trigger_time(
        track_length=5
    )


    assert trigger == 0