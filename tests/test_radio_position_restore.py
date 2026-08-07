"""
ArtistRadio Engine
Playback Position Tests
"""

from src.radio.state import RadioState
from src.radio.storage import RadioStorage


def test_playback_position_is_restored(tmp_path):

    file = tmp_path / "radio_state.json"

    storage = RadioStorage(
        file
    )

    state = RadioState(
        station="Test Radio",
        mode="album",
        track="song.mp3",
        position=125.5,
    )

    storage.save(
        state
    )


    restored = storage.load()


    assert restored.track == "song.mp3"

    assert restored.position == 125.5