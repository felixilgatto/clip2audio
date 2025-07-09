import os
from pathlib import Path


DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "./downloads"))
AUDIO_DIR = Path(os.getenv("AUDIO_DIR", "./audios"))
TMP_DIR = Path(os.getenv("TMP_DIR", "./tmp"))
AUDIO_FORMAT = os.getenv("AUDIO_FORMAT", "m4a")
DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "INFO").upper()
