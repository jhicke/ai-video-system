# services/broll/models.py

from dataclasses import dataclass
from typing import Any


@dataclass
class VisualAnchor:
    text_span: str
    importance: float
    position: int


@dataclass
class BrollPrompt:
    anchor: VisualAnchor
    prompt_text: str
    style_preset: str


@dataclass
class BrollClip:
    id: str
    prompt: str
    source: str
    file_path: str
    duration_sec: float
    seed: int
    style_preset: str


@dataclass
class BrollResult:
    clips: list[BrollClip]
    metadata: dict[str, Any]


@dataclass
class CachedClip:
    file_path: str
    duration_sec: float
    seed: int
    style_preset: str
    resolution: tuple[int, int]
    fps: int


@dataclass
class GeneratedClip:
    file_path: str
    duration_sec: float
    seed: int
    source: str
