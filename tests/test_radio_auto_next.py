"""
ArtistRadio Engine
Auto Next Track Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer


class FakeProcess:

    def terminate(self):
        pass

    def poll(self):
        return 0



def test_finished_player_reports_finished():

    player = AudioPlayer()

    player.process = FakeProcess()

    player.current = Path(
        "song.mp3"
    )

    player.playing = True


    assert player.is_finished() is True