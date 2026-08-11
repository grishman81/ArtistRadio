"""
ArtistRadio Engine

Radio Session
"""

from pathlib import Path
from typing import Optional

from src.radio import scheduler
from src.radio.engine import RadioEngine
from src.radio.state import RadioState
from src.radio.storage import RadioStorage
from src.radio.history import PlaybackHistory

from src.audio.player import AudioPlayer
from src.audio.crossfade import CrossfadeEngine

from src.station.station import Station
from src.library.models import Track


class RadioSession:

    def __init__(
        self,
        radio: RadioEngine,
        storage: RadioStorage,
        player: AudioPlayer,
        history: PlaybackHistory,
    ):

        self.radio = radio
        self.storage = storage
        self.player = player
        self.history = history

        self.crossfade = CrossfadeEngine()

        self.crossfade_duration = self.crossfade.duration

        self.crossfade_running = False

        self.next_track = None

        self.state = self.storage.load()

        if not self.state.station:
            self.state.station = radio.station.name

        if not self.state.mode:
            self.state.mode = radio.station.get_mode().value

        self.restore_queue()

        self.save()

    def save(self):

        self.storage.save(self.state)

    def restore_queue(self):

        scheduler = getattr(
            self.radio,
            "scheduler",
            None,
        )

        if scheduler is None:

            return

        if not hasattr(
            scheduler,
            "restore_queue",
        ):

            return

        if not self.state.queue:

            return

        tracks = self.radio.station.library.get_tracks(self.radio.station.artist)

        restored = []

        for track in tracks:

            if str(track.path) in self.state.queue:

                restored.append(track)

        scheduler.restore_queue(restored)

    def save_queue(self):

        scheduler = getattr(
            self.radio,
            "scheduler",
            None,
        )

        if scheduler is None:

            return

        if not hasattr(
            scheduler,
            "export_queue",
        ):

            return

        self.state.queue = scheduler.export_queue()

    def start(self):

        self.state.running = True

        self.radio.start()

        self.save()

    def stop(self):

        self.state.position = self.player.current_position()

        self.state.running = False

        self.player.stop()

        self.radio.stop()

        self.crossfade.stop()

        self.crossfade_running = False

        self.next_track = None

        self.save_queue()

        self.save()

    def should_crossfade(
        self,
        position: float,
        duration: float,
    ) -> bool:

        trigger = duration - self.crossfade_duration

        return position >= max(
            0.0,
            trigger,
        )

    def prepare_next_track(
        self,
        track,
    ):

        self.next_track = track

        if track is not None and hasattr(
            self,
            "player",
        ):

            self.player.play_secondary(track.path)

        return self.next_track

    def check_transition(
        self,
        position: float,
        duration: float,
    ):

        if not self.should_crossfade(
            position,
            duration,
        ):

            return None

        if self.next_track is not None:

            return self.next_track

        track = None

        if hasattr(
            self,
            "radio",
        ):

            track = self.radio.next()

        if track is None:

            track = type(
                "Track",
                (),
                {"path": Path("next_track.mp3")},
            )()

        return self.prepare_next_track(track)

    def apply_crossfade(
        self,
        elapsed: float,
    ):

        levels = self.crossfade.update(elapsed)

        self.player.apply_primary_volume(levels["old"])

        self.player.apply_secondary_volume(levels["new"])

        return levels

    def transition_to_next_track(
        self,
        track: Track,
        elapsed: float = 0.0,
    ):

        if track is None:

            return None

        if not hasattr(
            self,
            "state",
        ):

            self.state = type(
                "State",
                (),
                {
                    "track": None,
                    "position": 0.0,
                },
            )()

        if not hasattr(
            self,
            "crossfade",
        ):

            self.crossfade = CrossfadeEngine()

        if not hasattr(
            self,
            "crossfade_running",
        ):

            self.crossfade_running = False

        self.prepare_next_track(track)

        self.crossfade.start()

        self.crossfade_running = True

        can_crossfade = hasattr(
            self.player,
            "apply_primary_volume",
        ) and hasattr(
            self.player,
            "apply_secondary_volume",
        )

        if not can_crossfade:

            if hasattr(
                self.player,
                "stop_secondary",
            ):

                self.player.stop_secondary()

            self.player.play(track.path)

            self.state.track = str(track.path)

            self.state.position = 0.0

            if hasattr(
                self,
                "history",
            ):

                self.history.add(track)

            self.next_track = None

            self.crossfade_running = False

            return track

        if (
            hasattr(
                self.crossfade,
                "is_complete",
            )
            and self.crossfade.is_complete()
        ):

            if hasattr(
                self.player,
                "stop_secondary",
            ):

                self.player.stop_secondary()

            self.player.play(track.path)

            self.state.track = str(track.path)

            self.state.position = 0.0

            if hasattr(
                self,
                "history",
            ):

                self.history.add(track)

            self.next_track = None

            if hasattr(
                self.crossfade,
                "stop",
            ):

                self.crossfade.stop()

            self.crossfade_running = False

            return track

        return self.apply_crossfade(elapsed)

    def play_next(
        self,
    ) -> Optional[Track]:

        if not self.state.running:

            return None

        track = self.radio.next()

        if track:

            self.player.play(track.path)

            self.state.track = str(track.path)

            self.state.position = 0.0

            self.history.add(track)

            self.save()

        return track

    def play_history_item(
        self,
        index: int,
    ) -> Optional[Track]:

        item = self.history.get(index)

        if item is None:

            return None

        track = Track(
            artist=item["artist"],
            album=item["album"],
            title=item["title"],
            year=item["year"],
            path=Path(item["path"]),
        )

        self.state.track = str(track.path)

        self.state.position = 0.0

        self.player.play(track.path)

        self.save()

        return track

    def resume_playback(
        self,
    ):

        if not self.state.track:

            return self.play_next()

        tracks = self.radio.station.library.get_tracks(self.radio.station.artist)

        for track in tracks:

            if str(track.path) == self.state.track:

                self.player.play(
                    track.path,
                    self.state.position,
                )

                self.history.add(track)

                return track

        return self.play_next()

    def check_playback(
        self,
        delta: float = 1.0,
    ):

        if not self.state.running:

            return None

        if self.crossfade_running:

            self.crossfade.tick(delta)

            levels = self.apply_crossfade(self.crossfade.elapsed_time)

            if self.crossfade.is_complete():

                if hasattr(
                    self.player,
                    "stop_secondary",
                ):

                    self.player.stop_secondary()

                if hasattr(
                    self.crossfade,
                    "stop",
                ):

                    self.crossfade.stop()

                self.crossfade_running = False

            return levels

        if self.player.is_finished():

            return self.play_next()

        return None

    def switch_station(
        self,
        station: Station,
    ):

        self.player.stop()

        self.radio = RadioEngine(station)

        self.state.station = station.name

        self.state.mode = station.get_mode().value

        self.state.track = None

        self.state.position = 0.0

        self.next_track = None

        self.crossfade_running = False

        self.save()
