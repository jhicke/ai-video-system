from pathlib import Path
import torch
from diffusers import StableVideoDiffusionPipeline
import imageio

_pipe = None


def load_svd_model(model_path: str = "svd_xt"):
    global _pipe
    if _pipe is None:
        _pipe = StableVideoDiffusionPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
        ).to("cuda")
    return _pipe


def generate_svd_video(
    prompt: str,
    seconds: int,
    seed: int,
    width: int,
    height: int,
    fps: int,
    output_path: Path,
) -> Path:

    pipe = load_svd_model()

    torch.manual_seed(seed)

    # SVD is img2vid → needs an initial conditioning image
    init_image = torch.zeros((1, 3, height, width), dtype=torch.float16, device="cuda")

    num_frames = seconds * fps

    result = pipe(
        prompt=prompt,
        image=init_image,
        num_frames=num_frames,
    )

    frames = result.frames[0]

    writer = imageio.get_writer(str(output_path), fps=fps)
    for frame in frames:
        writer.append_data(frame)
    writer.close()

    return output_path
