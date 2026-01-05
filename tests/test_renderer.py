from renderer.renderer import render_video
from pathlib import Path


def test_renderer(tmp_path):
    project_root = Path(__file__).parent.parent  # gets the project root directory

    # clean up previous output
    output = tmp_path / "test.mp4"
    if output.exists():
        output.unlink()

    resolution = "1080x1920"
    fps = 30
    background = str(
        project_root / "assets" / "video" / "background.mp4"
    )  # Always points to project/assets/
    audio = str(project_root / "assets" / "audio" / "voice.wav")

    output_path = render_video(
        audio_path=Path(audio),
        background_path=Path(background),
        output_path=Path(output),
        resolution=resolution,
        fps=fps,
    )
    print("Renderer test complete:", output_path)
    assert output_path.exists(), "Rendered video file was not created."
