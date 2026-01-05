from renderer.renderer import render_video
from pathlib import Path
from tts.tts_service import synthesize

project_root = Path(__file__).parent.parent


def test_pipeline():

    # cleanup previous outputs
    print("cleanup previous outputs")
    files_to_delete = [
        project_root / "assets" / "output" / "integration_test.mp4",
        project_root / "assets" / "testFile.wav",
    ]

    for f in files_to_delete:
        if f.exists():
            f.unlink()

    # generate TTS
    print("generate TTS")
    test_text = "Hello, this is a test of the full video synthesis pipeline."
    tts_output_path = synthesize(test_text, "pipeline_test.wav")
    print(f"TTS synthesis complete: {tts_output_path}")

    # render video
    print("render video")
    background_path = project_root / "assets" / "video" / "background.mp4"
    output_path = project_root / "assets" / "output" / "integration_test.mp4"

    rendered_video_path = render_video(
        audio_path=tts_output_path,
        background_path=background_path,
        output_path=output_path,
    )
    print("assertion checks")
    assert rendered_video_path.exists(), "Rendered video file was not created."

    return rendered_video_path


if __name__ == "__main__":
    print("Starting full pipeline test...")
    test_output = test_pipeline()
    print("Full pipeline test complete:", test_output)
