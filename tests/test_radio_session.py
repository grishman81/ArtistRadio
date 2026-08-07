"""
ArtistRadio Engine
Radio Session Tests
"""

from pathlib import Path

from src.library.library import Library

from src.radio.history import PlaybackHistory
from src.radio.engine import RadioEngine
from src.radio.session import RadioSession
from src.radio.storage import RadioStorage

from src.playlist.history import PlaylistHistory
from src.playlist.randomizer import PlaylistRandomizer
from src.playlist.engine import PlaylistEngine

from src.station.station import Station

from src.audio.player import AudioPlayer


def create_session():

    library = Library(
        Path("database")
    )

    playlist_history = PlaylistHistory()

    randomizer = PlaylistRandomizer(
        playlist_history
    )

    playlist = PlaylistEngine(
        randomizer,
        playlist_history,
    )

    station = Station(
        name="Jennifer Lopez Radio",
        artist="Jennifer Lopez",
        library=library,
        playlist=playlist,
    )

    radio = RadioEngine(
        station
    )

    storage = RadioStorage(
        Path("test_radio_state.json")
    )

    playback_history = PlaybackHistory(
        Path("test_radio_history.json")
    )

    player = AudioPlayer()

    return RadioSession(
        radio,
        storage,
        player,
        playback_history,
    )


def test_radio_session_start_stop():

    session = create_session()

    session.start()

    assert session.state.running is True

    session.stop()

    assert session.state.running is False


def test_radio_session_play_next():

    session = create_session()

    session.start()

    track = session.play_next()

    assert track is not None

    assert (
        session.state.track
        == str(track.path)
    )

    assert (
        session.player.current
        == track.path
    )

    session.stop()