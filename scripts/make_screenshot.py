#!/usr/bin/env python3
"""Generate README screenshot from a preview PDF."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT = ROOT / "screenshots" / "example_invitation.png"


def main() -> int:
    sys.path.insert(0, str(ROOT))
    subprocess.run([sys.executable, str(ROOT / "generate.py"), "--preview"], check=True)

    preview_dir = ROOT / "generated_invitations"
    pdfs = sorted(preview_dir.glob("preview-*.pdf"))
    if not pdfs:
        print("No preview PDF found.", file=sys.stderr)
        return 1

    try:
        from pdf2image import convert_from_path
    except ImportError:
        from PIL import Image

        # Fallback: use reportlab-only — render via Pillow from PDF needs poppler
        # Try pymupdf if available
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(pdfs[0])
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
            pix.save(str(SCREENSHOT))
            print(f"Wrote {SCREENSHOT}")
            return 0
        except ImportError:
            pass

        print(
            "Install PyMuPDF (pip install pymupdf) or poppler + pdf2image for screenshots.",
            file=sys.stderr,
        )
        return 1

    images = convert_from_path(pdfs[0], dpi=150)
    SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(SCREENSHOT, "PNG")
    print(f"Wrote {SCREENSHOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
