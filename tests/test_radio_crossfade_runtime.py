"""
ArtistRadio Engine
Radio Runtime Crossfade Tests
"""


def test_radio_session_has_crossfade_engine():

    from src.audio.crossfade import CrossfadeEngine

    engine = CrossfadeEngine()

    engine.start()

    engine.tick(
        1
    )

    assert engine.active is True
    assert engine.progress() > 0