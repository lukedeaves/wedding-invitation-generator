#!/usr/bin/env python3
"""
Wedding Invitation PDF Generator

A Python utility to generate personalized wedding invitations with botanical design elements.
Based on the elegant design with green foliage, gold accents, and sophisticated typography.

Usage:
    python generate.py

The script reads configuration from config.yaml and generates personalized invitations
for each guest listed in the configuration file.
"""

import os
from datetime import datetime
from typing import Dict
import yaml
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class WeddingInvitationGenerator:
    """
    Generates personalized wedding invitation PDFs with botanical design elements.
    """
    
    def __init__(self, output_directory: str = "./generated_invitations"):
        """
        Initialize the generator.
        
        Args:
            output_directory: Directory where generated PDFs will be saved
        """
        # Color palette
        self.colors = {
            'background': Color(0.98, 0.98, 0.96),  # Cream background
            'dark_green': Color(0.2, 0.4, 0.3),     # Dark green for leaves
            'medium_green': Color(0.3, 0.5, 0.4),   # Medium green
            'light_green': Color(0.4, 0.6, 0.5),    # Light green
            'gold': Color(0.8, 0.7, 0.3),           # Gold for dots and accents
            'text_dark': Color(0.2, 0.2, 0.2),      # Dark text
            'text_light': Color(0.4, 0.4, 0.4),     # Light text
        }
        
        # Page dimensions
        self.page_width, self.page_height = letter
        self.margin = 0.75 * inch
        self.output_directory = output_directory
        
    def _draw_decorative_border(self, c: canvas.Canvas) -> None:
        """Draw a simple decorative border around the invitation."""
        c.setStrokeColor(self.colors['gold'])
        c.setLineWidth(1)
        
        # Draw elegant corner flourishes
        margin = 0.5 * inch
        corner_size = 0.3 * inch
        
        # Top left corner
        c.line(margin, self.page_height - margin, margin + corner_size, self.page_height - margin)
        c.line(margin, self.page_height - margin, margin, self.page_height - margin - corner_size)
        
        # Top right corner
        c.line(self.page_width - margin, self.page_height - margin, self.page_width - margin - corner_size, self.page_height - margin)
        c.line(self.page_width - margin, self.page_height - margin, self.page_width - margin, self.page_height - margin - corner_size)
        
        # Bottom left corner
        c.line(margin, margin, margin + corner_size, margin)
        c.line(margin, margin, margin, margin + corner_size)
        
        # Bottom right corner
        c.line(self.page_width - margin, margin, self.page_width - margin - corner_size, margin)
        c.line(self.page_width - margin, margin, self.page_width - margin, margin + corner_size)
    
    def _draw_top_graphic(self, c: canvas.Canvas) -> None:
        """Draw an elegant graphic at the top of the invitation."""
        center_x = self.page_width / 2
        top_y = self.page_height - 1.5 * inch
        
        # Draw elegant flourish design
        c.setStrokeColor(self.colors['gold'])
        c.setFillColor(self.colors['gold'])
        c.setLineWidth(2)
        
        # Central ornamental design
        # Draw a decorative diamond/star pattern
        size = 0.4 * inch
        
        # Central diamond
        diamond_points = [
            (center_x, top_y + size/2),  # top
            (center_x + size/2, top_y),  # right
            (center_x, top_y - size/2),  # bottom
            (center_x - size/2, top_y)   # left
        ]
        
        path = c.beginPath()
        path.moveTo(*diamond_points[0])
        for point in diamond_points[1:]:
            path.lineTo(*point)
        path.close()
        c.drawPath(path, fill=1)
        
        # Decorative lines extending from center
        line_length = 1.2 * inch
        
        # Horizontal decorative lines
        c.line(center_x - line_length, top_y, center_x - size/2 - 0.1*inch, top_y)
        c.line(center_x + size/2 + 0.1*inch, top_y, center_x + line_length, top_y)
        
        # Small decorative circles at line ends
        c.setFillColor(self.colors['gold'])
        c.circle(center_x - line_length, top_y, 3, fill=1)
        c.circle(center_x + line_length, top_y, 3, fill=1)
        
        # Additional small decorative elements
        c.circle(center_x - line_length/2, top_y, 2, fill=1)
        c.circle(center_x + line_length/2, top_y, 2, fill=1)
    
    def _draw_text_content(self, c: canvas.Canvas, invitation_data: Dict) -> None:
        """Draw all text content on the invitation."""
        # Guest names at the top
        guest_names = invitation_data.get('guest_names', 'Dear Guests')
        c.setFillColor(self.colors['text_dark'])
        c.setFont("Helvetica", 16)
        guest_width = c.stringWidth(guest_names, "Helvetica", 16)
        c.drawString((self.page_width - guest_width) / 2, 
                    self.page_height - 3.2 * inch, guest_names)
        
        # Wedding invitation text
        c.setFillColor(self.colors['text_light'])
        c.setFont("Helvetica", 14)
        c.drawString((self.page_width - c.stringWidth("You are invited to the wedding of", "Helvetica", 14)) / 2, 
                    self.page_height - 3.8 * inch, "You are invited to the wedding of")
        
        # Couple names (elegant script-style) - increased spacing from invitation text
        c.setFillColor(self.colors['gold'])
        c.setFont("Helvetica-Oblique", 36)
        
        bride_name = invitation_data.get('bride_name', 'Bride Name')
        groom_name = invitation_data.get('groom_name', 'Groom Name')
        
        # Increased spacing: larger gap between invitation text and names
        # Gap 1: 3.8 to 5.0 = 1.2 inches (increased)
        # Names section: 5.0 to 6.2 = 1.2 inches
        # Gap 2: 6.2 to 7.4 = 1.2 inches (to divider line)
        
        # Draw bride's name
        bride_width = c.stringWidth(bride_name, "Helvetica-Oblique", 36)
        c.drawString((self.page_width - bride_width) / 2, 
                    self.page_height - 5.0 * inch, bride_name)
        
        # Draw "and"
        c.setFont("Helvetica-Oblique", 20)
        and_width = c.stringWidth("and", "Helvetica-Oblique", 20)
        c.drawString((self.page_width - and_width) / 2, 
                    self.page_height - 5.5 * inch, "and")
        
        # Draw groom's name
        c.setFont("Helvetica-Oblique", 36)
        groom_width = c.stringWidth(groom_name, "Helvetica-Oblique", 36)
        c.drawString((self.page_width - groom_width) / 2, 
                    self.page_height - 6.2 * inch, groom_name)
        
        # Event details
        c.setFillColor(self.colors['text_dark'])
        c.setFont("Helvetica", 12)
        
        # Date and time
        date_str = invitation_data.get('date', '01 JAN 2026')
        time_str = invitation_data.get('time', '12:30')
        
        # Draw vertical line - adjusted position to match new name spacing
        line_x = self.page_width / 2 - 0.5 * inch
        line_top = self.page_height - 7.4 * inch
        line_bottom = self.page_height - 9.4 * inch
        c.line(line_x, line_top, line_x, line_bottom)
        
        # Calculate vertical center of the line for alignment
        line_center_y = (line_top + line_bottom) / 2
        
        # Date on the left of the line - vertically centered
        c.setFont("Helvetica-Bold", 16)
        date_parts = date_str.split()
        if len(date_parts) >= 3:
            day, month, year = date_parts[0], date_parts[1], date_parts[2]
            
            # Calculate widths for centering
            day_width = c.stringWidth(day, "Helvetica-Bold", 16)
            month_width = c.stringWidth(month, "Helvetica-Bold", 16)
            year_width = c.stringWidth(year, "Helvetica-Bold", 16)
            max_date_width = max(day_width, month_width, year_width)
            
            # Center the date block vertically around line_center_y
            date_line_spacing = 0.25 * inch
            date_block_height = 2 * date_line_spacing  # Height of 3 lines with 2 gaps
            date_start_y = line_center_y + date_block_height / 2
            
            # Position date block center point (left of vertical line with margin)
            date_center_x = line_x - max_date_width / 2 - 20
            
            # Draw each date component centered around the common center point
            c.drawString(date_center_x - day_width / 2, date_start_y, day)
            c.drawString(date_center_x - month_width / 2, date_start_y - date_line_spacing, month)
            c.drawString(date_center_x - year_width / 2, date_start_y - (2 * date_line_spacing), year)
        
        # Time and venue details on the right of the line - vertically centered
        c.setFont("Helvetica", 12)
        
        # Handle venue as nested dict (from YAML) or flat dict (backward compatibility)
        if 'venue' in invitation_data:
            venue = invitation_data.get('venue', {})
            venue_name = venue.get('name')
            venue_address_1 = venue.get('address_1')
            venue_address_2 = venue.get('address_2')
            venue_postcode = venue.get('postcode')
        else:
            venue_name = invitation_data.get('venue_name')
            venue_address_1 = invitation_data.get('venue_address_1')
            venue_address_2 = invitation_data.get('venue_address_2')
            venue_postcode = invitation_data.get('venue_postcode')
        
        venue_details = [
            time_str,
            venue_name or 'Venue Name',
            venue_address_1 or 'Address Line 1',
            venue_address_2 or 'Address Line 2',
            venue_postcode or 'Postcode'
        ]
        
        # Filter out empty details and calculate total height
        filtered_details = [detail for detail in venue_details if detail]
        venue_line_spacing = 0.25 * inch  # Match date spacing
        venue_block_height = (len(filtered_details) - 1) * venue_line_spacing
        venue_start_y = line_center_y + venue_block_height / 2
        
        for i, detail in enumerate(filtered_details):
            c.drawString(line_x + 20, venue_start_y - (i * venue_line_spacing), detail)
        
        # Reception note - positioned inside the corner brackets
        c.setFont("Helvetica-Oblique", 11)
        c.setFillColor(self.colors['text_light'])
        reception_text = invitation_data.get('reception_note', 'Reception to follow')
        reception_width = c.stringWidth(reception_text, "Helvetica-Oblique", 11)
        # Position it near the bottom, inside the decorative border area
        c.drawString((self.page_width - reception_width) / 2, 
                    1.2 * inch, reception_text)
    
    def generate_invitation(self, invitation_data: Dict, output_filename: str = None) -> str:
        """
        Generate a wedding invitation PDF.
        
        Args:
            invitation_data: Dictionary containing invitation details
            output_filename: Optional custom filename, otherwise auto-generated
            
        Returns:
            Path to the generated PDF file
        """
        if output_filename is None:
            bride = invitation_data.get('bride_name', 'Bride').replace(' ', '_')
            groom = invitation_data.get('groom_name', 'Groom').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"wedding_invitation_{bride}_{groom}_{timestamp}.pdf"
        
        # Ensure output directory exists
        os.makedirs(self.output_directory, exist_ok=True)
        output_path = os.path.join(self.output_directory, output_filename)
        
        # Create PDF
        c = canvas.Canvas(output_path, pagesize=letter)
        
        # Set background color
        c.setFillColor(self.colors['background'])
        c.rect(0, 0, self.page_width, self.page_height, fill=1, stroke=0)
        
        # Draw decorative elements
        self._draw_decorative_border(c)
        self._draw_top_graphic(c)
        
        # Draw text content
        self._draw_text_content(c, invitation_data)
        
        # Save the PDF
        c.save()
        
        return output_path


def load_config(config_path: str = "config.yaml") -> Dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Dictionary containing configuration data
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def flatten_invitation_data(wedding_data: Dict, guest_data: Dict) -> Dict:
    """
    Flatten nested YAML structure into flat dict for generate_invitation method.
    
    Args:
        wedding_data: Wedding data from config (may contain nested venue)
        guest_data: Guest-specific data
        
    Returns:
        Flattened dictionary with all invitation fields
    """
    # Start with wedding data
    invitation_data = wedding_data.copy()
    
    # Extract venue if nested
    if 'venue' in invitation_data:
        venue = invitation_data.pop('venue')
        invitation_data['venue_name'] = venue.get('name', '')
        invitation_data['venue_address_1'] = venue.get('address_1', '')
        invitation_data['venue_address_2'] = venue.get('address_2', '')
        invitation_data['venue_postcode'] = venue.get('postcode', '')
    
    # Merge guest-specific data
    invitation_data.update(guest_data)
    
    return invitation_data


def main():
    """Main function to generate invitations from config.yaml."""
    try:
        # Load configuration
        print("Loading configuration from config.yaml...")
        config = load_config()
        
        # Extract sections
        wedding_data = config.get('wedding', {})
        output_config = config.get('output', {})
        guests = config.get('guests', [])
        
        if not guests:
            print("Warning: No guests found in configuration file.")
            return
        
        # Get output directory
        output_dir = output_config.get('directory', './generated_invitations')
        
        # Initialize generator
        generator = WeddingInvitationGenerator(output_directory=output_dir)
        
        # Generate invitations
        print(f"\nGenerating personalized wedding invitations...")
        print("=" * 50)
        
        generated_files = []
        for i, guest in enumerate(guests, 1):
            guest_names = guest.get('guest_names', f'Guest {i}')
            
            # Flatten data structure
            invitation_data = flatten_invitation_data(wedding_data, guest)
            
            # Generate filename
            filename = f"{guest_names} wedding invitation.pdf"
            
            try:
                output_path = generator.generate_invitation(invitation_data, filename)
                generated_files.append(output_path)
                print(f"✓ Generated invitation for {guest_names}")
                print(f"  File: {output_path}")
            except Exception as e:
                print(f"✗ Error generating invitation for {guest_names}: {e}")
        
        print("=" * 50)
        print(f"\nSuccessfully generated {len(generated_files)} invitation(s)")
        print(f"Output directory: {os.path.abspath(output_dir)}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure config.yaml exists in the current directory.")
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}")
        print("Please check that your YAML file is valid.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
