from pathlib import Path
from .models import GeneratedClip
import subprocess


def mock_generate_clip_local(prompt_text, clip_length_sec, seed, run_id):
    """
    Creates a tiny 1-second black video using ffmpeg.
    This replaces the real SVD generator during tests.
    """

    out_dir = Path("data/broll_mock")
    out_dir.mkdir(parents=True, exist_ok=True)

    output_path = out_dir / f"mock_{run_id}_{seed}.mp4"

    # Generate a tiny black video (1 second, 1080x1920)
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=black:s=1080x1920:d=1",
        "-vf",
        "format=yuv420p",
        str(output_path),
    ]

    subprocess.run(cmd, check=True)

    return GeneratedClip(
        file_path=str(output_path),
        duration_sec=1.0,
        seed=seed,
        source="mock_svd",
    )
