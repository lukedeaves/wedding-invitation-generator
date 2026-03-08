# Wedding Invitation PDF Generator

A Python utility to generate personalized wedding invitations with elegant botanical design elements, matching the sophisticated style of the provided template.

![Example Invitation](screenshots/example_invitation.png)

## Features

- **Elegant Design**: Clean layout with gold decorative elements and sophisticated typography
- **Personalized Output**: Each invitation includes guest names and is specifically named for the intended recipient
- **Easy Configuration**: Simple YAML-based configuration - just edit `config.yaml` and run the script
- **Professional Typography**: Sophisticated font styling with elegant script fonts for names
- **Batch Generation**: Create multiple personalized invitations at once
- **Decorative Elements**: Beautiful top graphic and corner flourishes

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

1. **Edit `config.yaml`** with your wedding details:
   ```yaml
   wedding:
     bride_name: "Your Bride Name"
     groom_name: "Your Groom Name"
     date: "01 JAN 2026"
     time: "12:30"
     venue:
       name: "Your Venue Name"
       address_1: "Address Line 1"
       address_2: "City"
       postcode: "POSTCODE"
     reception_note: "Reception to follow"

   output:
     directory: "./generated_invitations"

   guests:
     - guest_names: "Guest Name 1"
     - guest_names: "Guest Name 2"
   ```

2. **Run the generator**:
   ```bash
   python generate.py
   ```

3. **Find your invitations** in the `generated_invitations/` directory (or your configured output directory)

That's it! The script will generate a personalized PDF invitation for each guest listed in your `config.yaml` file.

## Customization Options

All customization is done through the `config.yaml` file. The following fields are available:

### Wedding Details
- `wedding.bride_name`: Bride's name (displayed in elegant script)
- `wedding.groom_name`: Groom's name (displayed in elegant script)
- `wedding.date`: Wedding date (format: "DD MMM YYYY", e.g., "01 JAN 2026")
- `wedding.time`: Ceremony time (e.g., "12:30")
- `wedding.venue.name`: Name of the venue
- `wedding.venue.address_1`: First line of venue address
- `wedding.venue.address_2`: Second line of venue address (city)
- `wedding.venue.postcode`: Venue postcode
- `wedding.reception_note`: Note about reception (e.g., "Reception to follow")

### Output Settings
- `output.directory`: Directory where generated PDFs will be saved (default: `./generated_invitations`)

### Guest List
- `guests`: List of guest entries, each with:
  - `guest_names`: Names of the invited guests (displayed at the top of invitation)

### Design Elements
The generator automatically includes:
- Elegant decorative border with corner flourishes
- Beautiful top graphic with ornamental design
- Gold decorative elements and accents
- Elegant typography with script fonts for names
- Professional layout with clean, sophisticated design
- Cream background with gold accents

## Output

Generated PDFs are saved to the configured output directory (default: `generated_invitations/`) with descriptive filenames that include the guest names.

Example output filename: `Sample Guest wedding invitation.pdf`

## File Structure

```
wedding-invitations/
├── config.yaml                    # Configuration file (edit this!)
├── generate.py                    # Main generator script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── screenshots/                   # Example output screenshots
│   └── example_invitation.png     # Example invitation preview
└── generated_invitations/         # Output directory (created automatically)
    ├── Guest Name 1 wedding invitation.pdf
    ├── Guest Name 2 wedding invitation.pdf
    └── ...
```

## Design Details

The generator creates an elegant wedding invitation design featuring:

- **Color Palette**: Cream background with sophisticated gold accents
- **Typography**: Mix of elegant script fonts for names and clean sans-serif for details
- **Layout**: Centered text with decorative elements and professional spacing
- **Elements**: Ornamental top graphic, corner flourishes, clean lines, and gold accents

## Technical Details

- Python 3.7+

### Modules Used

- reportlab 4.0.0+
- Pillow 10.0.0+
- pyyaml 6.0.0+

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.