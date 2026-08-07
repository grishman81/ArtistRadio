"""
ArtistRadio Engine
Dual Playback Tests
"""

from pathlib import Path

from src.audio.player import AudioPlayer



def test_player_can_hold_secondary_track():

    player = AudioPlayer()

    path = Path(
        "next_song.mp3"
    )

    player.secondary = path

    assert player.secondary == path



def test_player_secondary_starts_empty():

    player = AudioPlayer()

    assert player.secondary is None