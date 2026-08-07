"""
ArtistRadio Engine
Audio Fade Transition Tests
"""


from src.audio.player import AudioPlayer



def test_fade_out_reduces_volume():

    player = AudioPlayer()

    player.volume = 1.0

    player.fade_out(
        steps=5
    )

    assert player.volume == 0.0



def test_fade_in_restores_volume():

    player = AudioPlayer()

    player.volume = 0.0

    player.fade_in(
        steps=5
    )

    assert player.volume == 1.0