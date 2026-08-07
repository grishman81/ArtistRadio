"""
ArtistRadio Engine
Radio Mode Restore Tests
"""

from pathlib import Path

from src.radio.state import RadioState
from src.radio.storage import RadioStorage


def test_radio_mode_is_restored(tmp_path):

    file = tmp_path / "radio_state.json"

    storage = RadioStorage(
        file
    )

    state = RadioState(
        station="Test Radio",
        mode="album",
    )

    storage.save(
        state
    )


    restored = storage.load()


    assert restored.station == "Test Radio"

    assert restored.mode == "album"