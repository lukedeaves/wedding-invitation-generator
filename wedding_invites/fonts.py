"""Register bundled fonts with ReportLab."""

from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"
_REGISTERED = False

FONT_SCRIPT = "GreatVibes"
FONT_BODY = "Cormorant"
FONT_BODY_ITALIC = "Cormorant-Italic"


def register_fonts() -> None:
    """Register custom fonts, falling back silently if files are missing."""
    global _REGISTERED
    if _REGISTERED:
        return

    mappings = [
        (FONT_SCRIPT, "GreatVibes-Regular.ttf"),
        (FONT_BODY, "CormorantGaramond.ttf"),
        (FONT_BODY_ITALIC, "CormorantGaramond-Italic.ttf"),
    ]

    for font_name, filename in mappings:
        path = _FONTS_DIR / filename
        if path.exists():
            try:
                pdfmetrics.registerFont(TTFont(font_name, str(path)))
            except Exception:
                pass

    _REGISTERED = True


def body_font() -> str:
    return FONT_BODY if FONT_BODY in pdfmetrics.getRegisteredFontNames() else "Helvetica"


def body_italic_font() -> str:
    if FONT_BODY_ITALIC in pdfmetrics.getRegisteredFontNames():
        return FONT_BODY_ITALIC
    return "Helvetica-Oblique"


def script_font() -> str:
    return FONT_SCRIPT if FONT_SCRIPT in pdfmetrics.getRegisteredFontNames() else "Helvetica-Oblique"
