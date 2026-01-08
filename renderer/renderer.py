import subprocess
from pathlib import Path
import logging
from typing import List

logger = logging.getLogger("ai_video_system.renderer")


def _concat_broll_clips(broll_clips: List, temp_dir: Path) -> Path:
    """
    Concatenate B-roll clips into a single temporary video file.
    """
    temp_dir.mkdir(parents=True, exist_ok=True)
    list_file = temp_dir / "broll_list.txt"

    # Write ffmpeg concat list
    with open(list_file, "w") as f:
        for clip in broll_clips:
            f.write(f"file '{clip.file_path}'\n")

    output_path = temp_dir / "broll_concat.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-c",
        "copy",
        str(output_path),
    ]

    logger.info(f"Concatenating {len(broll_clips)} B-roll clips...")
    subprocess.run(cmd, check=True)

    return output_path


def render_video(
    audio_path: Path,
    broll_clips: List,
    output_path: Path,
    resolution: str = "1080x1920",
    fps: int = 30,
) -> Path:
    """
    Render final video by combining:
    - concatenated B-roll clips
    - narration audio
    """

    # input validation
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not isinstance(output_path, Path):
        raise TypeError("output_path must be a Path object")
    if resolution.count("x") != 1:
        raise ValueError("Resolution must be WIDTHxHEIGHT")
    if fps <= 0:
        raise ValueError("FPS must be positive")

    if not broll_clips:
        raise ValueError("No B-roll clips provided to renderer")

    # Step 1: Concatenate B-roll clips
    temp_dir = output_path.parent / "_temp_renderer"
    concat_path = _concat_broll_clips(broll_clips, temp_dir)

    # Step 2: Combine B-roll + audio
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(concat_path),
        "-i",
        str(audio_path),
        "-vf",
        f"scale={resolution}",
        "-r",
        str(fps),
        "-shortest",
        str(output_path),
    ]

    logger.info("Rendering final video with audio + B-roll...")
    subprocess.run(cmd, check=True)

    return output_path
