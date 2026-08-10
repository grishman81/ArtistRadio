"""
ArtistRadio Engine
Automatic Transition Loop Tests
"""


from pathlib import Path

from src.radio.session import RadioSession



def test_check_playback_prepares_next_track():

    session = object.__new__(
        RadioSession
    )


    session.next_track = None


    session.should_crossfade = lambda *args: True


    session.prepare_next_track_called = False


    def fake_prepare(track):

        session.prepare_next_track_called = True
        session.next_track = track


    session.prepare_next_track = fake_prepare


    session.check_transition(
        position=230,
        duration=240,
    )


    assert (
        session.prepare_next_track_called
        is True
    )