"""
ArtistRadio Engine
Audio Player Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer


def test_player_initial_state():

    player = AudioPlayer()

    assert player.current is None

    assert player.is_playing() is False

    assert player.current_position() == 0.0



def test_player_seek_position():

    player = AudioPlayer()

    player.seek(
        120.5
    )

    assert player.current_position() == 120.5