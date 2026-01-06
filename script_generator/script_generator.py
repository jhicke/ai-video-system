from __future__ import annotations

import logging
import textwrap
from typing import Literal

import requests

logger = logging.getLogger("ai_video_system.script_generator")

# model + endpoint config for Ollama

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma2:9b"  # can switch the llama3.1:8b if needed


def _build_prompt(topic: str, style) -> str:
    prompt = f"""
    You are a professional short-form video scriptwriter.

    Write a concise, engaging script for a vertical video about:
    "{topic}"

    Style: {style}

    Requirements:
    - 80 to 140 words.
    - Strong hook in the first 1-2 sentences.
    - Conversational, human, natural tone.
    - 3-5 flowing ideas or beats.
    - No lists, no bullet points.
    - No emojis.
    - No hashtags.
    - No scene numbers or timestamps.
    - Output a single block of text ready for TTS.

    Output ONLY the script text. Do not label sections.
    """

    return textwrap.dedent(prompt).strip()


def _call_ollama(
    prompt: str, *, model: str = MODEL_NAME, temperature: float = 0.7
) -> str:
    """
    Call the local Ollama server and return the generated text.
    """
    logger.info(f"Calling Ollama model='{model}'")

    payload = {
        "model": model,
        "prompt": prompt,
        "options": {
            "temperature": temperature,
        },
        "stream": False,
    }

    response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    text = data.get("response", "").strip()
    if not text:
        raise RuntimeError("LLM returned empty response")

    logger.info(f"Received {len(text)} characters from Gemma 2 9B")
    return text


def generate_script(
    topic: str,
    *,
    style: Literal["default", "educational", "funny", "dramatic"] = "default",
    temperature: float = 0.7,
) -> str:
    if not topic or not topic.strip():
        raise ValueError("Topic must be a non-empty string")

    topic = topic.strip()
    logger.info(f"Generating script for topic='{topic}' style='{style}'")

    prompt = _build_prompt(topic, style)
    script = _call_ollama(prompt, model=MODEL_NAME, temperature=temperature)
    return script
