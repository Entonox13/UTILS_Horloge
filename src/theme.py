# -*- coding: utf-8 -*-
"""Thème graphique partagé — aligné sur BGRAPP Pyconseil / Pyjury."""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from typing import Optional, Tuple

_UI_FONT_CANDIDATES = (
    "DejaVu Sans",
    "Noto Sans",
    "Ubuntu",
    "Liberation Sans",
    "Cantarell",
    "Source Sans 3",
    "Source Sans Pro",
    "Open Sans",
    "Inter",
    "Verdana",
    "Segoe UI",
    "Arial",
)
_MONO_FONT_CANDIDATES = (
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Ubuntu Mono",
    "JetBrains Mono",
    "Cascadia Mono",
    "Noto Sans Mono",
    "Consolas",
)

FONT_SIZE_BODY = 13
FONT_SIZE_HEADER = 14
FONT_SIZE_SUBTITLE = 15
FONT_SIZE_TITLE = 20
FONT_SIZE_MONO = 12

PADDING_COMPACT = "8"
PADDING_NORMAL = "12"
PADDING_LARGE = "20"

COLOR_BG = "#f4f6f8"
COLOR_SURFACE = "#ffffff"
COLOR_BORDER = "#d8dee4"
COLOR_TEXT = "#1a1f24"
COLOR_TEXT_MUTED = "#5c6770"
COLOR_PRIMARY = "#1a5fb4"

TITLE_APP = "Horloge"
SUBTITLE_APP = "Affichage plein écran pour épreuves et surveillances"

SECTION_COLORS = "Couleurs"
SECTION_TYPOGRAPHY = "Typographie"
SECTION_OPTIONS = "Options"
SECTION_EXAM = "Épreuve"
SECTION_TIMELINE = "Timeline"

BTN_LAUNCH = "Lancer"
BTN_QUIT = "Quitter"
BTN_CHOOSE = "Choisir"

LOG_WARN = "[AVERT]"

# Polices proposées pour l'horloge (liste courte, polices vectorielles).
_CLOCK_FONT_CANDIDATES = (
    "DejaVu Sans",
    "Liberation Sans",
    "Noto Sans",
    "Ubuntu",
    "Cantarell",
    "Source Sans 3",
    "Source Sans Pro",
    "Open Sans",
    "Verdana",
    "Segoe UI",
    "Arial",
    "Helvetica",
    "Times New Roman",
    "Courier New",
)

_BITMAP_RESOLVED_NAMES = frozenset({"fixed", "courier", "helvetica"})
_BITMAP_FAMILY_NAMES = frozenset(
    {
        "c059",
        "d050000l",
        "p052",
        "z003",
        "clean",
        "clearlyu",
        "clearlyu alternate glyphs",
        "clearlyu pua",
        "fixed",
        "courier",
        "newspaper",
    }
)

_available_families: Optional[set] = None
_font_ui: Optional[str] = None
_font_mono: Optional[str] = None
_fonts_initialized = False
_font_warning_shown = False


def _fallback_families() -> set:
    return set(_UI_FONT_CANDIDATES) | set(_MONO_FONT_CANDIDATES)


def _font_families(root: Optional[tk.Misc] = None) -> set:
    global _available_families
    if _available_families is None:
        try:
            probe = root or tk._default_root
            if probe is None:
                temp = tk.Tk()
                temp.withdraw()
                families = tkfont.families(temp)
                temp.destroy()
            else:
                families = tkfont.families(probe)
            if isinstance(families, (list, tuple, set)):
                _available_families = set(families)
            else:
                _available_families = _fallback_families()
        except Exception:
            _available_families = _fallback_families()
    return _available_families


def _font_resolves_to_bitmap(family: str, root: Optional[tk.Misc] = None, *, probe_size: int = FONT_SIZE_BODY) -> bool:
    try:
        probe = root or tk._default_root
        if probe is None:
            return False
        actual = tkfont.Font(root=probe, family=family, size=probe_size).actual()
        resolved = str(actual.get("family", "")).lower()
        actual_size = int(actual.get("size", probe_size))
        if resolved in _BITMAP_RESOLVED_NAMES:
            return True
        if resolved in _BITMAP_FAMILY_NAMES or family.lower() in _BITMAP_FAMILY_NAMES:
            return True
        # Les polices bitmap ignorent souvent la taille demandée (ex. Clean -> 9 pt).
        if actual_size != probe_size:
            return True
        if "emoji" in resolved:
            return True
        return False
    except tk.TclError:
        return True


def is_scalable_font(family: str, root: Optional[tk.Misc] = None, *, probe_size: int = FONT_SIZE_BODY) -> bool:
    if not family or family == "TkDefaultFont":
        return False
    return not _font_resolves_to_bitmap(family, root, probe_size=probe_size)


def discover_clock_fonts(root: tk.Misc) -> list[str]:
    """Liste courte de polices vectorielles pour l'horloge."""
    families = _font_families(root)
    kept = [
        name
        for name in _CLOCK_FONT_CANDIDATES
        if name in families and is_scalable_font(name, root)
    ]
    if kept:
        return kept
    fallback = get_font_ui()
    return [fallback] if is_scalable_font(fallback, root) else ["DejaVu Sans"]


def resolve_clock_font(family: str, root: Optional[tk.Misc] = None) -> str:
    if is_scalable_font(family, root):
        return family
    return get_font_ui()


def _pick_font_family(candidates: Tuple[str, ...], root: Optional[tk.Misc] = None) -> str:
    families = _font_families(root)
    for name in candidates:
        if name in families and not _font_resolves_to_bitmap(name, root):
            return name
    for name in candidates:
        if name in families:
            return name
    return "TkDefaultFont"


def get_font_ui() -> str:
    global _font_ui
    if _font_ui is None:
        _font_ui = _pick_font_family(_UI_FONT_CANDIDATES)
    return _font_ui


def get_font_mono() -> str:
    global _font_mono
    if _font_mono is None:
        _font_mono = _pick_font_family(_MONO_FONT_CANDIDATES)
    return _font_mono


def init_fonts(root: tk.Misc) -> str:
    global _font_ui, _font_mono, _fonts_initialized, _font_warning_shown, _available_families
    _available_families = None
    _font_families(root)
    _font_ui = _pick_font_family(_UI_FONT_CANDIDATES, root)
    _font_mono = _pick_font_family(_MONO_FONT_CANDIDATES, root)
    _fonts_initialized = True

    if _font_resolves_to_bitmap(_font_ui, root) and not _font_warning_shown:
        _font_warning_shown = True
        print(
            f"{LOG_WARN} Polices Tk pixellisées : l'environnement conda utilise tk sans fontconfig (build noxft).\n"
            "  Depuis la racine du projet : conda env update -f environment.yml --prune\n"
            "  Ou : conda install -c conda-forge tk=8.6.13=xft_h891c84d_3"
        )
    return _font_ui


def font_ui(size: int, bold: bool = False) -> Tuple[str, int, str]:
    style = "bold" if bold else "normal"
    return (get_font_ui(), size, style)


def font_body(bold: bool = False) -> Tuple[str, int, str]:
    return font_ui(FONT_SIZE_BODY, bold=bold)


def font_mono() -> Tuple[str, int]:
    return (get_font_mono(), FONT_SIZE_MONO)


def setup_root_scaling(root: tk.Misc) -> None:
    global _fonts_initialized
    if not _fonts_initialized:
        init_fonts(root)
    try:
        dpi = root.winfo_fpixels("1i")
        if not isinstance(dpi, (int, float)) or dpi <= 0:
            return
        scaling = max(1.0, min(dpi / 96.0, 2.0))
        root.tk.call("tk", "scaling", scaling)
    except (tk.TclError, TypeError, AttributeError):
        pass


def fit_window_to_screen(
    root: tk.Misc,
    width: int,
    height: int,
    *,
    margin: int = 48,
    min_width: int = 640,
    min_height: int = 480,
) -> None:
    """Dimensionne et centre la fenêtre sans dépasser l'écran."""
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    max_w = max(min_width, screen_w - margin)
    max_h = max(min_height, screen_h - margin)
    w = min(width, max_w)
    h = min(height, max_h)
    x = max(0, (screen_w - w) // 2)
    y = max(0, (screen_h - h) // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.minsize(min(min_width, w), min(min_height, h))
    root.maxsize(screen_w, screen_h)


def apply_theme(style: ttk.Style, *, root: Optional[tk.Misc] = None) -> None:
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    if root is not None:
        root.configure(bg=COLOR_BG)

    style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT, font=font_body())
    style.configure("TFrame", background=COLOR_BG)
    style.configure("Card.TFrame", background=COLOR_SURFACE, relief="flat")
    style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=font_body())
    style.configure("Card.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT, font=font_body())
    style.configure("Title.TLabel", font=font_ui(FONT_SIZE_TITLE, bold=True), background=COLOR_BG)
    style.configure("Subtitle.TLabel", font=font_ui(FONT_SIZE_SUBTITLE, bold=True), background=COLOR_BG)
    style.configure("Section.TLabel", font=font_ui(FONT_SIZE_HEADER, bold=True), background=COLOR_SURFACE)
    style.configure("Muted.TLabel", font=font_body(), foreground=COLOR_TEXT_MUTED, background=COLOR_BG)
    style.configure("CardMuted.TLabel", font=font_body(), foreground=COLOR_TEXT_MUTED, background=COLOR_SURFACE)
    style.configure("Panel.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT, font=font_body())

    style.configure(
        "TLabelframe",
        background=COLOR_SURFACE,
        bordercolor=COLOR_BORDER,
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "TLabelframe.Label",
        background=COLOR_SURFACE,
        foreground=COLOR_TEXT,
        font=font_ui(FONT_SIZE_HEADER, bold=True),
    )

    style.configure("TButton", font=font_body(), padding=(10, 6))
    style.configure("Primary.TButton", font=font_body(bold=True))
    style.configure("TCheckbutton", font=font_body(), background=COLOR_SURFACE)
    style.configure("TEntry", font=font_body(), fieldbackground=COLOR_SURFACE)
    style.configure("TCombobox", font=font_body(), fieldbackground=COLOR_SURFACE)
    style.configure("Horizontal.TSeparator", background=COLOR_BORDER)


def section_card(parent: tk.Widget, title: str, row: int = 0, column: int = 0, **grid_kw) -> ttk.LabelFrame:
    frame = ttk.LabelFrame(parent, text=title, padding=PADDING_NORMAL)
    frame.grid(row=row, column=column, sticky=(tk.W, tk.E), **grid_kw)
    return frame


def color_swatch(parent: tk.Widget, variable: tk.StringVar, *, width: int = 4) -> tk.Label:
    swatch = tk.Label(
        parent,
        text="",
        width=width,
        relief=tk.SOLID,
        borderwidth=1,
        highlightthickness=1,
        highlightbackground=COLOR_BORDER,
        bg=variable.get(),
    )

    def _on_change(*_args: object) -> None:
        swatch.configure(bg=variable.get())

    variable.trace_add("write", _on_change)
    return swatch
