from __future__ import annotations

import tkinter as tk
from tkinter import colorchooser, ttk
from typing import Callable

from src import theme
from src.constants import CONFIG_WINDOW_SIZE
from src.gui.timeline import TimelineEditor
from src.models import ClockConfig


class ConfigView:
    """Fenêtre de configuration (couleurs, typographie, épreuve)."""

    def __init__(self, root: tk.Tk, parent: ttk.Frame, config: ClockConfig, available_fonts: list[str]) -> None:
        self.root = root
        self.frame = ttk.Frame(parent)
        self._canvas: tk.Canvas | None = None
        self._timeline: TimelineEditor | None = None

        self.bg_var = tk.StringVar(value=config.bg_color)
        self.text_var = tk.StringVar(value=config.text_color)
        self.start_label_color_var = tk.StringVar(value=config.start_label_color)
        self.end_label_color_var = tk.StringVar(value=config.end_label_color)
        self.font_var = tk.StringVar(value=config.font_family)
        self.size_var = tk.IntVar(value=config.font_size)
        self.show_seconds_var = tk.BooleanVar(value=config.show_seconds)
        self.show_exam_labels_var = tk.BooleanVar(value=config.show_exam_labels)

        self._available_fonts = available_fonts
        self._on_launch: Callable[[], None] | None = None
        self._on_quit: Callable[[], None] | None = None

    def on_launch(self, callback: Callable[[], None]) -> None:
        self._on_launch = callback

    def on_quit(self, callback: Callable[[], None]) -> None:
        self._on_quit = callback

    @property
    def timeline(self) -> TimelineEditor:
        if self._timeline is None:
            raise RuntimeError("ConfigView.build() must be called first")
        return self._timeline

    def build(self) -> None:
        self.frame.pack(fill="both", expand=True)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        scroll_container = ttk.Frame(self.frame)
        scroll_container.grid(row=0, column=0, sticky="nsew")
        scroll_container.rowconfigure(0, weight=1)
        scroll_container.columnconfigure(0, weight=1)

        self._canvas = tk.Canvas(scroll_container, highlightthickness=0, bg=theme.COLOR_BG)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._canvas.grid(row=0, column=0, sticky="nsew")

        content = ttk.Frame(self._canvas, padding=theme.PADDING_LARGE)
        scroll_window = self._canvas.create_window((0, 0), window=content, anchor="nw")
        content.bind("<Configure>", lambda _e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>", lambda e: self._canvas.itemconfigure(scroll_window, width=e.width))
        self._bind_scroll(self._canvas)

        content.columnconfigure(0, weight=1)

        ttk.Label(content, text=theme.TITLE_APP, style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Label(content, text=theme.SUBTITLE_APP, style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 16))
        ttk.Separator(content, orient="horizontal").grid(row=2, column=0, sticky="ew", pady=(0, 16))

        colors_card = theme.section_card(content, theme.SECTION_COLORS, row=3, pady=(0, 8))
        colors_card.columnconfigure(1, weight=1)
        self._add_color_row(colors_card, 0, "Fond", self.bg_var, self._choose_bg_color)
        self._add_color_row(colors_card, 1, "Texte horloge", self.text_var, self._choose_text_color)
        self._add_color_row(colors_card, 2, "Label début / partie", self.start_label_color_var, self._choose_start_label_color)
        self._add_color_row(colors_card, 3, "Label fin / départ", self.end_label_color_var, self._choose_end_label_color)

        font_card = theme.section_card(content, theme.SECTION_TYPOGRAPHY, row=4, pady=(0, 8))
        font_card.columnconfigure(1, weight=1)
        ttk.Label(font_card, text="Police", style="Panel.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=6)
        ttk.Combobox(
            font_card,
            textvariable=self.font_var,
            values=self._available_fonts,
            state="readonly",
            width=28,
        ).grid(row=0, column=1, sticky="w", pady=6)
        ttk.Label(font_card, text="Taille texte", style="Panel.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 12), pady=6
        )
        ttk.Spinbox(font_card, from_=24, to=360, increment=2, textvariable=self.size_var, width=8).grid(
            row=1, column=1, sticky="w", pady=6
        )

        options_card = theme.section_card(content, theme.SECTION_OPTIONS, row=5, pady=(0, 8))
        ttk.Checkbutton(options_card, text="Afficher les secondes", variable=self.show_seconds_var).grid(
            row=0, column=0, sticky="w", pady=4
        )
        ttk.Checkbutton(
            options_card,
            text="Afficher les horaires de l'épreuve",
            variable=self.show_exam_labels_var,
        ).grid(row=1, column=0, sticky="w", pady=4)

        exam_card = theme.section_card(content, theme.SECTION_EXAM, row=6, pady=(0, 8))
        self._timeline = TimelineEditor(
            exam_card,
            on_changed=self._noop,
            is_applying_preset=self._timeline_applying_preset,
            safe_int=self._safe_int,
        )

        actions = ttk.Frame(self.frame, padding=(theme.PADDING_LARGE, theme.PADDING_NORMAL))
        actions.grid(row=1, column=0, sticky="ew")
        actions.columnconfigure(0, weight=1)
        ttk.Button(actions, text=theme.BTN_LAUNCH, style="Primary.TButton", command=self._handle_launch).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(actions, text=theme.BTN_QUIT, command=self._handle_quit).grid(row=0, column=1, sticky="e")

    def wire_timeline_callbacks(self, on_changed: Callable[[], None]) -> None:
        if self._timeline is not None:
            self._timeline._on_changed = on_changed

    @staticmethod
    def _noop() -> None:
        return None

    def _timeline_applying_preset(self) -> bool:
        return self._timeline.applying_preset if self._timeline is not None else False

    def load_timeline(self, segments: list) -> None:
        self.timeline.load_segments(segments)

    def show(self) -> None:
        self.root.title(f"{theme.TITLE_APP} — Configuration")
        self.frame.pack(fill="both", expand=True)
        theme.fit_window_to_screen(self.root, *CONFIG_WINDOW_SIZE)
        if self._canvas is not None:
            self._bind_scroll(self._canvas)

    def hide(self) -> None:
        self._unbind_scroll()
        self.frame.pack_forget()

    def read_config(self, *, resolve_font: Callable[[str], str]) -> ClockConfig:
        timeline = self.timeline
        return ClockConfig(
            bg_color=self.bg_var.get(),
            text_color=self.text_var.get(),
            start_label_color=self.start_label_color_var.get(),
            end_label_color=self.end_label_color_var.get(),
            font_family=resolve_font(self.font_var.get()),
            font_size=max(24, int(self.size_var.get())),
            show_seconds=self.show_seconds_var.get(),
            show_exam_labels=self.show_exam_labels_var.get(),
            start_hour=self._safe_int(timeline.start_hour_var, 0, 23, 8),
            start_minute=self._safe_int(timeline.start_minute_var, 0, 59, 0),
            segments=timeline.segments(),
        )

    def _handle_launch(self) -> None:
        if self._on_launch:
            self._on_launch()

    def _handle_quit(self) -> None:
        if self._on_quit:
            self._on_quit()

    def _add_color_row(
        self,
        parent: ttk.Frame,
        row: int,
        label_text: str,
        variable: tk.StringVar,
        command: Callable[[], None],
    ) -> None:
        ttk.Label(parent, text=label_text, style="Panel.TLabel").grid(
            row=row, column=0, sticky="w", padx=(0, 12), pady=6
        )
        row_frame = ttk.Frame(parent)
        row_frame.grid(row=row, column=1, sticky="w", pady=6)
        theme.color_swatch(row_frame, variable).pack(side="left", padx=(0, 8))
        ttk.Label(row_frame, textvariable=variable, style="CardMuted.TLabel").pack(side="left", padx=(0, 12))
        ttk.Button(row_frame, text=theme.BTN_CHOOSE, command=command).pack(side="left")

    def _choose_bg_color(self) -> None:
        color = colorchooser.askcolor(color=self.bg_var.get(), title="Choisir la couleur du fond")[1]
        if color:
            self.bg_var.set(color)

    def _choose_text_color(self) -> None:
        color = colorchooser.askcolor(color=self.text_var.get(), title="Choisir la couleur du texte")[1]
        if color:
            self.text_var.set(color)

    def _choose_start_label_color(self) -> None:
        color = colorchooser.askcolor(
            color=self.start_label_color_var.get(), title="Choisir la couleur du label de début"
        )[1]
        if color:
            self.start_label_color_var.set(color)

    def _choose_end_label_color(self) -> None:
        color = colorchooser.askcolor(
            color=self.end_label_color_var.get(), title="Choisir la couleur du label de fin / départ"
        )[1]
        if color:
            self.end_label_color_var.set(color)

    @staticmethod
    def _safe_int(variable: tk.IntVar, minimum: int, maximum: int, fallback: int) -> int:
        try:
            value = int(variable.get())
        except (TypeError, ValueError):
            value = fallback
        return max(minimum, min(maximum, value))

    def _bind_scroll(self, canvas: tk.Canvas) -> None:
        def _on_mousewheel(event: tk.Event) -> None:
            if event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

    def _unbind_scroll(self) -> None:
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")
