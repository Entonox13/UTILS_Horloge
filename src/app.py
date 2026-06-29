from __future__ import annotations

import time
import tkinter as tk
from tkinter import ttk

from src.presets import CUSTOM_PRESET_NAME
from src import theme
from src.gui.clock_view import ClockView
from src.gui.config_view import ConfigView
from src.models import ClockConfig
from src.schedule import build_exam_display_state, build_exam_schedule, exam_now


class ClockApplication:
    """Application principale : configuration et affichage plein écran."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        theme.setup_root_scaling(self.root)
        theme.apply_theme(ttk.Style(), root=self.root)
        theme.fit_window_to_screen(self.root, 820, 720)

        self.config = ClockConfig()
        self._clock_job: str | None = None
        self._fullscreen = False

        default_font = theme.resolve_clock_font(self.config.font_family, self.root)
        self.config.font_family = default_font

        self._container = ttk.Frame(self.root)
        self._container.pack(fill="both", expand=True)

        self._config_view = ConfigView(
            self.root,
            self._container,
            self.config,
            theme.discover_clock_fonts(self.root),
        )
        self._config_view.font_var.set(default_font)
        self._config_view.build()
        self._config_view.on_launch(self._launch_clock)
        self._config_view.on_quit(self.root.destroy)
        self._config_view.wire_timeline_callbacks(self._on_timeline_changed)
        self._config_view.load_timeline(self.config.segments)

        self._clock_view = ClockView(self.root)

        self._show_config()
        self.root.bind("<Escape>", self._on_escape)

    def _on_timeline_changed(self) -> None:
        if self._config_view.timeline.applying_preset:
            return
        self._config_view.timeline.preset_var.set(CUSTOM_PRESET_NAME)

    def _resolve_font(self, family: str) -> str:
        return theme.resolve_clock_font(family, self.root)

    def _apply_config(self) -> None:
        self.config = self._config_view.read_config(resolve_font=self._resolve_font)
        self._clock_view.apply_config(self.config)
        schedule = build_exam_schedule(self.config)
        display_state = build_exam_display_state(exam_now(), schedule)
        self._clock_view.refresh_labels(schedule, display_state)

    def _launch_clock(self) -> None:
        self._apply_config()
        self._show_clock()
        self._tick()

    def _show_config(self) -> None:
        self._fullscreen = False
        self._clock_view.hide()
        self._container.pack(fill="both", expand=True)
        self._config_view.show()
        self._cancel_tick()

    def _show_clock(self) -> None:
        self._config_view.hide()
        self._container.pack_forget()
        self._fullscreen = True
        self._clock_view.show()

    def _on_escape(self, _event: tk.Event[tk.Misc]) -> None:
        if self._fullscreen:
            self._show_config()

    def _tick(self) -> None:
        display_format = "%H:%M:%S" if self.config.show_seconds else "%H:%M"
        self._clock_view.set_time_text(time.strftime(display_format))

        schedule = build_exam_schedule(self.config)
        display_state = build_exam_display_state(exam_now(), schedule)
        self._clock_view.refresh_labels(schedule, display_state)

        self._clock_job = self.root.after(250, self._tick)

    def _cancel_tick(self) -> None:
        if self._clock_job is not None:
            self.root.after_cancel(self._clock_job)
            self._clock_job = None

    def run(self) -> None:
        self.root.mainloop()


def run() -> None:
    ClockApplication().run()
