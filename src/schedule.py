from __future__ import annotations

from datetime import datetime, timedelta

from src.constants import DEPARTURE_OFFSET, TIERS_TEMPS_FACTOR
from src.models import ClockConfig, ExamDisplayState, ExamSchedule, ScheduledSegment
from src.presets import ExamSegment


def _reference_datetime(hour: int, minute: int) -> datetime:
    return datetime(2000, 1, 1, hour, minute)


def effective_duration_minutes(segment: ExamSegment, *, tiers_temps: bool) -> int:
    if tiers_temps and not segment.is_pause:
        return round(segment.duration_minutes * TIERS_TEMPS_FACTOR)
    return segment.duration_minutes


def build_exam_schedule(config: ClockConfig) -> ExamSchedule:
    current = _reference_datetime(config.start_hour, config.start_minute)
    general_start = current
    scheduled: list[ScheduledSegment] = []
    part_segments: list[ScheduledSegment] = []

    for segment in config.segments:
        duration = effective_duration_minutes(segment, tiers_temps=config.tiers_temps)
        end = current + timedelta(minutes=duration)
        scheduled_segment = ScheduledSegment(
            name=segment.name,
            start=current,
            end=end,
            is_pause=segment.is_pause,
        )
        scheduled.append(scheduled_segment)
        if not segment.is_pause:
            part_segments.append(scheduled_segment)
        current = end

    if not part_segments:
        fallback = ScheduledSegment(name="Partie 1", start=general_start, end=general_start, is_pause=False)
        scheduled = [fallback]
        part_segments = [fallback]

    last_part = part_segments[-1]
    return ExamSchedule(
        general_start=general_start,
        general_end=last_part.end,
        segments=tuple(scheduled),
        last_part_start=last_part.start,
        departure_authorized=last_part.start + DEPARTURE_OFFSET,
    )


def build_exam_display_state(now: datetime, schedule: ExamSchedule) -> ExamDisplayState:
    for index, segment in enumerate(schedule.segments):
        if segment.start <= now < segment.end and index < len(schedule.segments) - 1:
            return ExamDisplayState(
                show_current_part_end=True,
                current_part_end=segment.end,
                current_part_name=segment.name,
            )
    return ExamDisplayState(show_current_part_end=False, current_part_end=None, current_part_name=None)


def exam_now() -> datetime:
    """Heure courante normalisée sur une journée fictive (calcul des horaires d'épreuve)."""
    return datetime.now().replace(year=2000, month=1, day=1, microsecond=0)
