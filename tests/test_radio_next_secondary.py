"""
ArtistRadio Engine
Next Track Secondary Playback Tests
"""


from pathlib import Path

from src.radio.session import RadioSession



class FakePlayer:


    def __init__(self):

        self.secondary = None



    def play_secondary(
        self,
        path,
    ):

        self.secondary = path



def test_prepare_next_track_starts_secondary():


    session = object.__new__(
        RadioSession
    )


    session.player = FakePlayer()


    track = type(
        "Track",
        (),
        {
            "path": Path(
                "next_song.mp3"
            )
        },
    )()



    session.prepare_next_track(
        track
    )


    assert (
        session.player.secondary
        ==
        track.path
    )