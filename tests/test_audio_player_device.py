import src.audio.player as player_module
from src.audio.player import AudioPlayer


def test_player_passes_optional_audio_device_to_ffplay(monkeypatch):
    captured = {}

    def fake_popen(command):
        captured["command"] = command
        return object()

    monkeypatch.setattr(player_module.subprocess, "Popen", fake_popen)

    player = AudioPlayer(audio_device="CABLE Input (VB-Audio Virtual Cable)")
    player._start_ffplay("track.mp3")

    assert captured["command"][-3:] == [
        "-audio_device",
        "CABLE Input (VB-Audio Virtual Cable)",
        "track.mp3",
    ]
