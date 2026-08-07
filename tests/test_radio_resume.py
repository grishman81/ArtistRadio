"""
ArtistRadio Engine
Resume Playback Tests
"""

from src.radio.state import RadioState
from src.radio.storage import RadioStorage


def test_last_track_is_restored(tmp_path):

    file = tmp_path / "radio_state.json"

    storage = RadioStorage(
        file
    )

    state = RadioState(
        station="Test Radio",
        mode="album",
        track="song.mp3",
        running=False,
    )

    storage.save(
        state
    )


    restored = storage.load()


    assert restored.station == "Test Radio"

    assert restored.mode == "album"

    assert restored.track == "song.mp3"