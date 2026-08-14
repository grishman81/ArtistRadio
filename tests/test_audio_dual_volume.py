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


def test_primary_volume_can_be_applied():

    player = AudioPlayer()

    player.apply_primary_volume(0.4)

    assert player.primary_volume == 0.4


def test_secondary_volume_can_be_applied():

    player = AudioPlayer()

    player.apply_secondary_volume(0.6)

    assert player.secondary_volume == 0.6


def test_primary_volume_is_clamped():

    player = AudioPlayer()

    player.apply_primary_volume(2.0)

    assert player.primary_volume == 1.0

    player.apply_primary_volume(-1.0)

    assert player.primary_volume == 0.0


def test_secondary_volume_is_clamped():

    player = AudioPlayer()

    player.apply_secondary_volume(2.0)

    assert player.secondary_volume == 1.0

    player.apply_secondary_volume(-1.0)

    assert player.secondary_volume == 0.0