from __future__ import annotations

import tkinter as tk

from src.constants import (
    CLOCK_CENTER_RELY,
    LABEL_DEPARTURE,
    LABEL_EXAM_END,
    LABEL_EXAM_START,
    META_LABEL_FONT_SIZE,
)
from src.formatting import format_time_hm
from src.models import ClockConfig, ExamDisplayState, ExamSchedule


class ClockView:
    """Affichage plein écran de l'horloge et des horaires d'épreuve."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.frame = tk.Frame(root, bd=0, highlightthickness=0)
        self._config = ClockConfig()
        self._meta_labels: tuple[tk.Label, ...] = ()

        self.time_label = tk.Label(self.frame, text="00:00:00", bd=0, highlightthickness=0, relief="flat")
        self.meta_frame = tk.Frame(self.frame, bd=0, highlightthickness=0)
        self.meta_center = tk.Frame(self.meta_frame, bd=0, highlightthickness=0)
        self.meta_center.pack(anchor="center")

        self.general_start_label = self._make_meta_label()
        self.general_end_label = self._make_meta_label()
        self.current_part_end_label = self._make_meta_label(text="Fin partie en cours: --:--")
        self.departure_label = self._make_meta_label()

        self.general_start_label.pack(anchor="center", pady=(0, 8))
        self.general_end_label.pack(anchor="center", pady=(0, 8))
        self.current_part_end_label.pack(anchor="center", pady=(0, 8))
        self.departure_label.pack(anchor="center")

        self._meta_labels = (
            self.general_start_label,
            self.general_end_label,
            self.current_part_end_label,
            self.departure_label,
        )

        self.meta_frame.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 24))
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def _make_meta_label(self, text: str = "") -> tk.Label:
        return tk.Label(
            self.meta_center,
            text=text,
            bd=0,
            highlightthickness=0,
            relief="flat",
        )

    def apply_config(self, config: ClockConfig) -> None:
        self._config = config
        bg = config.bg_color
        self.root.configure(bg=bg)
        self.frame.configure(bg=bg)
        self.meta_frame.configure(bg=bg)
        self.meta_center.configure(bg=bg)

        clock_font = (config.font_family, config.font_size, "bold")
        self.time_label.configure(bg=bg, fg=config.text_color, font=clock_font)

        meta_font = (config.font_family, META_LABEL_FONT_SIZE, "bold")
        label_colors = (
            (self.general_start_label, config.start_label_color),
            (self.current_part_end_label, config.start_label_color),
            (self.general_end_label, config.end_label_color),
            (self.departure_label, config.end_label_color),
        )
        for label, color in label_colors:
            label.configure(bg=bg, fg=color, font=meta_font)

    def refresh_labels(self, schedule: ExamSchedule, display_state: ExamDisplayState) -> None:
        self.general_start_label.configure(text=f"{LABEL_EXAM_START}: {format_time_hm(schedule.general_start)}")
        self.general_end_label.configure(text=f"{LABEL_EXAM_END}: {format_time_hm(schedule.general_end)}")
        self.departure_label.configure(text=f"{LABEL_DEPARTURE}: {format_time_hm(schedule.departure_authorized)}")

        if (
            display_state.show_current_part_end
            and display_state.current_part_end is not None
            and display_state.current_part_name
        ):
            self.current_part_end_label.configure(
                text=f"Fin {display_state.current_part_name}: {format_time_hm(display_state.current_part_end)}"
            )
            if not self.current_part_end_label.winfo_ismapped():
                self.current_part_end_label.pack(anchor="center", pady=(0, 8), before=self.departure_label)
        else:
            self.current_part_end_label.pack_forget()

        if self._config.show_exam_labels:
            if not self.meta_frame.winfo_ismapped():
                self.meta_frame.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 24))
        else:
            self.meta_frame.grid_remove()

    def set_time_text(self, text: str) -> None:
        self.time_label.configure(text=text)

    def show(self) -> None:
        from src import theme

        self.root.title(f"{theme.TITLE_APP} — Plein écran")
        self.frame.pack(fill="both", expand=True)
        self.root.attributes("-fullscreen", True)
        self.time_label.place(relx=0.5, rely=CLOCK_CENTER_RELY, anchor="center")

    def hide(self) -> None:
        self.time_label.place_forget()
        self.frame.pack_forget()
        self.root.attributes("-fullscreen", False)
