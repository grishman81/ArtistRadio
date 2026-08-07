"""
ArtistRadio Engine
Radio Session Crossfade Volume Tests
"""


from src.audio.crossfade import CrossfadeEngine



def test_session_crossfade_volume_flow():

    engine = CrossfadeEngine(
        duration=10
    )

    engine.start()

    levels = engine.update(
        elapsed=5
    )

    assert levels["old"] == 0.5
    assert levels["new"] == 0.5