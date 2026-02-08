from pathlib import Path
from orchestrator.orchestrator import run_pipeline
from broll import clip_generator
from broll.mock_svd import mock_generate_clip_local
import pytest


class DummyLlamaClient:
    """
    Minimal mock for llama3.1:b used by the B-roll service.
    It returns a fixed JSON structure for visual anchors.
    """

    def generate(self, prompt: str) -> str:
        return """
        [
            {"text_span": "mysterious cat", "importance": 0.9, "position": 10},
            {"text_span": "shadowy alley", "importance": 0.7, "position": 50}
        ]
        """


def test_run_pipeline(tmp_path: Path, monkeypatch):
    # Patch SVD generator
    monkeypatch.setattr(clip_generator, "generate_clip_local", mock_generate_clip_local)

    # Patch llama client
    class DummyLlamaClient:
        def generate(self, prompt: str) -> str:
            return """
            [
                {"text_span": "mysterious cat", "importance": 0.9, "position": 10},
                {"text_span": "shadowy alley", "importance": 0.7, "position": 50}
            ]
            """

    from orchestrator import orchestrator

    monkeypatch.setattr(orchestrator, "llama_client", DummyLlamaClient())

    # Run pipeline
    project_root = Path(__file__).parent.parent
    topic = "The lore of cats and their mysterious ways."
    output_dir = tmp_path

    final_video_path = run_pipeline(
        topic=topic,
        project_root=project_root,
        output_dir=output_dir,
        video_filename="test_video.mp4",
    )

    assert final_video_path.exists()
