from __future__ import annotations

import time
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime, timedelta
from tkinter import colorchooser, ttk
from tkinter import font as tkfont


@dataclass
class ClockConfig:
    bg_color: str = "#000000"
    text_color: str = "#FFFFFF"
    start_label_color: str = "#4FC3F7"
    end_label_color: str = "#FFB74D"
    font_family: str = "Arial"
    font_size: int = 300
    show_seconds: bool = True
    show_start_end_labels: bool = True
    start_hour: int = 8
    start_minute: int = 0
    duration_minutes: int = 60


class ClockApplication:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Horloge - Configuration")
        self.root.geometry("1100x900")
        self.root.minsize(980, 820)

        self.config = ClockConfig()
        self._clock_job: str | None = None
        self._fullscreen = False

        self._available_fonts = self._discover_fonts()

        self.bg_var = tk.StringVar(value=self.config.bg_color)
        self.text_var = tk.StringVar(value=self.config.text_color)
        self.start_label_color_var = tk.StringVar(value=self.config.start_label_color)
        self.end_label_color_var = tk.StringVar(value=self.config.end_label_color)
        self.font_var = tk.StringVar(value=self.config.font_family)
        self.size_var = tk.IntVar(value=self.config.font_size)
        self.show_seconds_var = tk.BooleanVar(value=self.config.show_seconds)
        self.show_start_end_labels_var = tk.BooleanVar(value=self.config.show_start_end_labels)
        self.start_hour_var = tk.IntVar(value=self.config.start_hour)
        self.start_minute_var = tk.IntVar(value=self.config.start_minute)
        self.duration_minutes_var = tk.IntVar(value=self.config.duration_minutes)

        self.container = ttk.Frame(self.root, padding=24)
        self.container.pack(fill="both", expand=True)

        self.config_frame = ttk.Frame(self.container)
        self.clock_frame = tk.Frame(self.root, bg=self.config.bg_color, bd=0, highlightthickness=0)

        self._build_config_view()
        self._build_clock_view()
        self._show_config()

        self.root.bind("<Escape>", self._on_escape)

    def _discover_fonts(self) -> list[str]:
        # Keep the list simple and predictable, using only system fonts.
        preferred = ["Arial", "Helvetica", "Times New Roman", "Courier New", "TkDefaultFont"]
        discovered = sorted(set(tkfont.families()))
        kept = [name for name in preferred if name in discovered]
        if not kept:
            kept = discovered[:10] if discovered else ["TkDefaultFont"]
        return kept

    def _build_config_view(self) -> None:
        self.config_frame.pack(fill="both", expand=True)

        title = ttk.Label(self.config_frame, text="Configuration Horloge", font=("TkDefaultFont", 20, "bold"))
        title.pack(pady=(0, 18))

        colors_card = ttk.LabelFrame(self.config_frame, text="Couleurs", padding=12)
        colors_card.pack(fill="x", pady=8)

        bg_row = ttk.Frame(colors_card)
        bg_row.pack(fill="x", pady=6)
        ttk.Label(bg_row, text="Fond").pack(side="left")
        self.bg_preview = tk.Label(bg_row, textvariable=self.bg_var, width=12, bg=self.bg_var.get(), fg="#FFFFFF")
        self.bg_preview.pack(side="left", padx=12)
        ttk.Button(bg_row, text="Choisir", command=self._choose_bg_color).pack(side="left")

        text_row = ttk.Frame(colors_card)
        text_row.pack(fill="x", pady=6)
        ttk.Label(text_row, text="Texte").pack(side="left")
        self.text_preview = tk.Label(
            text_row, textvariable=self.text_var, width=12, bg=self.text_var.get(), fg="#000000"
        )
        self.text_preview.pack(side="left", padx=12)
        ttk.Button(text_row, text="Choisir", command=self._choose_text_color).pack(side="left")

        start_label_row = ttk.Frame(colors_card)
        start_label_row.pack(fill="x", pady=6)
        ttk.Label(start_label_row, text="Label heure debut").pack(side="left")
        self.start_label_color_preview = tk.Label(
            start_label_row,
            textvariable=self.start_label_color_var,
            width=12,
            bg=self.start_label_color_var.get(),
            fg="#000000",
        )
        self.start_label_color_preview.pack(side="left", padx=12)
        ttk.Button(start_label_row, text="Choisir", command=self._choose_start_label_color).pack(side="left")

        end_label_row = ttk.Frame(colors_card)
        end_label_row.pack(fill="x", pady=6)
        ttk.Label(end_label_row, text="Label heure fin").pack(side="left")
        self.end_label_color_preview = tk.Label(
            end_label_row,
            textvariable=self.end_label_color_var,
            width=12,
            bg=self.end_label_color_var.get(),
            fg="#000000",
        )
        self.end_label_color_preview.pack(side="left", padx=12)
        ttk.Button(end_label_row, text="Choisir", command=self._choose_end_label_color).pack(side="left")

        font_card = ttk.LabelFrame(self.config_frame, text="Typographie", padding=12)
        font_card.pack(fill="x", pady=8)

        font_row = ttk.Frame(font_card)
        font_row.pack(fill="x", pady=6)
        ttk.Label(font_row, text="Police").pack(side="left")
        font_combo = ttk.Combobox(
            font_row,
            textvariable=self.font_var,
            values=self._available_fonts,
            state="readonly",
            width=30,
        )
        font_combo.pack(side="left", padx=12)

        size_row = ttk.Frame(font_card)
        size_row.pack(fill="x", pady=6)
        ttk.Label(size_row, text="Taille texte").pack(side="left")
        size_spin = ttk.Spinbox(size_row, from_=24, to=360, increment=2, textvariable=self.size_var, width=10)
        size_spin.pack(side="left", padx=12)

        options_card = ttk.LabelFrame(self.config_frame, text="Options", padding=12)
        options_card.pack(fill="x", pady=8)
        ttk.Checkbutton(options_card, text="Afficher les secondes", variable=self.show_seconds_var).pack(
            anchor="w"
        )
        ttk.Checkbutton(
            options_card,
            text="Afficher les labels heure debut / heure fin",
            variable=self.show_start_end_labels_var,
        ).pack(anchor="w")

        schedule_card = ttk.LabelFrame(self.config_frame, text="Plage horaire", padding=12)
        schedule_card.pack(fill="x", pady=8)

        start_row = ttk.Frame(schedule_card)
        start_row.pack(fill="x", pady=6)
        ttk.Label(start_row, text="Heure de debut").pack(side="left")
        ttk.Spinbox(start_row, from_=0, to=23, textvariable=self.start_hour_var, width=4, wrap=True).pack(
            side="left", padx=(12, 4)
        )
        ttk.Label(start_row, text=":").pack(side="left")
        ttk.Spinbox(
            start_row,
            from_=0,
            to=59,
            format="%02.0f",
            textvariable=self.start_minute_var,
            width=4,
            wrap=True,
        ).pack(side="left", padx=(4, 0))

        duration_row = ttk.Frame(schedule_card)
        duration_row.pack(fill="x", pady=6)
        ttk.Label(duration_row, text="Duree (minutes)").pack(side="left")
        ttk.Spinbox(
            duration_row,
            from_=1,
            to=1440,
            increment=1,
            textvariable=self.duration_minutes_var,
            width=8,
        ).pack(side="left", padx=12)

        actions = ttk.Frame(self.config_frame)
        actions.pack(fill="x", pady=(18, 0))
        ttk.Button(actions, text="Lancer", command=self._launch_clock).pack(side="left")
        ttk.Button(actions, text="Quitter", command=self.root.destroy).pack(side="right")

    def _build_clock_view(self) -> None:
        self.time_label = tk.Label(
            self.clock_frame,
            text="00:00:00",
            bg=self.config.bg_color,
            fg=self.config.text_color,
            font=(self.config.font_family, self.config.font_size, "bold"),
            bd=0,
            highlightthickness=0,
            relief="flat",
        )
        self.time_label.pack(fill="both", expand=True)

        self.meta_frame = tk.Frame(self.clock_frame, bg=self.config.bg_color, bd=0, highlightthickness=0)
        self.meta_frame.pack(side="bottom", fill="x", pady=(0, 24))

        self.meta_center = tk.Frame(self.meta_frame, bg=self.config.bg_color, bd=0, highlightthickness=0)
        self.meta_center.pack(anchor="center")

        self.start_label = tk.Label(
            self.meta_center,
            text="Heure debut: --:--",
            bg=self.config.bg_color,
            fg=self.config.start_label_color,
            font=(self.config.font_family, 100, "bold"),
            bd=0,
            highlightthickness=0,
            relief="flat",
        )
        self.start_label.pack(anchor="center", pady=(0, 8))

        self.end_label = tk.Label(
            self.meta_center,
            text="Heure fin: --:--",
            bg=self.config.bg_color,
            fg=self.config.end_label_color,
            font=(self.config.font_family, 100, "bold"),
            bd=0,
            highlightthickness=0,
            relief="flat",
        )
        self.end_label.pack(anchor="center")

    def _choose_bg_color(self) -> None:
        color = colorchooser.askcolor(color=self.bg_var.get(), title="Choisir la couleur du fond")[1]
        if color:
            self.bg_var.set(color)
            self.bg_preview.configure(bg=color)

    def _choose_text_color(self) -> None:
        color = colorchooser.askcolor(color=self.text_var.get(), title="Choisir la couleur du texte")[1]
        if color:
            self.text_var.set(color)
            self.text_preview.configure(bg=color)

    def _choose_start_label_color(self) -> None:
        color = colorchooser.askcolor(
            color=self.start_label_color_var.get(), title="Choisir la couleur du label de debut"
        )[1]
        if color:
            self.start_label_color_var.set(color)
            self.start_label_color_preview.configure(bg=color)

    def _choose_end_label_color(self) -> None:
        color = colorchooser.askcolor(color=self.end_label_color_var.get(), title="Choisir la couleur du label de fin")[
            1
        ]
        if color:
            self.end_label_color_var.set(color)
            self.end_label_color_preview.configure(bg=color)

    def _safe_int(self, variable: tk.IntVar, minimum: int, maximum: int, fallback: int) -> int:
        try:
            value = int(variable.get())
        except (TypeError, ValueError):
            value = fallback
        return max(minimum, min(maximum, value))

    def _refresh_start_end_labels(self) -> None:
        start = datetime(2000, 1, 1, self.config.start_hour, self.config.start_minute)
        end = start + timedelta(minutes=self.config.duration_minutes)
        self.start_label.configure(text=f"Heure debut: {start.strftime('%H:%M')}")
        self.end_label.configure(text=f"Heure fin: {end.strftime('%H:%M')}")

        if self.config.show_start_end_labels:
            if not self.meta_frame.winfo_ismapped():
                self.meta_frame.pack(side="bottom", fill="x", pady=(0, 24))
        else:
            self.meta_frame.pack_forget()

    def _apply_config(self) -> None:
        self.config = ClockConfig(
            bg_color=self.bg_var.get(),
            text_color=self.text_var.get(),
            start_label_color=self.start_label_color_var.get(),
            end_label_color=self.end_label_color_var.get(),
            font_family=self.font_var.get(),
            font_size=max(24, int(self.size_var.get())),
            show_seconds=self.show_seconds_var.get(),
            show_start_end_labels=self.show_start_end_labels_var.get(),
            start_hour=self._safe_int(self.start_hour_var, 0, 23, 8),
            start_minute=self._safe_int(self.start_minute_var, 0, 59, 0),
            duration_minutes=self._safe_int(self.duration_minutes_var, 1, 1440, 60),
        )
        self.root.configure(bg=self.config.bg_color)
        self.clock_frame.configure(bg=self.config.bg_color)
        self.meta_frame.configure(bg=self.config.bg_color)
        self.meta_center.configure(bg=self.config.bg_color)
        self.time_label.configure(
            bg=self.config.bg_color,
            fg=self.config.text_color,
            font=(self.config.font_family, self.config.font_size, "bold"),
        )
        self.start_label.configure(bg=self.config.bg_color, fg=self.config.start_label_color)
        self.end_label.configure(bg=self.config.bg_color, fg=self.config.end_label_color)
        self.start_label.configure(font=(self.config.font_family, 100, "bold"))
        self.end_label.configure(font=(self.config.font_family, 100, "bold"))
        self._refresh_start_end_labels()

    def _launch_clock(self) -> None:
        self._apply_config()
        self._show_clock()
        self._tick()

    def _show_config(self) -> None:
        self.root.title("Horloge - Configuration")
        self.root.attributes("-fullscreen", False)
        self._fullscreen = False
        self.clock_frame.pack_forget()
        self.container.pack(fill="both", expand=True)
        self.config_frame.pack(fill="both", expand=True)
        self._cancel_tick()

    def _show_clock(self) -> None:
        self.root.title("Horloge - Plein ecran")
        self.config_frame.pack_forget()
        self.container.pack_forget()
        self.clock_frame.pack(fill="both", expand=True)
        self.root.attributes("-fullscreen", True)
        self._fullscreen = True

    def _on_escape(self, _event: tk.Event[tk.Misc]) -> None:
        if self._fullscreen:
            self._show_config()

    def _tick(self) -> None:
        display_format = "%H:%M:%S" if self.config.show_seconds else "%H:%M"
        self.time_label.configure(text=time.strftime(display_format))
        self._clock_job = self.root.after(250, self._tick)

    def _cancel_tick(self) -> None:
        if self._clock_job is not None:
            self.root.after_cancel(self._clock_job)
            self._clock_job = None

    def run(self) -> None:
        self.root.mainloop()


def run() -> None:
    app = ClockApplication()
    app.run()
