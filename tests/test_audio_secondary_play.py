"""
ArtistRadio Engine
Secondary Playback Start Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer



class FakeProcess:

    def __init__(self):

        self.stopped = False


    def terminate(self):

        self.stopped = True



def test_secondary_play_stores_track(monkeypatch):

    monkeypatch.setattr(
        "subprocess.Popen",
        lambda *args, **kwargs: FakeProcess()
    )


    player = AudioPlayer()

    track = Path(
        "next_song.mp3"
    )


    player.play_secondary(
        track
    )


    assert player.secondary == track

    assert player.secondary_process is not None



def test_secondary_play_can_replace_track(monkeypatch):

    monkeypatch.setattr(
        "subprocess.Popen",
        lambda *args, **kwargs: FakeProcess()
    )


    player = AudioPlayer()


    first = Path(
        "first.mp3"
    )

    second = Path(
        "second.mp3"
    )


    player.play_secondary(
        first
    )

    player.play_secondary(
        second
    )


    assert player.secondary == second