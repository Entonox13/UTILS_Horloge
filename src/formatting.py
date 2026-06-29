from __future__ import annotations

from datetime import datetime


def format_time_hm(value: datetime) -> str:
    """Formate une heure en HH:MM (minutes sur deux chiffres)."""
    return value.strftime("%H:%M")
