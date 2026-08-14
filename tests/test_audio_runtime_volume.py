from src.audio.player import AudioPlayer


def test_primary_volume_is_clamped():

    player = AudioPlayer()

    player.apply_primary_volume(0.5)

    assert player.primary_volume == 0.5

    player.apply_primary_volume(2.0)

    assert player.primary_volume == 1.0

    player.apply_primary_volume(-1.0)

    assert player.primary_volume == 0.0


def test_secondary_volume_is_clamped():

    player = AudioPlayer()

    player.apply_secondary_volume(0.5)

    assert player.secondary_volume == 0.5

    player.apply_secondary_volume(2.0)

    assert player.secondary_volume == 1.0

    player.apply_secondary_volume(-1.0)

    assert player.secondary_volume == 0.0
