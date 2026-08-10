"""
ArtistRadio Engine
Next Track Preparation Tests
"""


from src.radio.session import RadioSession



def test_session_can_prepare_next_track():

    session = object.__new__(
        RadioSession
    )


    session.next_track = None


    session.prepare_next_track(
        "next_song.mp3"
    )


    assert session.next_track == "next_song.mp3"