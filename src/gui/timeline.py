from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Callable

from src.presets import (
    BUILTIN_PRESETS,
    CUSTOM_PRESET_NAME,
    MAX_SEGMENTS,
    PRESET_BY_NAME,
    ExamSegment,
)


@dataclass
class _TimelineRow:
    frame: ttk.Frame
    type_var: tk.StringVar
    name_var: tk.StringVar
    duration_var: tk.IntVar
    name_entry: ttk.Entry


class TimelineEditor:
    """Éditeur de la timeline d'épreuve (parties et pauses)."""

    def __init__(
        self,
        parent: ttk.Frame,
        *,
        on_changed: Callable[[], None],
        is_applying_preset: Callable[[], bool],
        safe_int: Callable[[tk.IntVar, int, int, int], int],
    ) -> None:
        self._on_changed = on_changed
        self._is_applying_preset = is_applying_preset
        self._safe_int = safe_int
        self.preset_var = tk.StringVar(value=CUSTOM_PRESET_NAME)
        self.start_hour_var = tk.IntVar(value=8)
        self.start_minute_var = tk.IntVar(value=0)
        self._rows: list[_TimelineRow] = []
        self._applying_preset = False

        self._build(parent)

    @property
    def applying_preset(self) -> bool:
        return self._applying_preset

    def set_applying_preset(self, value: bool) -> None:
        self._applying_preset = value

    def _build(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(1, weight=1)

        ttk.Label(parent, text="Preset", style="Panel.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=6)
        preset_combo = ttk.Combobox(
            parent,
            textvariable=self.preset_var,
            values=[preset.name for preset in BUILTIN_PRESETS],
            state="readonly",
            width=34,
        )
        preset_combo.grid(row=0, column=1, sticky="w", pady=6)
        preset_combo.bind("<<ComboboxSelected>>", self._on_preset_selected)

        ttk.Label(parent, text="Heure de début", style="Panel.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 12), pady=6
        )
        start_row = ttk.Frame(parent)
        start_row.grid(row=1, column=1, sticky="w", pady=6)
        ttk.Spinbox(start_row, from_=0, to=23, format="%02.0f", textvariable=self.start_hour_var, width=4, wrap=True).pack(
            side="left", padx=(0, 4)
        )
        ttk.Label(start_row, text=":", style="Card.TLabel").pack(side="left")
        ttk.Spinbox(
            start_row,
            from_=0,
            to=59,
            format="%02.0f",
            textvariable=self.start_minute_var,
            width=4,
            wrap=True,
        ).pack(side="left", padx=(4, 0))

        from src import theme

        ttk.Label(parent, text=theme.SECTION_TIMELINE, style="Section.TLabel").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(12, 8)
        )

        timeline_container = ttk.Frame(parent)
        timeline_container.grid(row=3, column=0, columnspan=2, sticky="ew")
        timeline_container.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            timeline_container,
            height=160,
            highlightthickness=1,
            highlightbackground=theme.COLOR_BORDER,
            bg=theme.COLOR_SURFACE,
        )
        timeline_scroll = ttk.Scrollbar(timeline_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=timeline_scroll.set)
        timeline_scroll.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="ew")

        self.inner = ttk.Frame(self.canvas)
        self._window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda _e: self._update_scroll_region())
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self._window_id, width=e.width))

        timeline_actions = ttk.Frame(parent)
        timeline_actions.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        ttk.Button(timeline_actions, text="+ Partie", command=self._add_part_row).pack(side="left")
        ttk.Button(timeline_actions, text="+ Pause", command=self._add_pause_row).pack(side="left", padx=(8, 0))

    def load_segments(self, segments: list[ExamSegment]) -> None:
        self._clear()
        for segment in segments:
            self._append_row(segment, notify=False)
        self._sync_row_states()
        self._update_scroll_region()

    def segments(self) -> list[ExamSegment]:
        result: list[ExamSegment] = []
        for row in self._rows:
            is_pause = row.type_var.get() == "Pause"
            name = "Pause" if is_pause else row.name_var.get().strip() or "Partie"
            duration = self._safe_int(row.duration_var, 1, 1440, 60)
            result.append(ExamSegment(name=name, duration_minutes=duration, is_pause=is_pause))
        return result

    def _on_preset_selected(self, _event: tk.Event[tk.Misc] | None = None) -> None:
        preset = PRESET_BY_NAME.get(self.preset_var.get())
        if preset is None:
            return
        self._applying_preset = True
        try:
            segments = [ExamSegment(s.name, s.duration_minutes, s.is_pause) for s in preset.segments]
            self.load_segments(segments)
        finally:
            self._applying_preset = False

    def _on_timeline_changed(self, *_args: object) -> None:
        if self._is_applying_preset() or self._applying_preset:
            return
        self.preset_var.set(CUSTOM_PRESET_NAME)
        self._sync_row_states()

    def _on_type_changed(self, *_args: object) -> None:
        self._sync_row_states()
        self._on_timeline_changed()

    def _sync_row_states(self) -> None:
        for row in self._rows:
            is_pause = row.type_var.get() == "Pause"
            if is_pause:
                row.name_var.set("Pause")
            row.name_entry.configure(state="disabled" if is_pause else "normal")

    def _clear(self) -> None:
        for row in self._rows:
            row.frame.destroy()
        self._rows.clear()

    def _append_row(self, segment: ExamSegment, notify: bool = True) -> None:
        if len(self._rows) >= MAX_SEGMENTS:
            return

        row_frame = ttk.Frame(self.inner)
        row_frame.pack(fill="x", pady=3)

        type_var = tk.StringVar(value="Pause" if segment.is_pause else "Partie")
        name_var = tk.StringVar(value=segment.name)
        duration_var = tk.IntVar(value=segment.duration_minutes)

        ttk.Combobox(
            row_frame,
            textvariable=type_var,
            values=("Partie", "Pause"),
            state="readonly",
            width=8,
        ).pack(side="left", padx=(0, 8))

        name_entry = ttk.Entry(row_frame, textvariable=name_var, width=16)
        name_entry.pack(side="left", padx=(0, 8))

        ttk.Spinbox(
            row_frame,
            from_=1,
            to=1440,
            increment=1,
            format="%02.0f",
            textvariable=duration_var,
            width=6,
        ).pack(side="left")
        ttk.Label(row_frame, text="min").pack(side="left", padx=(4, 8))

        ttk.Button(row_frame, text="^", width=3, command=lambda: self._move_row(row_frame, -1)).pack(side="left", padx=2)
        ttk.Button(row_frame, text="v", width=3, command=lambda: self._move_row(row_frame, 1)).pack(side="left", padx=2)
        ttk.Button(row_frame, text="x", width=3, command=lambda: self._remove_row(row_frame)).pack(side="left", padx=2)

        row = _TimelineRow(
            frame=row_frame,
            type_var=type_var,
            name_var=name_var,
            duration_var=duration_var,
            name_entry=name_entry,
        )
        self._rows.append(row)

        type_var.trace_add("write", self._on_type_changed)
        name_var.trace_add("write", self._on_timeline_changed)
        duration_var.trace_add("write", self._on_timeline_changed)

        if notify:
            self._on_timeline_changed()
        else:
            self._sync_row_states()

    def _row_index(self, row_frame: ttk.Frame) -> int | None:
        for index, row in enumerate(self._rows):
            if row.frame is row_frame:
                return index
        return None

    def _move_row(self, row_frame: ttk.Frame, direction: int) -> None:
        index = self._row_index(row_frame)
        if index is None:
            return
        new_index = index + direction
        if new_index < 0 or new_index >= len(self._rows):
            return
        items = self.segments()
        items[index], items[new_index] = items[new_index], items[index]
        self._applying_preset = True
        try:
            self.load_segments(items)
        finally:
            self._applying_preset = False
        self.preset_var.set(CUSTOM_PRESET_NAME)

    def _remove_row(self, row_frame: ttk.Frame) -> None:
        index = self._row_index(row_frame)
        if index is None:
            return
        items = self.segments()
        if len(items) <= 1:
            return
        part_count = sum(1 for segment in items if not segment.is_pause)
        if not items[index].is_pause and part_count <= 1:
            return
        del items[index]
        self._applying_preset = True
        try:
            self.load_segments(items)
        finally:
            self._applying_preset = False
        self.preset_var.set(CUSTOM_PRESET_NAME)

    def _add_part_row(self) -> None:
        if len(self._rows) >= MAX_SEGMENTS:
            return
        part_index = sum(1 for row in self._rows if row.type_var.get() == "Partie") + 1
        self._append_row(ExamSegment(f"Partie {part_index}", 60))

    def _add_pause_row(self) -> None:
        if len(self._rows) >= MAX_SEGMENTS:
            return
        self._append_row(ExamSegment("Pause", 15, is_pause=True))

    def _update_scroll_region(self) -> None:
        self.inner.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
