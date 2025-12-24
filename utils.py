
from pathlib import Path

def is_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def cleanup(path):
    try:
        Path(path).unlink()
    except:
        pass
