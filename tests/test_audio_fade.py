"""
ArtistRadio Engine
Audio Fade Tests
"""

from src.audio.player import AudioPlayer


def test_player_initial_fade_state():

    player = AudioPlayer()

    assert player.volume == 1.0



def test_player_set_volume():

    player = AudioPlayer()

    player.set_volume(
        0.5
    )

    assert player.volume == 0.5