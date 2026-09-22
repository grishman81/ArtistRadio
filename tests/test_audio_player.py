"""
ArtistRadio Engine
Audio Player Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer


def test_player_initial_state():

    player = AudioPlayer()

    assert player.current is None

    assert player.is_playing() is False

    assert player.current_position() == 0.0


def test_player_seek_position():

    player = AudioPlayer()

    player.seek(120.5)

    assert player.current_position() == 120.5


def test_player_pause_resume():

    player = AudioPlayer()

    player.playing = True

    player.pause()

    assert player.paused is True

    player.resume()

    assert player.paused is False



def test_find_session_retries_until_audio_session_appears(monkeypatch):

    class FakeProcess:
        pid = 1234

    class FakeSession:
        ProcessId = 1234

    class FakeAudioUtilities:
        calls = 0

        @classmethod
        def GetAllSessions(cls):
            cls.calls += 1
            if cls.calls < 3:
                return []
            return [FakeSession()]

    import src.audio.player as player_module

    monkeypatch.setattr(player_module, "PYCAW_AVAILABLE", True)\n    monkeypatch.setattr(player_module, "AudioUtilities", FakeAudioUtilities)
    monkeypatch.setattr(player_module.time, "sleep", lambda _: None)

    player = AudioPlayer()
    session = player._find_session(FakeProcess())

    assert session is not None
    assert FakeAudioUtilities.calls == 3
