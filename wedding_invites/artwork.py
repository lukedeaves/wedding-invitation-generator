"""Decorative drawing primitives for invitation artwork."""

import math
from typing import Tuple

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

Point = Tuple[float, float]


def _bezier_leaf(
    c: canvas.Canvas,
    origin: Point,
    angle_deg: float,
    length: float,
    color,
    stroke: float = 1.0,
) -> None:
    """Draw a single stylized leaf along a direction from origin."""
    ox, oy = origin
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad), math.sin(rad)
    tip = (ox + dx * length, oy + dy * length)
    ctrl1 = (ox + dx * length * 0.35 - dy * length * 0.22, oy + dy * length * 0.35 + dx * length * 0.22)
    ctrl2 = (ox + dx * length * 0.75 - dy * length * 0.12, oy + dy * length * 0.75 + dx * length * 0.12)

    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(stroke)
    path = c.beginPath()
    path.moveTo(ox, oy)
    path.curveTo(*ctrl1, *ctrl2, *tip)
    path.curveTo(
        ctrl2[0] + dy * length * 0.08,
        ctrl2[1] - dx * length * 0.08,
        ctrl1[0] + dy * length * 0.12,
        ctrl1[1] - dx * length * 0.12,
        ox,
        oy,
    )
    c.drawPath(path, fill=1, stroke=0)


def draw_corner_botanical(
    c: canvas.Canvas,
    corner: str,
    page_width: float,
    page_height: float,
    inset: float,
    colors: dict,
) -> None:
    """Draw mirrored botanical sprigs in a corner."""
    sage = colors.get("sage", colors["gold"])
    sage_dark = colors.get("sage_dark", sage)
    spread = 0.82 * inch

    positions = {
        "top_left": (inset + 0.15 * inch, page_height - inset - 0.15 * inch),
        "top_right": (page_width - inset - 0.15 * inch, page_height - inset - 0.15 * inch),
        "bottom_left": (inset + 0.15 * inch, inset + 0.15 * inch),
        "bottom_right": (page_width - inset - 0.15 * inch, inset + 0.15 * inch),
    }
    angle_sets = {
        "top_left": [-20, 10, 45, 75],
        "top_right": [-160, -110, -75, -45],
        "bottom_left": [20, -10, -45, -75],
        "bottom_right": [160, 110, 75, 45],
    }

    ox, oy = positions[corner]
    for i, angle in enumerate(angle_sets[corner]):
        length = spread * (0.55 + 0.12 * i)
        color = sage_dark if i % 2 else sage
        _bezier_leaf(c, (ox, oy), angle, length, color, stroke=0.8)


def draw_all_corner_botanicals(
    c: canvas.Canvas, page_width: float, page_height: float, inset: float, colors: dict
) -> None:
    for corner in ("top_left", "top_right", "bottom_left", "bottom_right"):
        draw_corner_botanical(c, corner, page_width, page_height, inset, colors)


def draw_layered_frame(
    c: canvas.Canvas,
    page_width: float,
    page_height: float,
    colors: dict,
    outer_inset: float = 0.38 * inch,
    inner_gap: float = 0.11 * inch,
) -> float:
    """
    Draw double gold frame and inner panel.
    Returns the inset content boundary (y/x safe margin inside inner frame).
    """
    gold = colors["gold"]
    gold_light = colors.get("gold_light", gold)
    panel = colors.get("panel", colors["background"])

    # Inner content panel
    panel_inset = outer_inset + inner_gap + 0.14 * inch
    c.setFillColor(panel)
    c.setStrokeColor(gold_light)
    c.setLineWidth(0.5)
    c.roundRect(
        panel_inset,
        panel_inset,
        page_width - 2 * panel_inset,
        page_height - 2 * panel_inset,
        6,
        fill=1,
        stroke=1,
    )

    # Outer frame
    c.setStrokeColor(gold)
    c.setLineWidth(1.25)
    c.roundRect(
        outer_inset,
        outer_inset,
        page_width - 2 * outer_inset,
        page_height - 2 * outer_inset,
        4,
        fill=0,
        stroke=1,
    )

    # Inner frame
    mid = outer_inset + inner_gap
    c.setStrokeColor(gold_light)
    c.setLineWidth(0.6)
    c.roundRect(
        mid,
        mid,
        page_width - 2 * mid,
        page_height - 2 * mid,
        3,
        fill=0,
        stroke=1,
    )

    return panel_inset


def draw_ornament_divider(
    c: canvas.Canvas,
    y: float,
    page_width: float,
    colors: dict,
    width: float = 4.2 * inch,
    style: str = "diamond",
) -> None:
    """Horizontal rule with centre ornament."""
    cx = page_width / 2
    gold = colors["gold"]
    gold_light = colors.get("gold_light", gold)
    half = width / 2

    c.setStrokeColor(gold_light)
    c.setLineWidth(0.6)
    c.line(cx - half, y, cx - 0.22 * inch, y)
    c.line(cx + 0.22 * inch, y, cx + half, y)

    c.setFillColor(gold)
    c.setStrokeColor(gold)
    if style == "diamond":
        s = 0.07 * inch
        path = c.beginPath()
        path.moveTo(cx, y + s)
        path.lineTo(cx + s, y)
        path.lineTo(cx, y - s)
        path.lineTo(cx - s, y)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        c.circle(cx, y, 1.8, fill=1)
    elif style == "dot":
        c.circle(cx, y, 3, fill=1)
        c.circle(cx - 0.35 * inch, y, 1.5, fill=1)
        c.circle(cx + 0.35 * inch, y, 1.5, fill=1)


def draw_corner_flourish(
    c: canvas.Canvas,
    corner: str,
    page_width: float,
    page_height: float,
    inset: float,
    colors: dict,
) -> None:
    """Delicate gold bracket flourish in each corner (inside frame)."""
    gold_light = colors.get("gold_light", colors["gold"])
    c.setStrokeColor(gold_light)
    c.setLineWidth(0.65)
    arm = 0.42 * inch
    gap = inset + 0.28 * inch

    if corner == "top_left":
        x, y, sx, sy = gap, page_height - gap, 1, -1
    elif corner == "top_right":
        x, y, sx, sy = page_width - gap, page_height - gap, -1, -1
    elif corner == "bottom_left":
        x, y, sx, sy = gap, gap, 1, 1
    else:
        x, y, sx, sy = page_width - gap, gap, -1, 1

    c.line(x, y, x + sx * arm, y)
    c.line(x, y, x, y + sy * arm)
    c.setFillColor(gold_light)
    c.circle(x + sx * arm * 0.72, y + sy * arm * 0.72, 1.5, fill=1, stroke=0)


def draw_all_corner_flourishes(
    c: canvas.Canvas, page_width: float, page_height: float, inset: float, colors: dict
) -> None:
    for corner in ("top_left", "top_right", "bottom_left", "bottom_right"):
        draw_corner_flourish(c, corner, page_width, page_height, inset, colors)


def draw_header_emblem(c: canvas.Canvas, y: float, page_width: float, colors: dict) -> None:
    """Top centre wreath-style emblem."""
    cx = page_width / 2
    gold = colors["gold"]
    sage = colors.get("sage", gold)

    c.setStrokeColor(gold)
    c.setLineWidth(0.8)
    c.circle(cx, y, 0.2 * inch, fill=0, stroke=1)

    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = cx + math.cos(rad) * 0.2 * inch
        y1 = y + math.sin(rad) * 0.2 * inch
        x2 = cx + math.cos(rad) * 0.34 * inch
        y2 = y + math.sin(rad) * 0.34 * inch
        c.line(x1, y1, x2, y2)

    for angle in (30, 150, 210, 330):
        _bezier_leaf(c, (cx, y), angle, 0.42 * inch, sage, stroke=0.6)


def draw_date_medallion(
    c: canvas.Canvas,
    cx: float,
    cy: float,
    day: str,
    month: str,
    year: str,
    fonts: dict,
    colors: dict,
    body_font: str,
) -> Tuple[float, float]:
    """Draw date as a centred medallion; returns (width, height) of block."""
    gold = colors["gold"]
    gold_light = colors.get("gold_light", gold)
    text = colors["text_dark"]

    w_box = 1.55 * inch
    h_box = 1.35 * inch
    left = cx - w_box / 2
    bottom = cy - h_box / 2

    c.setStrokeColor(gold_light)
    c.setLineWidth(0.75)
    c.roundRect(left, bottom, w_box, h_box, 8, fill=0, stroke=1)

    c.setFillColor(text)
    day_size = fonts.get("date_day_size", 36)
    c.setFont(body_font, day_size)
    dw = c.stringWidth(day, body_font, day_size)
    c.drawString(cx - dw / 2, cy + 0.12 * inch, day)

    month_size = fonts.get("date_month_size", 11)
    c.setFont(body_font, month_size)
    c.setFillColor(gold)
    mw = c.stringWidth(month, body_font, month_size)
    c.drawString(cx - mw / 2, cy - 0.08 * inch, month)

    year_size = fonts.get("date_year_size", 10)
    c.setFillColor(colors["text_light"])
    c.setFont(body_font, year_size)
    yw = c.stringWidth(year, body_font, year_size)
    c.drawString(cx - yw / 2, cy - 0.28 * inch, year)

    return w_box, h_box
