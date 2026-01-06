import json
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger("ai_video_system.renderer")


def load_template(path="template.json"):
    with open(path, "r") as f:
        return json.load(f)


def render_video(
    audio_path: Path,  # audio file path
    background_path: Path,  # background video file path
    output_path: Path,  # output video file path
    resolution: str = "1080x1920",
    fps: int = 30,
) -> Path:
    # input validation
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not background_path.exists():
        raise FileNotFoundError(f"Background video file not found: {background_path}")
    if not isinstance(output_path, Path):
        raise TypeError("output_path must be a Path object")
    if resolution.count("x") != 1:
        raise ValueError("Resolution must be in the format WIDTHxHEIGHT")
    if fps <= 0:
        raise ValueError("FPS must be a positive integer")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(background_path),
        "-i",
        str(audio_path),
        "-vf",
        f"scale={resolution}",
        "-r",
        str(fps),
        "-shortest",
        str(output_path),
    ]

    subprocess.run(cmd, check=True)

    return output_path
