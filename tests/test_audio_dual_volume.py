"""
ArtistRadio Engine
Dual Volume Control Tests
"""


from src.audio.player import AudioPlayer



def test_primary_volume_exists():

    player = AudioPlayer()

    player.primary_volume = 1.0

    assert player.primary_volume == 1.0



def test_secondary_volume_exists():

    player = AudioPlayer()

    player.secondary_volume = 0.0

    assert player.secondary_volume == 0.0