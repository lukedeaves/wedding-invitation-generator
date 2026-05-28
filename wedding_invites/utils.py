"""Shared utilities."""

import os
import re
import subprocess
import sys
from pathlib import Path


def slugify(text: str, max_length: int = 80) -> str:
    """Convert text to a safe filename segment."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    text = text.strip("-")
    if not text:
        text = "guest"
    return text[:max_length]


def invitation_filename(guest_names: str) -> str:
    """Build a filesystem-safe PDF filename for a guest."""
    return f"{slugify(guest_names)}-wedding-invitation.pdf"


def open_output_folder(directory: str) -> bool:
    """Open the output directory in the system file manager."""
    path = Path(directory).resolve()
    path.mkdir(parents=True, exist_ok=True)

    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        elif sys.platform == "win32":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
        return True
    except OSError:
        return False
