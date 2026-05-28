"""PDF invitation generator — garden-formal editorial layout."""

import os
from typing import Dict, Optional

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from wedding_invites import fonts
from wedding_invites.artwork import (
    draw_all_corner_botanicals,
    draw_all_corner_flourishes,
    draw_date_medallion,
    draw_header_emblem,
    draw_layered_frame,
    draw_ornament_divider,
)
from wedding_invites.design import load_design
from wedding_invites.text_layout import (
    content_width,
    draw_centered_paragraph,
    draw_centered_spaced_caps,
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
        self.frame_inset = self.design["layout"]["frame_inset_inches"] * inch
        self.content_w = content_width(
            self.page_width,
            self.margin,
            self.design["layout"]["content_width_inches"],
        )
        self.output_directory = output_directory
        self.colors = self.design["colors"]
        self.fonts = self.design["fonts"]
        self.copy = self.design["copy"]

    def _draw_background(self, c: canvas.Canvas) -> None:
        c.setFillColor(self.colors["background"])
        c.rect(0, 0, self.page_width, self.page_height, fill=1, stroke=0)

    def _draw_text_content(self, c: canvas.Canvas, invitation_data: Dict) -> None:
        script = fonts.script_font()
        body = fonts.body_font()
        body_italic = fonts.body_italic_font()
        gold = self.colors["gold"]
        text_dark = self.colors["text_dark"]
        text_light = self.colors["text_light"]

        content_inset = self.frame_inset + 0.38 * inch
        y = self.page_height - content_inset - 0.55 * inch

        # Header emblem
        draw_header_emblem(c, y, self.page_width, self.colors)
        y -= 0.55 * inch

        draw_ornament_divider(c, y, self.page_width, self.colors, width=3.2 * inch)
        y -= 0.38 * inch

        # Guest honour line
        guest = invitation_data.get("guest_names") or self.copy["default_guest"]
        prefix = (self.copy.get("guest_prefix") or "").strip()
        guest_line = f"{prefix} {guest}".strip() if prefix else guest
        y = draw_centered_spaced_caps(
            c,
            guest_line,
            y,
            self.page_width,
            body,
            self.fonts["guest_size"],
            text_dark,
            tracking=self.fonts.get("guest_tracking", 2.5),
        )
        y -= 0.12 * inch

        draw_ornament_divider(c, y, self.page_width, self.colors, width=2.8 * inch, style="dot")
        y -= 0.42 * inch

        # Invitation copy (may include line break)
        invite = self.copy["invitation_line"]
        y = draw_centered_paragraph(
            c,
            invite,
            y,
            self.page_width,
            self.content_w * 0.92,
            body_italic,
            self.fonts["invite_line_size"],
            text_light,
            leading=self.fonts["invite_line_size"] * 1.45,
        )
        y -= 0.2 * inch

        # Couple names with ornamental ampersand
        bride = invitation_data.get("bride_name", "")
        groom = invitation_data.get("groom_name", "")

        for index, name in enumerate((bride, groom)):
            if index == 1:
                amp_size = self.fonts["ampersand_size"]
                y -= 0.08 * inch
                draw_centered_text(
                    c, "&", y, self.page_width, script, amp_size, gold
                )
                y -= amp_size * 0.95

            name_size = fit_font_size(
                c,
                name,
                script,
                self.fonts["name_size"],
                self.fonts["name_min_size"],
                self.content_w,
            )
            y = draw_centered_text(
                c, name, y - 0.08 * inch, self.page_width, script, name_size, gold
            )

        y -= 0.28 * inch
        draw_ornament_divider(c, y, self.page_width, self.colors, width=4.0 * inch)
        y -= 0.55 * inch

        # Date medallion + time & venue column
        date_parts = invitation_data.get("date_parts")
        if not date_parts:
            date_str = invitation_data.get("date_display") or invitation_data.get("date", "")
            parts = str(date_str).split()
            date_parts = (parts[0], parts[1], parts[2]) if len(parts) >= 3 else ("01", "JANUARY", "2026")

        day, month, year = date_parts
        cx = self.page_width / 2
        medallion_y = y - 0.55 * inch
        draw_date_medallion(
            c, cx, medallion_y, day, month, year, self.fonts, self.colors, body
        )

        y = medallion_y - 0.95 * inch

        # Time
        time_str = invitation_data.get("time", "")
        time_prefix = self.copy.get("time_prefix", "at")
        time_line = f"{time_prefix} {time_str}".strip() if time_str else ""
        if time_line:
            y = draw_centered_spaced_caps(
                c,
                time_line,
                y,
                self.page_width,
                body_italic,
                self.fonts["time_size"],
                text_dark,
                tracking=1.8,
            )
            y -= 0.08 * inch

        draw_ornament_divider(
            c, y, self.page_width, self.colors, width=2.4 * inch, style="dot"
        )
        y -= 0.35 * inch

        # Venue block
        venue = invitation_data.get("venue") or {}
        venue_name = venue.get("name", "")
        if venue_name:
            name_size = self.fonts["venue_name_size"]
            y = draw_centered_spaced_caps(
                c,
                venue_name,
                y,
                self.page_width,
                body,
                name_size,
                text_dark,
                tracking=2.0,
            )
            y -= 0.06 * inch

        address_lines = [
            venue.get("address_1", ""),
            venue.get("address_2", ""),
            venue.get("postcode", ""),
        ]
        address_lines = [line for line in address_lines if line]

        for line in address_lines:
            y = draw_centered_text(
                c,
                line,
                y,
                self.page_width,
                body,
                self.fonts["detail_size"],
                text_light,
            )
            y += 0.04 * inch

        # Footer
        footer_y = content_inset + 0.95 * inch
        draw_ornament_divider(
            c, footer_y + 0.35 * inch, self.page_width, self.colors, width=3.0 * inch
        )

        reception = invitation_data.get("reception_note") or self.copy["default_reception"]
        draw_centered_spaced_caps(
            c,
            reception,
            footer_y,
            self.page_width,
            body_italic,
            self.fonts["reception_size"],
            text_light,
            tracking=1.5,
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

        self._draw_background(c)
        draw_layered_frame(c, self.page_width, self.page_height, self.colors, self.frame_inset)
        inset = self.frame_inset + 0.05 * inch
        draw_all_corner_botanicals(c, self.page_width, self.page_height, inset, self.colors)
        draw_all_corner_flourishes(c, self.page_width, self.page_height, inset, self.colors)
        self._draw_text_content(c, invitation_data)
        c.save()

        return output_path
