from .keyword_extractor import extract_visual_anchors
from .prompt_generator import build_prompts
from .clip_cache import lookup_cached_clip, save_clip_to_cache
from .clip_generator import generate_clip_local
from .models import BrollClip, BrollResult
from .config import DEFAULT_PRESET, DEFAULT_CLIP_LENGTH_SEC, DEFAULT_MAX_CLIPS
from .utils import deterministic_seed

MODEL_VERSION = "svd_local_v1"


def generate_broll(
    script: str,
    style_preset: str | None,
    max_clips: int | None,
    clip_length_sec: int | None,
    run_id: str,
    batch_id: str | None = None,
    llama_client=None,
) -> BrollResult:

    style_preset = style_preset or DEFAULT_PRESET
    max_clips = max_clips or DEFAULT_MAX_CLIPS
    clip_length_sec = clip_length_sec or DEFAULT_CLIP_LENGTH_SEC

    anchors = extract_visual_anchors(
        script,
        max_candidates=max_clips * 2,
        llama_client=llama_client,
    )

    prompts = build_prompts(
        anchors,
        style_preset=style_preset,
        max_clips=max_clips,
    )

    clips: list[BrollClip] = []

    for idx, prompt in enumerate(prompts):
        seed = deterministic_seed(run_id, idx, prompt.prompt_text)

        cached = lookup_cached_clip(
            prompt,
            clip_length_sec,
            model_version=MODEL_VERSION,
        )

        if cached:
            clips.append(
                BrollClip(
                    id=f"broll_{idx:03}",
                    prompt=prompt.prompt_text,
                    source="cache",
                    file_path=cached.file_path,
                    duration_sec=cached.duration_sec,
                    seed=cached.seed,
                    style_preset=cached.style_preset,
                )
            )
            continue

        generated = generate_clip_local(
            prompt.prompt_text,
            clip_length_sec,
            seed,
            run_id,
        )

        save_clip_to_cache(
            prompt,
            seed=seed,
            file_path=generated.file_path,
            duration_sec=generated.duration_sec,
            clip_length_sec=clip_length_sec,
            model_version=MODEL_VERSION,
        )

        clips.append(
            BrollClip(
                id=f"broll_{idx:03}",
                prompt=prompt.prompt_text,
                source=generated.source,
                file_path=generated.file_path,
                duration_sec=generated.duration_sec,
                seed=seed,
                style_preset=style_preset,
            )
        )

    return BrollResult(
        clips=clips,
        metadata={
            "style_preset": style_preset,
            "run_id": run_id,
            "batch_id": batch_id,
            "model_version": MODEL_VERSION,
            "num_clips": len(clips),
        },
    )
