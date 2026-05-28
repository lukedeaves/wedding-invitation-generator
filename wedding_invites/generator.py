"""PDF invitation generator."""

import os
from typing import Dict, Optional

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from wedding_invites import fonts
from wedding_invites.design import load_design
from wedding_invites.text_layout import (
    content_width,
    draw_centered_paragraph,
    draw_centered_text,
    fit_font_size,
)


class WeddingInvitationGenerator:
    """Generates personalized wedding invitation PDFs."""

    def __init__(
        self,
        output_directory: str = "./generated_invitations",
        design_path: Optional[str] = None,
    ):
        fonts.register_fonts()
        self.design = load_design(design_path)
        self.page_width, self.page_height = self.design["page_size"]
        self.margin = self.design["layout"]["margin_inches"] * inch
        self.content_w = content_width(
            self.page_width,
            self.margin,
            self.design["layout"]["content_width_inches"],
        )
        self.output_directory = output_directory
        self.colors = self.design["colors"]
        self.fonts = self.design["fonts"]
        self.copy = self.design["copy"]

    def _draw_decorative_border(self, c: canvas.Canvas) -> None:
        c.setStrokeColor(self.colors["gold"])
        c.setLineWidth(1)
        margin = 0.5 * inch
        corner_size = 0.3 * inch

        corners = [
            (margin, self.page_height - margin, 1, -1),
            (self.page_width - margin, self.page_height - margin, -1, -1),
            (margin, margin, 1, 1),
            (self.page_width - margin, margin, -1, 1),
        ]
        for x, y, dx, dy in corners:
            c.line(x, y, x + dx * corner_size, y)
            c.line(x, y, x, y + dy * corner_size)

    def _draw_top_graphic(self, c: canvas.Canvas) -> None:
        center_x = self.page_width / 2
        top_y = self.page_height - 1.45 * inch

        c.setStrokeColor(self.colors["gold"])
        c.setFillColor(self.colors["gold"])
        c.setLineWidth(1.5)

        size = 0.35 * inch
        diamond = [
            (center_x, top_y + size / 2),
            (center_x + size / 2, top_y),
            (center_x, top_y - size / 2),
            (center_x - size / 2, top_y),
        ]
        path = c.beginPath()
        path.moveTo(*diamond[0])
        for point in diamond[1:]:
            path.lineTo(*point)
        path.close()
        c.drawPath(path, fill=1)

        line_length = 1.1 * inch
        c.line(center_x - line_length, top_y, center_x - size / 2 - 0.08 * inch, top_y)
        c.line(center_x + size / 2 + 0.08 * inch, top_y, center_x + line_length, top_y)
        for offset in (-line_length, line_length, -line_length / 2, line_length / 2):
            c.circle(center_x + offset, top_y, 2.5, fill=1)

    def _draw_text_content(self, c: canvas.Canvas, invitation_data: Dict) -> None:
        y = self.page_height - 2.85 * inch
        script = fonts.script_font()
        body = fonts.body_font()
        body_italic = fonts.body_italic_font()

        guest_names = invitation_data.get("guest_names") or self.copy["default_guest"]
        y = draw_centered_paragraph(
            c,
            guest_names,
            y,
            self.page_width,
            self.content_w,
            body,
            self.fonts["guest_size"],
            self.colors["text_dark"],
        )

        invite_line = self.copy["invitation_line"]
        y = draw_centered_text(
            c,
            invite_line,
            y - 0.1 * inch,
            self.page_width,
            body,
            self.fonts["invite_line_size"],
            self.colors["text_light"],
        )

        bride_name = invitation_data.get("bride_name", "")
        groom_name = invitation_data.get("groom_name", "")
        name_font = script
        name_color = self.colors["gold"]

        for name in (bride_name, groom_name):
            name_size = fit_font_size(
                c,
                name,
                name_font,
                self.fonts["name_size"],
                self.fonts["name_min_size"],
                self.content_w,
            )
            y = draw_centered_text(
                c, name, y - 0.15 * inch, self.page_width, name_font, name_size, name_color
            )
            if name == bride_name:
                connector = self.copy["connector"]
                y = draw_centered_text(
                    c,
                    connector,
                    y - 0.05 * inch,
                    self.page_width,
                    body_italic,
                    self.fonts["and_size"],
                    self.colors["text_light"],
                )

        y -= 0.35 * inch
        line_x = self.page_width / 2
        line_top = y
        line_bottom = y - 2.0 * inch
        c.setStrokeColor(self.colors["gold"])
        c.setLineWidth(0.75)
        c.line(line_x, line_top, line_x, line_bottom)
        line_center_y = (line_top + line_bottom) / 2

        date_parts = invitation_data.get("date_parts")
        if not date_parts:
            date_str = invitation_data.get("date_display") or invitation_data.get("date", "")
            parts = str(date_str).split()
            date_parts = (parts[0], parts[1], parts[2]) if len(parts) >= 3 else ("01", "JAN", "2026")

        day, month, year = date_parts
        c.setFillColor(self.colors["text_dark"])
        date_font = body
        date_size = self.fonts["date_day_size"]
        spacing = 0.28 * inch

        day_w = c.stringWidth(day, date_font, date_size)
        month_w = c.stringWidth(month, date_font, date_size)
        year_w = c.stringWidth(year, date_font, date_size - 2)
        max_w = max(day_w, month_w, year_w)
        date_x = line_x - max_w / 2 - 0.45 * inch
        block_h = 2 * spacing
        date_y = line_center_y + block_h / 2

        c.setFont(date_font, date_size)
        c.drawString(date_x - day_w / 2, date_y, day)
        c.setFont(date_font, date_size - 1)
        c.drawString(date_x - month_w / 2, date_y - spacing, month)
        c.drawString(date_x - year_w / 2, date_y - 2 * spacing, year)

        venue = invitation_data.get("venue") or {}
        time_str = invitation_data.get("time", "")
        venue_lines = [
            time_str,
            venue.get("name", ""),
            venue.get("address_1", ""),
            venue.get("address_2", ""),
            venue.get("postcode", ""),
        ]
        venue_lines = [line for line in venue_lines if line]

        detail_size = self.fonts["detail_size"]
        c.setFont(body, detail_size)
        c.setFillColor(self.colors["text_dark"])
        venue_spacing = 0.26 * inch
        venue_block_h = (len(venue_lines) - 1) * venue_spacing if venue_lines else 0
        venue_y = line_center_y + venue_block_h / 2
        detail_x = line_x + 0.45 * inch

        for i, line in enumerate(venue_lines):
            c.drawString(detail_x, venue_y - i * venue_spacing, line)

        reception = invitation_data.get("reception_note") or self.copy["default_reception"]
        draw_centered_text(
            c,
            reception,
            1.15 * inch,
            self.page_width,
            body_italic,
            self.fonts["reception_size"],
            self.colors["text_light"],
        )

    def generate_invitation(
        self, invitation_data: Dict, output_filename: Optional[str] = None
    ) -> str:
        if output_filename is None:
            output_filename = "wedding-invitation.pdf"

        os.makedirs(self.output_directory, exist_ok=True)
        output_path = os.path.join(self.output_directory, output_filename)

        c = canvas.Canvas(output_path, pagesize=self.design["page_size"])
        c.setTitle(
            f"Wedding invitation — {invitation_data.get('guest_names', 'Guest')}"
        )
        c.setAuthor(
            f"{invitation_data.get('bride_name', '')} & {invitation_data.get('groom_name', '')}"
        )

        c.setFillColor(self.colors["background"])
        c.rect(0, 0, self.page_width, self.page_height, fill=1, stroke=0)

        self._draw_decorative_border(c)
        self._draw_top_graphic(c)
        self._draw_text_content(c, invitation_data)
        c.save()

        return output_path
