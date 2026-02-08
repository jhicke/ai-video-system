from pathlib import Path
from pydub import AudioSegment
import logging

logger = logging.getLogger("ai_video_system.tts")


def clean_audio(path):
    audio = AudioSegment.from_wav(path)

    # trim silence
    trimmed_audio = audio.strip_silence(silence_len=100, silence_thresh=-40)

    # normalize volume
    normalized_audio = trimmed_audio.apply_gain(-trimmed_audio.max_dBFS)

    # Save the cleaned audio
    normalized_audio.export(path, format="wav")


def generate_speech(text, output_path):
    logger.info(f"Starting TTS for {len(text)} characters")

    raise NotImplementedError(
        "TTS speech generation not yet implemented. Choose a TTS provider."
    )


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
