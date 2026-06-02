#!/usr/bin/env python3
"""
Wedding Invitation PDF Generator

Create personalized wedding invitation PDFs from config.yaml.

Examples:
    python generate.py
    python generate.py --preview
    python generate.py --open
    python generate.py --config my-wedding.yaml --design design.yaml
"""

from __future__ import annotations

import argparse
import os
import sys

from wedding_invites.config import AppConfig, ConfigError, flatten_invitation_data, load_config
from wedding_invites.generator import WeddingInvitationGenerator
from wedding_invites.utils import invitation_filename, open_output_folder


def _print_header() -> None:
    print()
    print("  Wedding Invitation Generator")
    print("  ----------------------------")


def _print_success(count: int, output_dir: str, opened: bool) -> None:
    abs_dir = os.path.abspath(output_dir)
    print()
    print(f"  Done! Created {count} invitation{'s' if count != 1 else ''}.")
    print(f"  Your PDFs are in:\n  {abs_dir}")
    if opened:
        print("  (Opened that folder for you.)")
    print()


def run_generation(
    config: AppConfig,
    *,
    design_path: str | None = None,
    preview_only: bool = False,
    open_folder: bool = False,
) -> int:
    guests = config.guests[:1] if preview_only else config.guests
    total = len(guests)

    if preview_only:
        print("  Creating a preview invitation (first guest only)...")
    else:
        print(f"  Creating {total} invitation{'s' if total != 1 else ''}...")

    generator = WeddingInvitationGenerator(
        output_directory=config.output_directory,
        design_path=design_path,
    )

    generated = 0
    for index, guest in enumerate(guests, start=1):
        label = guest.guest_names
        if not preview_only and total > 1:
            print(f"  [{index}/{total}] {label}...", end=" ", flush=True)
        else:
            print(f"  {label}...", end=" ", flush=True)

        data = flatten_invitation_data(config.wedding, guest)
        filename = invitation_filename(guest.guest_names)
        if preview_only:
            filename = "preview-" + filename

        try:
            path = generator.generate_invitation(data, filename)
            generated += 1
            print("saved")
            if preview_only:
                print(f"  Preview file: {path}")
        except Exception as exc:
            print("failed")
            print(f"  Could not create invitation for {label}: {exc}")
            return 1

    opened = False
    if open_folder and generated > 0:
        opened = open_output_folder(config.output_directory)

    if not preview_only or generated > 0:
        _print_success(generated, config.output_directory, opened)

    return 0 if generated == total else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate personalized wedding invitation PDFs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Quick start:\n"
            "  1. Copy config.example.yaml to config.yaml\n"
            "  2. Fill in your wedding details and guest list\n"
            "  3. Run: python generate.py\n"
        ),
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to your wedding config file (default: config.yaml)",
    )
    parser.add_argument(
        "-d",
        "--design",
        default=None,
        help="Path to design.yaml for colors and wording (optional)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate only the first guest's invitation to check the layout",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the output folder when finished",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _print_header()

    try:
        print(f"  Reading {args.config}...")
        config = load_config(args.config)
    except ConfigError as exc:
        print()
        print(f"  {exc.message}")
        print()
        print("  Tip: copy config.example.yaml to config.yaml and edit your details.")
        return 1

    return run_generation(
        config,
        design_path=args.design,
        preview_only=args.preview,
        open_folder=args.open,
    )


if __name__ == "__main__":
    sys.exit(main())
