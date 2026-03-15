from pathlib import Path


def ensure_storage_dirs(upload_root: str) -> None:
    root = Path(upload_root)
    for folder in ['videos', 'thumbs', 'avatars', 'extras', 'bonus']:
        (root / folder).mkdir(parents=True, exist_ok=True)
