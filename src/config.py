"""
ArtistRadio Engine
Configuration
"""

from pathlib import Path

# Корень проекта
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Папка с музыкой (пока используем тестовую библиотеку)
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
