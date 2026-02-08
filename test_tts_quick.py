#!/usr/bin/env python3
"""Quick TTS test script"""

from pathlib import Path
from tts.tts_service import synthesize

# Test text
test_text = "Hello, this is a test of the text to speech system. It should sound natural and clear."

# Output path
output_path = Path("assets/audio/test_output.wav")

print(f"Testing TTS...")
print(f"Text: {test_text}")
print(f"Output: {output_path}")

try:
    result = synthesize(test_text, output_path)
    print(f"✓ Success! Audio saved to {result}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback

    traceback.print_exc()
