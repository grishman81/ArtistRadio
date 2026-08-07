"""
ArtistRadio Engine
Audio Crossfade Apply Tests
"""

from src.audio.player import AudioPlayer



def test_player_can_apply_crossfade_volume():

    player = AudioPlayer()

    player.apply_volume(
        0.5
    )

    assert player.volume == 0.5