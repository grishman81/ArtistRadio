"""
ArtistRadio Engine
Radio Transition Scheduler Tests
"""


from src.radio.session import RadioSession



def test_should_crossfade_when_near_end():

    session = object.__new__(
        RadioSession
    )

    session.crossfade_duration = 10


    result = session.should_crossfade(
        position=230,
        duration=240,
    )


    assert result is True



def test_should_not_crossfade_early():

    session = object.__new__(
        RadioSession
    )

    session.crossfade_duration = 10


    result = session.should_crossfade(
        position=100,
        duration=240,
    )


    assert result is False