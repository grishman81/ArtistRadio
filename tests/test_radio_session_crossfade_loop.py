"""
ArtistRadio Engine
Radio Session Crossfade Loop Tests
"""


def test_session_crossfade_can_tick():

    from src.audio.crossfade import CrossfadeEngine

    crossfade = CrossfadeEngine(
        duration=5
    )

    crossfade.start()

    before = crossfade.progress()

    crossfade.tick(
        1
    )

    after = crossfade.progress()

    assert before == 0.0
    assert after == 0.2