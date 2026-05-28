"""Load design settings from design.yaml."""

from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4, A5, letter

DEFAULT_DESIGN_PATH = Path(__file__).resolve().parent.parent / "design.yaml"

PAGE_SIZES = {
    "letter": letter,
    "a4": A4,
    "a5": A5,
}


def _rgb_color(values: List[float]) -> Color:
    return Color(values[0], values[1], values[2])


def load_design(path: str | None = None) -> Dict[str, Any]:
    """Load design configuration with sensible defaults."""
    design_path = Path(path) if path else DEFAULT_DESIGN_PATH
    data: Dict[str, Any] = {}

    if design_path.exists():
        with open(design_path, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
            if isinstance(loaded, dict):
                data = loaded

    page_key = str(data.get("page", {}).get("size", "letter")).lower()
    page_size = PAGE_SIZES.get(page_key, letter)

    colors_cfg = data.get("colors", {})
    colors = {
        "background": _rgb_color(colors_cfg.get("background", [0.98, 0.98, 0.96])),
        "gold": _rgb_color(colors_cfg.get("gold", [0.72, 0.58, 0.28])),
        "text_dark": _rgb_color(colors_cfg.get("text_dark", [0.18, 0.18, 0.18])),
        "text_light": _rgb_color(colors_cfg.get("text_light", [0.42, 0.42, 0.42])),
    }

    fonts = data.get("fonts", {})
    layout = data.get("layout", {})
    copy = data.get("copy", {})

    return {
        "page_size": page_size,
        "page_name": page_key,
        "colors": colors,
        "fonts": {
            "guest_size": int(fonts.get("guest_size", 17)),
            "invite_line_size": int(fonts.get("invite_line_size", 14)),
            "name_size": int(fonts.get("name_size", 40)),
            "name_min_size": int(fonts.get("name_min_size", 26)),
            "and_size": int(fonts.get("and_size", 18)),
            "detail_size": int(fonts.get("detail_size", 12)),
            "date_day_size": int(fonts.get("date_day_size", 18)),
            "reception_size": int(fonts.get("reception_size", 11)),
        },
        "layout": {
            "margin_inches": float(layout.get("margin_inches", 0.75)),
            "content_width_inches": float(layout.get("content_width_inches", 6.0)),
        },
        "copy": {
            "invitation_line": copy.get(
                "invitation_line", "You are invited to the wedding of"
            ),
            "connector": copy.get("connector", "and"),
            "default_guest": copy.get("default_guest", "Dear Guest"),
            "default_reception": copy.get(
                "default_reception", "Reception to follow"
            ),
        },
    }
