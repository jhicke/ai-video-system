from tts.tts_service import synthesize


def test_tts_service():
    test_text = "blah Hello, this is a test of the text to speech synthesis service."
    output_path = synthesize(test_text, "testfile.wav")
    print(f"testfile generated at: {str(output_path)}")
    assert output_path.exists(), "TTS output file was not created."
