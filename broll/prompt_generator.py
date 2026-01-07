# services/broll/prompt_generator.py

from .models import VisualAnchor, BrollPrompt
from .config import STYLE_PRESETS, DEFAULT_PRESET


def _normalize(anchor: VisualAnchor) -> str:
    return anchor.text_span.strip()


def build_prompts(
    anchors: list[VisualAnchor],
    style_preset: str,
    max_clips: int,
) -> list[BrollPrompt]:

    preset_name = style_preset if style_preset in STYLE_PRESETS else DEFAULT_PRESET
    preset = STYLE_PRESETS[preset_name]

    prompts = []

    for anchor in anchors[:max_clips]:
        base = _normalize(anchor)

        prompt_text = (
            f"{base}, {preset['base_suffix']}, "
            f"color palette {preset['color_palette']}, "
            f"{preset['motion_style']}"
        )

        prompts.append(
            BrollPrompt(
                anchor=anchor,
                prompt_text=prompt_text,
                style_preset=preset_name,
            )
        )

    return prompts
