"""
ArtistRadio Engine
Audio Finished Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer


class FakeProcess:

    def __init__(self, finished=False):

        self.finished = finished


    def terminate(self):

        pass


    def poll(self):

        if self.finished:

            return 0

        return None



def test_player_detects_finished_track():

    player = AudioPlayer()

    player.current = Path(
        "song.mp3"
    )

    player.process = FakeProcess(
        finished=True
    )

    player.playing = True


    assert player.is_finished() is True



def test_player_detects_running_track():

    player = AudioPlayer()

    player.current = Path(
        "song.mp3"
    )

    player.process = FakeProcess(
        finished=False
    )

    player.playing = True


    assert player.is_finished() is False