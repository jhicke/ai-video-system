from pathlib import Path
from .models import GeneratedClip
from .svd_engine import generate_svd_video
from .config import TARGET_RESOLUTION, TARGET_FPS


def generate_clip_local(prompt_text, clip_length_sec, seed, run_id) -> GeneratedClip:
    out_dir = Path("data/broll_generated")
    out_dir.mkdir(parents=True, exist_ok=True)

    output_path = out_dir / f"{run_id}_{seed}.mp4"

    generate_svd_video(
        prompt=prompt_text,
        seconds=clip_length_sec,
        seed=seed,
        width=TARGET_RESOLUTION[0],
        height=TARGET_RESOLUTION[1],
        fps=TARGET_FPS,
        output_path=output_path,
    )

    return GeneratedClip(
        file_path=str(output_path),
        duration_sec=float(clip_length_sec),
        seed=seed,
        source="local_svd",
    )
