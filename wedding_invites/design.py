"""Load design settings from design.yaml."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4, A5, letter

DEFAULT_DESIGN_PATH = Path(__file__).resolve().parent.parent / "design.yaml"

PAGE_SIZES = {
    "letter": letter,
    "a4": A4,
    "a5": A5,
}

DEFAULT_COLORS = {
    "background": [0.96, 0.93, 0.88],
    "panel": [0.99, 0.98, 0.96],
    "gold": [0.58, 0.44, 0.20],
    "gold_light": [0.78, 0.66, 0.38],
    "sage": [0.52, 0.62, 0.54],
    "sage_dark": [0.34, 0.44, 0.38],
    "text_dark": [0.14, 0.13, 0.12],
    "text_light": [0.48, 0.44, 0.40],
}


def _rgb_color(values: List[float]) -> Color:
    return Color(values[0], values[1], values[2])


def load_design(path: Optional[str] = None) -> Dict[str, Any]:
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

    colors_cfg = {**DEFAULT_COLORS, **(data.get("colors") or {})}
    colors = {key: _rgb_color(values) for key, values in colors_cfg.items()}

    fonts = data.get("fonts", {})
    layout = data.get("layout", {})
    copy = data.get("copy", {})

    return {
        "page_size": page_size,
        "page_name": page_key,
        "colors": colors,
        "fonts": {
            "guest_size": int(fonts.get("guest_size", 15)),
            "guest_tracking": float(fonts.get("guest_tracking", 2.5)),
            "invite_line_size": int(fonts.get("invite_line_size", 13)),
            "name_size": int(fonts.get("name_size", 44)),
            "name_min_size": int(fonts.get("name_min_size", 28)),
            "ampersand_size": int(fonts.get("ampersand_size", 32)),
            "detail_size": int(fonts.get("detail_size", 11)),
            "detail_leading": float(fonts.get("detail_leading", 14)),
            "date_day_size": int(fonts.get("date_day_size", 34)),
            "date_month_size": int(fonts.get("date_month_size", 11)),
            "date_year_size": int(fonts.get("date_year_size", 10)),
            "time_size": int(fonts.get("time_size", 13)),
            "venue_name_size": int(fonts.get("venue_name_size", 13)),
            "reception_size": int(fonts.get("reception_size", 11)),
        },
        "layout": {
            "margin_inches": float(layout.get("margin_inches", 0.75)),
            "content_width_inches": float(layout.get("content_width_inches", 5.5)),
            "frame_inset_inches": float(layout.get("frame_inset_inches", 0.38)),
        },
        "copy": {
            "guest_prefix": copy.get("guest_prefix", ""),
            "invitation_line": copy.get(
                "invitation_line",
                "request the pleasure of your company\nat the celebration of the marriage of",
            ),
            "time_prefix": copy.get("time_prefix", "at"),
            "default_guest": copy.get("default_guest", "Dear Guest"),
            "default_reception": copy.get(
                "default_reception", "Dinner and dancing to follow"
            ),
        },
    }
