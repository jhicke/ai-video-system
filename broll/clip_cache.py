# services/broll/clip_cache.py

import json
import hashlib
from pathlib import Path
from .models import CachedClip
from .config import TARGET_RESOLUTION, TARGET_FPS

CACHE_ROOT = Path("data/broll_cache")
INDEX_PATH = CACHE_ROOT / "index.json"


def _hash_key(prompt_text: str, style: str, length: int, model_version: str) -> str:
    key = f"{prompt_text}|{style}|{length}|{model_version}".encode("utf-8")
    return hashlib.sha256(key).hexdigest()[:16]


def _load_index() -> dict:
    if not INDEX_PATH.exists():
        return {}
    return json.loads(INDEX_PATH.read_text())


def _save_index(index: dict):
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, indent=2))


def lookup_cached_clip(
    prompt, clip_length_sec: int, model_version: str
) -> CachedClip | None:
    index = _load_index()
    key = _hash_key(
        prompt.prompt_text, prompt.style_preset, clip_length_sec, model_version
    )
    entry = index.get(key)
    if not entry:
        return None

    return CachedClip(
        file_path=entry["file_path"],
        duration_sec=entry["duration_sec"],
        seed=entry["seed"],
        style_preset=entry["style_preset"],
        resolution=tuple(entry["resolution"]),
        fps=entry["fps"],
    )


def save_clip_to_cache(
    prompt, seed, file_path, duration_sec, clip_length_sec, model_version
):
    index = _load_index()
    key = _hash_key(
        prompt.prompt_text, prompt.style_preset, clip_length_sec, model_version
    )

    index[key] = {
        "file_path": file_path,
        "duration_sec": duration_sec,
        "seed": seed,
        "style_preset": prompt.style_preset,
        "resolution": TARGET_RESOLUTION,
        "fps": TARGET_FPS,
        "model_version": model_version,
    }

    _save_index(index)
