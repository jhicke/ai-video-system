from pathlib import Path
from orchestrator.orchestrator import run_pipeline


def test_run_pipeline(tmp_path: Path):
    project_root = Path(__file__).parent.parent
    script = "I really love cats... They are playful, curious, and independent creatures that bring joy to my life. for example,  my cat loves to chase laser pointers and climb trees."
    output_dir = tmp_path
    video_filename = "test_video.mp4"

    final_video_path = run_pipeline(
        script,
        project_root,
        output_dir=output_dir,
        video_filename=video_filename,
    )

    assert final_video_path.exists(), "Final video file was not created."
    assert final_video_path.name == video_filename, "Video filename mismatch."
    assert final_video_path.parent == output_dir, "Output directory mismatch."
