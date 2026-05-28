"""Text measurement and drawing helpers for ReportLab canvas."""

from typing import Tuple

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


def content_width(page_width: float, margin: float, design_width_inches: float) -> float:
    from reportlab.lib.units import inch

    max_width = page_width - 2 * margin
    preferred = design_width_inches * inch
    return min(max_width, preferred)


def string_width(c: canvas.Canvas, text: str, font: str, size: float) -> float:
    c.setFont(font, size)
    return c.stringWidth(text, font, size)


def fit_font_size(
    c: canvas.Canvas,
    text: str,
    font: str,
    max_size: float,
    min_size: float,
    max_width: float,
) -> float:
    """Reduce font size until text fits within max_width."""
    size = max_size
    while size > min_size:
        if string_width(c, text, font, size) <= max_width:
            return size
        size -= 1
    return min_size


def draw_centered_text(
    c: canvas.Canvas,
    text: str,
    y: float,
    page_width: float,
    font: str,
    size: float,
    color,
) -> float:
    """Draw single-line centered text; returns the y position below the line."""
    c.setFillColor(color)
    c.setFont(font, size)
    width = c.stringWidth(text, font, size)
    c.drawString((page_width - width) / 2, y, text)
    return y - size * 1.35


def draw_centered_paragraph(
    c: canvas.Canvas,
    text: str,
    top_y: float,
    page_width: float,
    max_width: float,
    font: str,
    size: float,
    color,
    leading: float | None = None,
) -> float:
    """Draw wrapped centered text; returns y below the block."""
    if leading is None:
        leading = size * 1.25

    style = ParagraphStyle(
        name="Centered",
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_CENTER,
    )
    para = Paragraph(text.replace("\n", "<br/>"), style)
    w, h = para.wrap(max_width, 10000)
    x = (page_width - w) / 2
    para.drawOn(c, x, top_y - h)
    return top_y - h - 0.15 * 72  # small gap in points
