# Presets DNB — miroir de DNB.txt à la racine du projet.
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExamSegment:
    name: str
    duration_minutes: int
    is_pause: bool = False


@dataclass(frozen=True)
class ExamPreset:
    name: str
    segments: tuple[ExamSegment, ...]


def _part(name: str, duration_minutes: int) -> ExamSegment:
    return ExamSegment(name=name, duration_minutes=duration_minutes, is_pause=False)


def _pause(duration_minutes: int) -> ExamSegment:
    return ExamSegment(name="Pause", duration_minutes=duration_minutes, is_pause=True)


BUILTIN_PRESETS: tuple[ExamPreset, ...] = (
    ExamPreset("Personnalisé", (_part("Partie 1", 60),)),
    ExamPreset(
        "Français DNB",
        (
            _part("Partie 1", 70),
            _part("Dictée", 20),
            _pause(15),
            _part("Partie 2", 90),
        ),
    ),
    ExamPreset("HGEMC DNB", (_part("Partie 1", 120),)),
    ExamPreset("Sciences DNB", (_part("Partie 1", 60),)),
    ExamPreset(
        "Maths DNB",
        (
            _part("Partie 1 (Calculatrice interdite)", 20),
            _part("Partie 2", 100),
        ),
    ),
)

PRESET_BY_NAME = {preset.name: preset for preset in BUILTIN_PRESETS}
CUSTOM_PRESET_NAME = BUILTIN_PRESETS[0].name

MAX_SEGMENTS = 10
