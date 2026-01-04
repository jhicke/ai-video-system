from tts.tts_service import synthesize

if __name__ == "__main__":
    test_text = "Hello, this is a test of the text to speech synthesis service."
    output_path = synthesize(test_text, outputFileName="testfile.wav")
    print (f"testfile generated at: {output_path}")