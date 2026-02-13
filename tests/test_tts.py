from pathlib import Path
from tts.tts_service import synthesize


def test_tts_service():
    test_file = Path("tests/assets/test_output.wav")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    if test_file.exists():
        test_file.unlink()

    test_text = "blah Hello, this is a test of the text to speech synthesis service. Listen to the sound of my voice and decide if it sounds bad. the Roman create the empire"
    output_path = synthesize(test_text, str(test_file))
    print(f"testfile generated at: {str(output_path)}")
    assert output_path.exists(), "TTS output file was not created."
