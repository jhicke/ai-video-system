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


def generate_speech(text, output_path):
    # load default TTS model
    voiceModels = [
        "tts_models/en/ljspeech/tacotron2-DDC",
        "tts_models/en/vctk/vits",
        "tts_models/en/ljspeech/glow-tts",
        "tts_models/multilingual/multi-dataset/your_tts",
    ]

    speaker = "p340"  # Example speaker for vctk model

    tts = TTS(voiceModels[1], gpu=True)  # You can choose any model from the list

    # generate speech
    tts.tts_to_file(text=text, file_path=str(output_path), speaker=speaker)
    clean_audio(output_path)

    print(f"Speech generated successfully: {output_path}")


def synthesize(text, output_path) -> Path:
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    if text.strip() == "":
        raise ValueError("Input text for TTS synthesis is empty.")

    if not isinstance(output_path, Path):
        output_path = Path(output_path)

    # returns path relative to project root
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_speech(text, output_path)
    return output_path
