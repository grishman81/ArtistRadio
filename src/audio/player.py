"""
ArtistRadio Engine
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
    """
    РЈРїСЂР°РІР»РµРЅРёРµ РІРѕСЃРїСЂРѕРёР·РІРµРґРµРЅРёРµРј С‡РµСЂРµР· ffplay.

    Р“СЂРѕРјРєРѕСЃС‚СЊ РјРµРЅСЏРµС‚СЃСЏ СЂРµР°Р»СЊРЅРѕ РЅР° СѓСЂРѕРІРЅРµ Windows Audio Session,
    Р° РЅРµ С‚РѕР»СЊРєРѕ РІРѕ РІРЅСѓС‚СЂРµРЅРЅРёС… РїРµСЂРµРјРµРЅРЅС‹С… Python.
    """

    def __init__(self):

        self.started_at = None

        self.current: Path | None = None
        self.secondary: Path | None = None

        self.process = None
        self.secondary_process = None

        self.playing = False
        self.paused = False

        # РћР±С‰Р°СЏ РіСЂРѕРјРєРѕСЃС‚СЊ СЃС‚Р°СЂРѕРіРѕ API
        self.volume = 1.0

        # Р“СЂРѕРјРєРѕСЃС‚Рё РґРѕСЂРѕР¶РµРє РґР»СЏ crossfade
        self.primary_volume = 1.0
        self.secondary_volume = 0.0

        self.position = 0.0

        # Windows audio sessions
        self._primary_session = None
        self._secondary_session = None

    # ------------------------------------------------------------------
    # Windows Audio Session
    # ------------------------------------------------------------------

    def _find_session(self, process):
        """
        РќР°С…РѕРґРёС‚ Windows Audio Session, РїСЂРёРЅР°РґР»РµР¶Р°С‰СѓСЋ СѓРєР°Р·Р°РЅРЅРѕРјСѓ PID.
        """

        if not PYCAW_AVAILABLE:
            return None

        if process is None:
            return None

        pid = getattr(process, "pid", None)

        if pid is None:
            return None

        # Р”Р°РµРј Windows РЅРµРјРЅРѕРіРѕ РІСЂРµРјРµРЅРё СЃРѕР·РґР°С‚СЊ audio session.
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
        """
        Р РµР°Р»СЊРЅРѕ СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚ РіСЂРѕРјРєРѕСЃС‚СЊ РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ ffplay-РїСЂРѕС†РµСЃСЃР°.
        """

        if process is None:
            return

        volume = max(
            0.0,
            min(
                1.0,
                float(volume),
            ),
        )

        session = None

        if process is self.process:
            session = self._primary_session

        elif process is self.secondary_process:
            session = self._secondary_session

        if session is None:
            session = self._find_session(process)

            if process is self.process:
                self._primary_session = session

            elif process is self.secondary_process:
                self._secondary_session = session

        if session is None:
            return

        try:
            audio = session.SimpleAudioVolume

            audio.SetMasterVolume(
                volume,
                None,
            )

        except Exception:
            pass

    # ------------------------------------------------------------------
    # Primary playback
    # ------------------------------------------------------------------

    def play(
        self,
        path: Path,
        position: float = 0.0,
    ) -> None:

        self.stop()

        self.current = path
        self.position = position

        self.started_at = (
            time.time() - position
        )

        command = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            "-volume",
            "100",
            str(path),
        ]

        self.process = subprocess.Popen(
            command
        )

        self.playing = True
        self.paused = False

        self._primary_session = None

        # РќР°С‡Р°Р»СЊРЅРѕРµ Р·РЅР°С‡РµРЅРёРµ СЂРµР°Р»СЊРЅРѕР№ РіСЂРѕРјРєРѕСЃС‚Рё.
        time.sleep(0.05)

        self._set_process_volume(
            self.process,
            self.primary_volume * self.volume,
        )

    # ------------------------------------------------------------------
    # Secondary playback
    # ------------------------------------------------------------------

    def play_secondary(
        self,
        path: Path,
    ) -> None:

        # Р•СЃР»Рё СѓР¶Рµ СЃСѓС‰РµСЃС‚РІСѓРµС‚ РІС‚РѕСЂРёС‡РЅС‹Р№ РїСЂРѕС†РµСЃСЃ,
        # РєРѕСЂСЂРµРєС‚РЅРѕ РѕСЃС‚Р°РЅРѕРІРёРј РµРіРѕ РїРµСЂРµРґ Р·Р°РјРµРЅРѕР№.
        if self.secondary_process is not None:

            self.secondary_process.terminate()

            try:
                self.secondary_process.wait(
                    timeout=1
                )
            except Exception:
                pass

        self.secondary = path

        command = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            "-volume",
            "100",
            str(path),
        ]

        self.secondary_process = subprocess.Popen(
            command
        )

        self._secondary_session = None

        time.sleep(0.05)

        self._set_process_volume(
            self.secondary_process,
            self.secondary_volume * self.volume,
        )

    # ------------------------------------------------------------------
    # Secondary control
    # ------------------------------------------------------------------

    def stop_secondary(self) -> None:

        if self.secondary_process:

            try:
                self.secondary_process.terminate()

                try:
                    self.secondary_process.wait(
                        timeout=1
                    )
                except Exception:
                    pass

            except Exception:
                pass

            self.secondary_process = None

        self.secondary = None

        self._secondary_session = None

        self.secondary_volume = 0.0

    # ------------------------------------------------------------------
    # Stop
    # ------------------------------------------------------------------

    def stop(self) -> None:

        if self.process:

            try:
                self.process.terminate()

                try:
                    self.process.wait(
                        timeout=1
                    )
                except Exception:
                    pass

            except Exception:
                pass

            self.process = None

        self.stop_secondary()

        self.playing = False
        self.paused = False

        self.primary_volume = 1.0

        self._primary_session = None

    # ------------------------------------------------------------------
    # Pause / resume
    # ------------------------------------------------------------------

    def pause(self) -> None:

        if not self.playing:
            return

        self.position = self.current_position()

        if self.process:

            try:
                self.process.terminate()

                try:
                    self.process.wait(
                        timeout=1
                    )
                except Exception:
                    pass

            except Exception:
                pass

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

        self.play(
            self.current,
            self.position,
        )

    # ------------------------------------------------------------------
    # Position
    # ------------------------------------------------------------------

    def seek(
        self,
        position: float,
    ) -> None:

        self.position = position

        if self.started_at is not None:

            self.started_at = (
                time.time() - position
            )

    def current_position(self) -> float:

        if (
            self.playing
            and self.started_at is not None
        ):

            return max(
                self.position,
                time.time() - self.started_at,
            )

        return self.position

    # ------------------------------------------------------------------
    # General volume
    # ------------------------------------------------------------------

    def set_volume(
        self,
        volume: float,
    ) -> None:

        self.volume = max(
            0.0,
            min(
                1.0,
                float(volume),
            ),
        )

        # Р РµР°Р»СЊРЅРѕ РјРµРЅСЏРµРј РіСЂРѕРјРєРѕСЃС‚СЊ РѕР±РѕРёС… РїСЂРѕС†РµСЃСЃРѕРІ.
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

    def apply_volume(
        self,
        volume: float,
    ) -> None:

        self.set_volume(
            volume
        )

    # ------------------------------------------------------------------
    # Crossfade primary volume
    # ------------------------------------------------------------------

    def apply_primary_volume(
        self,
        volume: float,
    ) -> None:

        self.primary_volume = max(
            0.0,
            min(
                1.0,
                float(volume),
            ),
        )

        if self.process:

            self._set_process_volume(
                self.process,
                self.primary_volume * self.volume,
            )

    # ------------------------------------------------------------------
    # Crossfade secondary volume
    # ------------------------------------------------------------------

    def apply_secondary_volume(
        self,
        volume: float,
    ) -> None:

        self.secondary_volume = max(
            0.0,
            min(
                1.0,
                float(volume),
            ),
        )

        if self.secondary_process:

            self._set_process_volume(
                self.secondary_process,
                self.secondary_volume * self.volume,
            )

    # ------------------------------------------------------------------
    # Fade
    # ------------------------------------------------------------------

    def fade_out(
        self,
        steps: int = 10,
    ) -> None:

        step = (
            self.volume
            /
            max(
                steps,
                1,
            )
        )

        for _ in range(steps):

            self.volume = max(
                0.0,
                self.volume - step,
            )

            self.set_volume(
                self.volume
            )

        self.volume = 0.0

        self.set_volume(
            0.0
        )

    def fade_in(
        self,
        steps: int = 10,
    ) -> None:

        step = (
            1.0
            /
            max(
                steps,
                1,
            )
        )

        for _ in range(steps):

            self.volume = min(
                1.0,
                self.volume + step,
            )

            self.set_volume(
                self.volume
            )

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def is_finished(self) -> bool:

        if not self.process:
            return False

        return (
            self.process.poll()
            is not None
        )

    def is_playing(self) -> bool:

        return self.playing

    def current_track(self) -> Path | None:

        return self.current


