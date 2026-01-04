from tts.tts_service import synthesize

if __name__ == "__main__":
    output_path = synthesize("Hello, this is a test of the text to speech synthesis service.")
    print (f"testfile generated at: {output_path}")