from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from src.presets import ExamSegment


@dataclass
class ClockConfig:
    bg_color: str = "#000000"
    text_color: str = "#FFFFFF"
    start_label_color: str = "#4FC3F7"
    end_label_color: str = "#FFB74D"
    font_family: str = "DejaVu Sans"
    font_size: int = 300
    show_seconds: bool = False
    show_exam_labels: bool = True
    start_hour: int = 8
    start_minute: int = 0
    segments: list[ExamSegment] = field(default_factory=lambda: [ExamSegment("Partie 1", 60)])


@dataclass(frozen=True)
class ScheduledSegment:
    name: str
    start: datetime
    end: datetime
    is_pause: bool


@dataclass(frozen=True)
class ExamSchedule:
    general_start: datetime
    general_end: datetime
    segments: tuple[ScheduledSegment, ...]
    last_part_start: datetime
    departure_authorized: datetime


@dataclass(frozen=True)
class ExamDisplayState:
    show_current_part_end: bool
    current_part_end: datetime | None
    current_part_name: str | None
