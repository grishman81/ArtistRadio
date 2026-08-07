"""
ArtistRadio Engine
Radio Session
"""

from pathlib import Path
from typing import Optional

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


        self.state = RadioState(
            station=radio.station.name,
            mode=radio.station.get_mode().value,
        )


        self.save()



    def save(self):

        self.storage.save(
            self.state
        )



    def start(self):

        self.state.running = True

        self.radio.start()

        self.save()



    def stop(self):

        self.state.position = (
            self.player.current_position()
        )

        self.state.running = False

        self.player.stop()

        self.radio.stop()

        self.save()



    def apply_crossfade(
        self,
        elapsed: float,
    ):

        levels = self.crossfade.update(
            elapsed
        )


        self.player.apply_volume(
            levels["new"]
        )


        return levels



    def transition_to_next_track(
        self,
        track: Track,
        elapsed: float = 0.0,
    ):

        if track is None:

            return None


        self.player.play_secondary(
            track.path
        )


        self.crossfade.start()


        levels = self.crossfade.update(
            elapsed
        )


        self.player.apply_volume(
            levels["new"]
        )


        if self.crossfade.is_complete():

            self.player.stop()

            self.player.play(
                track.path
            )

            self.player.stop_secondary()


            self.state.track = str(
                track.path
            )

            self.state.position = 0.0


            self.history.add(
                track
            )

            self.save()


        return levels



    def play_next(self) -> Optional[Track]:

        if not self.state.running:

            return None


        if self.player.is_playing():

            self.crossfade.fade_out_old(
                self.player
            )


        track = self.radio.next()


        if track:

            self.state.track = str(
                track.path
            )

            self.state.position = 0.0


            self.player.play(
                track.path
            )


            self.crossfade.start()


            self.apply_crossfade(
                0
            )


            self.crossfade.fade_in_new(
                self.player
            )


            self.history.add(
                track
            )


            self.save()


        return track



    def play_history_item(
        self,
        index: int,
    ) -> Optional[Track]:


        item = self.history.get(
            index
        )


        if item is None:

            return None


        track = Track(
            artist=item["artist"],
            album=item["album"],
            title=item["title"],
            year=item["year"],
            path=Path(
                item["path"]
            ),
        )


        self.state.track = str(
            track.path
        )

        self.state.position = 0.0


        self.player.play(
            track.path
        )


        self.save()


        return track



    def resume_playback(self):

        if not self.state.track:

            return self.play_next()


        tracks = self.radio.station.library.get_tracks(
            self.radio.station.artist
        )


        for track in tracks:

            if str(track.path) == self.state.track:

                self.player.play(
                    track.path,
                    self.state.position,
                )

                self.history.add(
                    track
                )

                return track


        return self.play_next()



    def check_playback(self):

        if not self.state.running:

            return None


        if self.player.is_finished():

            return self.play_next()


        return None



    def switch_station(
        self,
        station: Station,
    ):


        self.player.stop()


        self.radio = RadioEngine(
            station
        )


        self.state.station = (
            station.name
        )


        self.state.mode = (
            station.get_mode().value
        )


        self.state.track = None

        self.state.position = 0.0


        self.save()