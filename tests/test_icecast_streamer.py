from src.streaming.icecast import IcecastConfig, IcecastStreamer


def test_icecast_config_normalizes_mount_and_builds_url():
    config = IcecastConfig(host="192.168.1.10", port=8000, mount="artist.mp3")

    assert config.normalized_mount == "/artist.mp3"
    assert config.url == "http://192.168.1.10:8000/artist.mp3"


def test_icecast_command_captures_directshow_audio_and_publishes_mp3():
    config = IcecastConfig(
        host="192.168.1.10",
        port=8000,
        mount="/radio.mp3",
        password="secret",
        name="ArtistRadio",
        genre="Pop",
        audio_device="CABLE Output (VB-Audio Virtual Cable)",
        bitrate=320,
        sample_rate=44100,
        channels=2,
    )

    command = IcecastStreamer(config).build_command()

    assert command[:4] == ["ffmpeg", "-hide_banner", "-loglevel", "warning"]
    assert "dshow" in command
    assert 'audio=CABLE Output (VB-Audio Virtual Cable)' in command
    assert "libmp3lame" in command
    assert "320k" in command
    assert "icecast://source:secret@192.168.1.10:8000/radio.mp3" in command
    assert "-ice_name" in command
    assert "ArtistRadio" in command


def test_icecast_requires_audio_device():
    streamer = IcecastStreamer(IcecastConfig())

    try:
        streamer.build_command()
    except ValueError as exc:
        assert "audio_device" in str(exc)
    else:
        raise AssertionError("Expected missing audio device to be rejected")
