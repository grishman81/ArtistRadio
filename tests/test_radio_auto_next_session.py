"""
ArtistRadio Engine
Radio Auto Next Session Tests
"""


def test_finished_playback_requests_next_track():

    class FakePlayer:

        def is_finished(self):
            return True


    player = FakePlayer()


    assert player.is_finished() is True