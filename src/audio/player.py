"""ArtistRadio Engine
Audio Player

Real-time volume control for ffplay on Windows
using Windows Audio Session API (pycaw).
"""

import subprocess
import time
from pathlib import Path

try:
    from pycaw.pycaw import AudioUtilities
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False


class AudioPlayer:
    """Управление воспроизведением через ffplay."""

    def __init__(self, audio_device: str | None = None):
        self.audio_device = audio_device or ""
        self.started_at = None
        self.current: Path | None = None
        self.secondary: Path | None = None
        self.process = None
        self.secondary_process = None
        self.playing = False
        self.paused = False
        self.volume = 1.0
        self.primary_volume = 1.0
        self.secondary_volume = 0.0
        self.position = 0.0
        self._primary_session = None
        self._secondary_session = None

    def _find_session(self, process):
        if not PYCAW_AVAILABLE or process is None:
            return None

        pid = getattr(process, "pid", None)
        if pid is None:
            return None

        for _ in range(20):
            try:
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions:
                    try:
                        if session.ProcessId == pid:
                            return session
                    except Exception:
                        continue
            except Exception:
                pass
            time.sleep(0.05)
        return None

    def _set_process_volume(self, process, volume):
        if process is None:
            return

        volume = max(0.0, min(1.0, float(volume)))

        if process is self.process:
            session = self._primary_session
        elif process is self.secondary_process:
            session = self._secondary_session
        else:
            session = None

        if session is None:
            session = self._find_session(process)

        if session is None:
            return

        try:
            session.SimpleAudioVolume.SetMasterVolume(volume, None)
        except Exception:
            # Windows audio sessions can be recreated while ffplay is
            # starting or after a device/session change. Refresh the session
            # once instead of silently keeping a stale COM object.
            session = self._find_session(process)
            if session is None:
                return
            try:
                session.SimpleAudioVolume.SetMasterVolume(volume, None)
            except Exception:
                return

        if process is self.process:
            self._primary_session = session
        elif process is self.secondary_process:
            self._secondary_session = session

    def _start_ffplay(self, path: Path):
        command = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            "-volume",
            "100",
        ]
        if self.audio_device:
            command.extend(["-audio_device", self.audio_device])
        command.append(str(path))
        return subprocess.Popen(command)

    def play(self, path: Path, position: float = 0.0) -> None:
        self.stop()
        self.current = path
        self.position = position
        self.started_at = time.time() - position

        self.process = self._start_ffplay(path)
        self.playing = True
        self.paused = False
        self._primary_session = None

        self._set_process_volume(
            self.process,
            self.primary_volume * self.volume,
        )

    def play_secondary(self, path: Path) -> None:
        if self.secondary_process is not None:
            self._terminate_process(self.secondary_process)

        self.secondary = path
        self.secondary_process = self._start_ffplay(path)
        self._secondary_session = None

        self._set_process_volume(
            self.secondary_process,
            self.secondary_volume * self.volume,
        )

    def _terminate_process(self, process) -> None:
        if process is None:
            return
        try:
            process.terminate()
            try:
                process.wait(timeout=1)
            except Exception:
                pass
        except Exception:
            pass

    def handoff_secondary(self) -> None:
        if self.secondary_process is None or self.secondary is None:
            return

        old_primary = self.process
        new_primary = self.secondary_process
        new_current = self.secondary

        self._terminate_process(old_primary)

        self.process = new_primary
        self.current = new_current
        self.secondary_process = None
        self.secondary = None
        self._primary_session = self._secondary_session
        self._secondary_session = None
        self.primary_volume = 1.0
        self.secondary_volume = 0.0
        self.position = 0.0
        self.started_at = time.time()
        self.playing = True
        self.paused = False

    def stop_secondary(self) -> None:
        self._terminate_process(self.secondary_process)
        self.secondary_process = None
        self.secondary = None
        self._secondary_session = None
        self.secondary_volume = 0.0

    def stop(self) -> None:
        self._terminate_process(self.process)
        self.process = None
        self.stop_secondary()
        self.playing = False
        self.paused = False
        self.primary_volume = 1.0
        self.current = None
        self._primary_session = None

    def pause(self) -> None:
        if not self.playing:
            return

        self.position = self.current_position()
        self._terminate_process(self.process)
        self.process = None
        self._primary_session = None
        self.playing = False
        self.paused = True

    def resume(self) -> None:
        if not self.paused:
            return
        if self.current is None:
            self.paused = False
            self.playing = True
            return
        self.play(self.current, self.position)

    def seek(self, position: float) -> None:
        self.position = position
        if self.started_at is not None:
            self.started_at = time.time() - position

    def current_position(self) -> float:
        if self.playing and self.started_at is not None:
            return max(self.position, time.time() - self.started_at)
        return self.position

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, float(volume)))
        if self.process:
            self._set_process_volume(
                self.process,
                self.primary_volume * self.volume,
            )
        if self.secondary_process:
            self._set_process_volume(
                self.secondary_process,
                self.secondary_volume * self.volume,
            )

    def apply_volume(self, volume: float) -> None:
        self.set_volume(volume)

    def apply_primary_volume(self, volume: float) -> None:
        self.primary_volume = max(0.0, min(1.0, float(volume)))
        if self.process:
            self._set_process_volume(
                self.process,
                self.primary_volume * self.volume,
            )

    def apply_secondary_volume(self, volume: float) -> None:
        self.secondary_volume = max(0.0, min(1.0, float(volume)))
        if self.secondary_process:
            self._set_process_volume(
                self.secondary_process,
                self.secondary_volume * self.volume,
            )

    def fade_out(self, steps: int = 10) -> None:
        step = self.volume / max(steps, 1)
        for _ in range(steps):
            self.volume = max(0.0, self.volume - step)
            self.set_volume(self.volume)
        self.volume = 0.0
        self.set_volume(0.0)

    def fade_in(self, steps: int = 10) -> None:
        step = 1.0 / max(steps, 1)
        for _ in range(steps):
            self.volume = min(1.0, self.volume + step)
            self.set_volume(self.volume)

    def is_finished(self) -> bool:
        if not self.process:
            return False
        return self.process.poll() is not None

    def is_playing(self) -> bool:
        return self.playing

    def current_track(self) -> Path | None:
        return self.current
