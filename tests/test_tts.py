from pathlib import Path
from tts.tts_service import synthesize


def test_tts_service(tmp_path: Path):
    test_file = tmp_path / "testfile.wav"
    if test_file.exists():
        test_file.unlink()

    test_text = "blah Hello, this is a test of the text to speech synthesis service."
    output_path = synthesize(test_text, test_file)
    print(f"testfile generated at: {str(output_path)}")
    assert output_path.exists(), "TTS output file was not created."
