"""Icecast stream capture and publishing for Windows."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass


@dataclass
class IcecastConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    mount: str = "/artist-radio.mp3"
    password: str = "hackme"
    name: str = "ArtistRadio"
    genre: str = "Various"
    audio_device: str = ""
    bitrate: int = 320
    sample_rate: int = 44100
    channels: int = 2

    @classmethod
    def from_env(cls) -> "IcecastConfig":
        return cls(
            host=os.getenv("AR_ICECAST_HOST", cls.host),
            port=int(os.getenv("AR_ICECAST_PORT", cls.port)),
            mount=os.getenv("AR_ICECAST_MOUNT", cls.mount),
            password=os.getenv("AR_ICECAST_PASSWORD", cls.password),
            name=os.getenv("AR_ICECAST_NAME", cls.name),
            genre=os.getenv("AR_ICECAST_GENRE", cls.genre),
            audio_device=os.getenv("AR_STREAM_AUDIO_DEVICE", ""),
            bitrate=int(os.getenv("AR_STREAM_BITRATE", cls.bitrate)),
            sample_rate=int(os.getenv("AR_STREAM_SAMPLE_RATE", cls.sample_rate)),
            channels=int(os.getenv("AR_STREAM_CHANNELS", cls.channels)),
        )

    @property
    def normalized_mount(self) -> str:
        return self.mount if self.mount.startswith("/") else f"/{self.mount}"

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}{self.normalized_mount}"


class IcecastStreamer:
    """Capture a Windows audio device and publish it to Icecast via FFmpeg.

    The recommended device is the recording side of a virtual audio cable.
    ArtistRadio's ffplay processes can be routed to the playback side of that
    cable, so the captured signal contains the same crossfade heard locally.
    """

    def __init__(self, config: IcecastConfig):
        self.config = config
        self.process: subprocess.Popen | None = None

    @property
    def running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def build_command(self) -> list[str]:
        if not self.config.audio_device:
            raise ValueError("Icecast streaming requires audio_device")

        return [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-f",
            "dshow",
            "-audio_buffer_size",
            "100",
            "-i",
            f'audio={self.config.audio_device}',
            "-vn",
            "-ar",
            str(self.config.sample_rate),
            "-ac",
            str(self.config.channels),
            "-c:a",
            "libmp3lame",
            "-b:a",
            f"{self.config.bitrate}k",
            "-content_type",
            "audio/mpeg",
            "-f",
            "mp3",
            "-ice_name",
            self.config.name,
            "-ice_genre",
            self.config.genre,
            f"icecast://source:{self.config.password}@{self.config.host}:{self.config.port}{self.config.normalized_mount}",
        ]

    def start(self) -> None:
        if self.running:
            return

        self.process = subprocess.Popen(
            self.build_command(),
            stdin=subprocess.DEVNULL,
        )

    def stop(self) -> None:
        process = self.process
        self.process = None
        if process is None:
            return

        try:
            process.terminate()
            process.wait(timeout=2)
        except (OSError, subprocess.TimeoutExpired):
            try:
                process.kill()
            except OSError:
                pass
