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

        self.state.running = False

        self.player.stop()

        self.radio.stop()

        self.save()


    def play_next(self) -> Optional[Track]:

        if not self.state.running:

            return None


        track = self.radio.next()


        if track:

            self.state.track = str(
                track.path
            )

            self.player.play(
                track.path
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


        self.player.play(
            track.path
        )


        self.state.track = str(
            track.path
        )


        self.save()


        return track



    def resume_playback(self):

        return self.play_next()



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


        self.save()