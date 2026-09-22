"""
ArtistRadio Engine
Configuration
"""

from pathlib import Path


# Корень проекта

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Папка с музыкой

MUSIC_ROOT = Path(r"D:\TestLibrary")


# Рабочие папки проекта

DATABASE_FOLDER = PROJECT_ROOT / "database"
CACHE_FOLDER = PROJECT_ROOT / "cache"
LOG_FOLDER = PROJECT_ROOT / "logs"


# Поддерживаемые аудиоформаты

SUPPORTED_FORMATS = {
    ".mp3",
    ".flac",
    ".m4a",
    ".wav",
    ".ape",
    ".ogg",
    ".aac",
}


# Настройки радиостанции

STATION_NAME = "ArtistRadio"

DEFAULT_ARTIST = "Jennifer Lopez"

BITRATE = 320

HISTORY_LIMIT = 100


# Локальный аудиовыход. Оставьте пустым для системного устройства по умолчанию.
AUDIO_DEVICE = ""


# Icecast streaming. Включается после настройки виртуального аудиокабеля.
STREAM_ENABLED = False
STREAM_AUDIO_DEVICE = "CABLE Output (VB-Audio Virtual Cable)"
ICECAST_HOST = "127.0.0.1"
ICECAST_PORT = 8000
ICECAST_MOUNT = "/artist-radio.mp3"
ICECAST_PASSWORD = "hackme"
ICECAST_NAME = STATION_NAME
ICECAST_GENRE = "Various"
STREAM_SAMPLE_RATE = 44100
STREAM_CHANNELS = 2