from pathlib import Path
from orchestrator.orchestrator import run_pipeline


def test_run_pipeline(tmp_path: Path):
    project_root = Path(__file__).parent.parent
    topic = "The lore of cats and their mysterious ways."
    style = "default"
    temperature = 0.2
    output_dir = tmp_path
    video_filename = "test_video.mp4"

    final_video_path = run_pipeline(
        topic=topic,
        project_root=project_root,
        style=style,
        temperature=temperature,
        output_dir=output_dir,
        video_filename=video_filename,
    )

    assert final_video_path.exists(), "Final video file was not created."
    assert final_video_path.name == video_filename, "Video filename mismatch."
    assert final_video_path.parent == output_dir, "Output directory mismatch."
