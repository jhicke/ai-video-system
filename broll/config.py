# services/broll/config.py

STYLE_PRESETS = {
    "default": {
        "base_suffix": (
            "cinematic, 4k, high quality, smooth camera motion, soft lighting, "
            "no text, no subtitles, no UI, no watermarks"
        ),
        "color_palette": "neon blues and purples",
        "motion_style": "slow smooth pan",
    },
}

DEFAULT_PRESET = "default"
DEFAULT_CLIP_LENGTH_SEC = 4
DEFAULT_MAX_CLIPS = 6

TARGET_RESOLUTION = (1080, 1920)
TARGET_FPS = 30
