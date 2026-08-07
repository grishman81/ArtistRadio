"""
ArtistRadio Engine
Secondary Playback Control Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer



class FakeProcess:

    def __init__(self):

        self.stopped = False


    def terminate(self):

        self.stopped = True



def test_secondary_track_can_be_set():

    player = AudioPlayer()

    track = Path(
        "next_song.mp3"
    )

    player.secondary = track

    assert player.secondary == track



def test_secondary_track_can_be_stopped():

    player = AudioPlayer()

    player.secondary = Path(
        "next_song.mp3"
    )

    player.secondary_process = FakeProcess()


    player.stop_secondary()


    assert player.secondary is None

    assert player.secondary_process is None