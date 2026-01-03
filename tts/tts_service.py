from TTS.api import TTS
from pathlib import Path
from pydub import AudioSegment

def clean_audio(path):
    audio = AudioSegment.from_wav(path)

    # trim silence

    trimmed_audio = audio.strip_silence(silence_len=100, silence_thresh=-40)

    # nomralize volume
    normalized_audio = trimmed_audio.apply_gain(-trimmed_audio.max_dBFS)

    # Save the cleaned audio
    normalized_audio.export(path, format="wav")

def generate_speech(text, output_path="../assets/voice.wav"):
    # load default TTS model
    voiceModels= ["tts_models/en/ljspeech/tacotron2-DDC",
                  "tts_models/en/vctk/vits",
                  "tts_models/en/ljspeech/glow-tts",
                  "tts_models/multilingual/multi-dataset/your_tts"]
    
    speaker ="p340"  # Example speaker for vctk model

    tts = TTS(voiceModels[1], gpu=True)  # You can choose any model from the list

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # generate speech
    tts.tts_to_file(text=text, file_path=str(output_path),speaker=speaker)
    clean_audio(output_path)

    print(f"Speech generated successfully: {output_path}")


if __name__ == "__main__":
    sample_test="Hello, this is a test of the text to speech generation."
    generate_speech(sample_test)