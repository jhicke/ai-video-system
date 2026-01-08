from pathlib import Path
from script_generator.script_generator import generate_script
from tts.tts_service import synthesize
from renderer.renderer import render_video
from logging_config import setup_logging
from broll.broll_service import generate_broll
import time

logger = setup_logging()


def run_pipeline(
    topic: str,
    project_root: Path,
    *,
    style: str = "default",
    temperature: float = 0.2,
    output_dir: Path | None = None,
    video_filename: str = "final_video.mp4",
) -> Path:
    """
    Orchestrates the full pipeline:
    1. Generate script
    2. Generate TTS audio
    3. Generate B-roll clips
    4. Render final video
    """
    logger.info("Pipeline started")

    # input validation
    if not isinstance(project_root, Path):
        raise TypeError("project_root must be a Path object")
    if not isinstance(topic, str):
        raise TypeError("topic must be a string")
    if style is not None and not isinstance(style, str):
        raise TypeError("style must be a string or None")
    if temperature is not None and not isinstance(temperature, (float, int)):
        raise TypeError("temperature must be a float or int")
    if output_dir is not None and not isinstance(output_dir, Path):
        raise TypeError("output_dir must be a Path object or None")
    if not isinstance(video_filename, str):
        raise TypeError("video_filename must be a string")
    if not video_filename.lower().endswith(".mp4"):
        raise ValueError("video_filename must end with .mp4")

    # Step 1: Generate script
    start = time.time()
    script = generate_script(topic=topic, style=style, temperature=temperature)
    logger.info(f"Script generated in {time.time() - start:.2f}s")
    if not script.strip():
        raise RuntimeError("Script generator returned empty output")

    # Step 2: Generate TTS audio
    start = time.time()
    logger.info("Running TTS...")

    tts_output_path = synthesize(
        script, project_root / "assets" / "voice" / "pipeline_voice.wav"
    )

    if not tts_output_path.exists():
        raise RuntimeError(f"TTS output file not found: {tts_output_path}")
    if not isinstance(tts_output_path, Path):
        raise TypeError("TTS microservice returned a non-Path output")

    logger.info(f"TTS complete: {tts_output_path}")
    logger.info(f"TTS completed in {time.time() - start:.2f}s")

    # Step 3: Generate B-roll
    logger.info("Generating B-roll clips...")
    start = time.time()

    # run_id = something unique per pipeline run
    run_id = f"{int(time.time())}"

    broll_result = generate_broll(
        script=script,
        style_preset=style,
        max_clips=6,
        clip_length_sec=4,
        run_id=run_id,
        batch_id=None,
        llama_client=None,  # plug in your llama client if needed
    )

    logger.info(f"B-roll generation completed in {time.time() - start:.2f}s")
    logger.info(f"Generated {len(broll_result.clips)} B-roll clips")

    # Step 4: Render video
    logger.info("Rendering video...")
    start = time.time()

    if output_dir is None:
        output_dir = project_root / "assets" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / video_filename

    rendered_video_path = render_video(
        audio_path=tts_output_path,
        broll_clips=broll_result.clips,
        output_path=output_path,
    )

    if not rendered_video_path.exists():
        raise RuntimeError(f"Rendered video file not found: {rendered_video_path}")
    if not isinstance(rendered_video_path, Path):
        raise TypeError("Renderer microservice returned a non-Path output")

    logger.info(f"Render complete: {rendered_video_path}")
    logger.info(f"Rendering completed in {time.time() - start:.2f}s")

    logger.info(f"Pipeline finished. Final video: {rendered_video_path}")

    return rendered_video_path
