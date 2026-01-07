# services/broll/clip_generator.py

import subprocess
import uuid
from pathlib import Path
from .models import GeneratedClip
from .config import TARGET_RESOLUTION, TARGET_FPS


def _run_svd(prompt, seconds, seed, run_id, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{run_id}_{uuid.uuid4().hex[:8]}.mp4"

    cmd = [
        "python",
        "svd_generate.py",
        "--prompt",
        prompt,
        "--seconds",
        str(seconds),
        "--seed",
        str(seed),
        "--width",
        str(TARGET_RESOLUTION[0]),
        "--height",
        str(TARGET_RESOLUTION[1]),
        "--fps",
        str(TARGET_FPS),
        "--output",
        str(out_path),
    ]

    subprocess.run(cmd, check=True)
    return out_path


def generate_clip_local(prompt_text, clip_length_sec, seed, run_id) -> GeneratedClip:
    out_dir = Path("data/broll_generated")
    out_path = _run_svd(prompt_text, clip_length_sec, seed, run_id, out_dir)

    return GeneratedClip(
        file_path=str(out_path),
        duration_sec=float(clip_length_sec),
        seed=seed,
        source="local_model",
    )
