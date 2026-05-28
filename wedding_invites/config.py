"""Load and validate invitation configuration."""

import csv
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dateutil import parser as date_parser


class ConfigError(Exception):
    """Raised when configuration is invalid."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


@dataclass
class GuestEntry:
    guest_names: str


@dataclass
class AppConfig:
    wedding: Dict[str, Any]
    output_directory: str
    guests: List[GuestEntry] = field(default_factory=list)


def _require_string(data: Dict[str, Any], key: str, label: str) -> str:
    value = data.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ConfigError(f"Please add {label} in your config file (field: {key}).")
    return str(value).strip()


def format_wedding_date(date_input: str) -> tuple[str, str, str]:
    """
    Parse flexible date input and return (day, month, year) for display.
    Display month is uppercase abbreviated (e.g. JAN).
    """
    try:
        parsed = date_parser.parse(date_input, dayfirst=True)
    except (ValueError, TypeError) as exc:
        raise ConfigError(
            f"We could not understand the wedding date '{date_input}'. "
            "Try formats like '15 June 2026', '2026-06-15', or '15/06/2026'."
        ) from exc

    day = f"{parsed.day:02d}"
    month = parsed.strftime("%B").upper()
    year = str(parsed.year)
    return day, month, year


def _load_guests_from_csv(csv_path: str) -> List[GuestEntry]:
    path = Path(csv_path)
    if not path.exists():
        raise ConfigError(
            f"The guest list file was not found: {csv_path}\n"
            "Check the path in guests_file or create guests.csv from guests.example.csv."
        )

    guests: List[GuestEntry] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ConfigError(f"The guest list file '{csv_path}' appears to be empty.")

        name_column = None
        for candidate in ("guest_names", "name", "names", "guest"):
            if candidate in reader.fieldnames:
                name_column = candidate
                break

        if name_column is None:
            raise ConfigError(
                f"The guest list file '{csv_path}' needs a column named guest_names "
                "(or name / names / guest)."
            )

        for row_num, row in enumerate(reader, start=2):
            name = (row.get(name_column) or "").strip()
            if name:
                guests.append(GuestEntry(guest_names=name))
            elif any((v or "").strip() for v in row.values()):
                raise ConfigError(
                    f"Row {row_num} in '{csv_path}' is missing a guest name."
                )

    if not guests:
        raise ConfigError(
            f"No guests were found in '{csv_path}'. Add at least one name."
        )

    return guests


def load_config(config_path: str = "config.yaml") -> AppConfig:
    """Load and validate configuration from YAML (and optional CSV guests)."""
    if not os.path.exists(config_path):
        raise ConfigError(
            f"We could not find '{config_path}'.\n"
            "Copy config.example.yaml to config.yaml and fill in your wedding details."
        )

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(
            f"'{config_path}' has a formatting problem. "
            "Check indentation and colons — YAML is sensitive to spacing."
        ) from exc

    if not isinstance(raw, dict):
        raise ConfigError(f"'{config_path}' should start with wedding:, output:, and guests: sections.")

    wedding = raw.get("wedding")
    if not isinstance(wedding, dict):
        raise ConfigError("Add a 'wedding:' section with bride_name, groom_name, date, and venue details.")

    bride_name = _require_string(wedding, "bride_name", "the bride's name")
    groom_name = _require_string(wedding, "groom_name", "the groom's name")
    date_raw = _require_string(wedding, "date", "the wedding date")
    time_str = _require_string(wedding, "time", "the ceremony time")

    day, month, year = format_wedding_date(date_raw)
    wedding["date_display"] = f"{day} {month} {year}"
    wedding["date_parts"] = (day, month, year)
    wedding["bride_name"] = bride_name
    wedding["groom_name"] = groom_name
    wedding["time"] = time_str

    venue = wedding.get("venue")
    if not isinstance(venue, dict):
        raise ConfigError(
            "Add a 'venue:' block under wedding with name, address_1, address_2, and postcode."
        )

    venue_name = _require_string(venue, "name", "the venue name")
    venue["name"] = venue_name
    venue["address_1"] = str(venue.get("address_1") or "").strip()
    venue["address_2"] = str(venue.get("address_2") or "").strip()
    venue["postcode"] = str(venue.get("postcode") or "").strip()

    wedding["reception_note"] = str(
        wedding.get("reception_note") or "Reception to follow"
    ).strip()

    output = raw.get("output") or {}
    output_dir = str(output.get("directory") or "./generated_invitations").strip()

    guests: List[GuestEntry] = []
    guests_file = raw.get("guests_file")
    if guests_file:
        guests = _load_guests_from_csv(str(guests_file))
    else:
        guest_list = raw.get("guests")
        if not guest_list:
            raise ConfigError(
                "Add at least one guest under 'guests:' or set guests_file to a CSV file."
            )
        if not isinstance(guest_list, list):
            raise ConfigError("'guests:' should be a list, with one entry per invited guest.")

        for index, guest in enumerate(guest_list, start=1):
            if not isinstance(guest, dict):
                raise ConfigError(f"Guest #{index} is not formatted correctly.")
            name = (guest.get("guest_names") or "").strip()
            if not name:
                raise ConfigError(
                    f"Guest #{index} is missing guest_names — add the name(s) to print on the invitation."
                )
            guests.append(GuestEntry(guest_names=name))

    return AppConfig(
        wedding=wedding,
        output_directory=output_dir,
        guests=guests,
    )


def flatten_invitation_data(wedding_data: Dict[str, Any], guest: GuestEntry) -> Dict[str, Any]:
    """Merge wedding and guest fields for the PDF generator."""
    data = dict(wedding_data)
    data["guest_names"] = guest.guest_names
    return data
