"""
ArtistRadio Engine
Radio Crossfade Tests
"""


def test_crossfade_transition_state():

    transition = {
        "active": True,
        "duration": 5,
    }

    assert transition["active"] is True
    assert transition["duration"] == 5