"""
ArtistRadio Engine
Audio Playback Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer


class FakeProcess:

    def terminate(self):
        pass



def test_player_play_starts(
    monkeypatch,
):

    monkeypatch.setattr(
        "subprocess.Popen",
        lambda *args, **kwargs: FakeProcess()
    )


    player = AudioPlayer()

    track = Path(
        "song.mp3"
    )


    player.play(
        track
    )


    assert player.current == track

    assert player.is_playing() is True



def test_player_stop_resets_state(
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

    player.stop()


    assert player.is_playing() is False