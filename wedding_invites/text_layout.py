"""Text measurement and drawing helpers for ReportLab canvas."""

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


def draw_centered_spaced_caps(
    c: canvas.Canvas,
    text: str,
    y: float,
    page_width: float,
    font: str,
    size: float,
    color,
    tracking: float = 2.5,
) -> float:
    """Draw centred text with increased letter spacing (small-caps feel)."""
    c.setFillColor(color)
    c.setFont(font, size)
    upper = text.upper()
    total = sum(c.stringWidth(ch, font, size) + tracking for ch in upper) - tracking
    x = (page_width - total) / 2
    for ch in upper:
        c.drawString(x, y, ch)
        x += c.stringWidth(ch, font, size) + tracking
    return y - size * 1.4


def draw_centered_lines(
    c: canvas.Canvas,
    lines: list[str],
    top_y: float,
    page_width: float,
    font: str,
    size: float,
    color,
    leading: float | None = None,
) -> float:
    """Draw multiple centred single lines; returns y below last line."""
    if leading is None:
        leading = size * 1.35
    y = top_y
    for line in lines:
        y = draw_centered_text(c, line, y, page_width, font, size, color)
        y += leading - size * 1.35  # adjust for draw_centered_text built-in gap
    return y
