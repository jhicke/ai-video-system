import json
import subprocess
from pathlib import Path


def load_template(path="template.json"):
    with open(path, "r") as f:
        return json.load(f)


def render_video(
    audio_path: Path,  # audio file path
    background_path: Path,  # background video file path
    output_path: Path,  # output video file path
    resolution: str = "1080x1920",
    fps: int = 30,
):

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
