"""
ArtistRadio Engine
Audio Pause Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer


class FakeProcess:

    def terminate(self):
        pass



def test_player_pause_and_resume(
    monkeypatch,
):

    monkeypatch.setattr(
        "subprocess.Popen",
        lambda *args, **kwargs: FakeProcess()
    )


    player = AudioPlayer()


    player.play(
        Path("song.mp3")
    )


    player.seek(
        50.0
    )


    player.pause()


    assert player.paused is True

    assert player.current_position() >= 50.0


    player.resume()


    assert player.paused is False