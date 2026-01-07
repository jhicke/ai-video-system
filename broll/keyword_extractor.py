# services/broll/keyword_extractor.py

import json
from .models import VisualAnchor


def _anchor_prompt(script: str, max_candidates: int) -> str:
    return f"""
Extract at most {max_candidates} short, visual concepts from the script.
Focus on concrete, visualizable ideas. Return JSON only.

Each item:
- text_span: short phrase
- importance: 0-1
- position: character index

Script:
\"\"\"{script}\"\"\"
""".strip()


def extract_visual_anchors(
    script: str, max_candidates: int, llama_client
) -> list[VisualAnchor]:
    prompt = _anchor_prompt(script, max_candidates)
    raw = llama_client.generate(prompt)
    data = json.loads(raw)

    anchors = [
        VisualAnchor(
            text_span=item["text_span"].strip(),
            importance=float(item.get("importance", 0.5)),
            position=int(item.get("position", 0)),
        )
        for item in data
    ]

    anchors.sort(key=lambda a: (-a.importance, a.position))
    return anchors[:max_candidates]
