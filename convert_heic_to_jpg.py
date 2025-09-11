#!/usr/bin/env python3
"""
Batch-convert all .heic images in a folder to .jpg using ImageMagick (magick).

Usage examples:
  python3 convert_heic_to_jpg.py                 # convert *.heic in current dir
  python3 convert_heic_to_jpg.py /path/to/folder # convert in specific dir
  python3 convert_heic_to_jpg.py --recursive     # include subfolders
  python3 convert_heic_to_jpg.py --quality 85    # set JPEG quality (default 85)
  python3 convert_heic_to_jpg.py --overwrite     # overwrite existing .jpg files
  python3 convert_heic_to_jpg.py --dry-run       # show actions without converting

Requires: ImageMagick installed and `magick` available on PATH
  macOS (Homebrew):  brew install imagemagick
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import Iterable, List


def find_magick_executable() -> str:
    """Return the ImageMagick executable name to use, or raise if missing."""
    from shutil import which

    # On most platforms the command is `magick`; on some it's `convert` (legacy)
    for candidate in ("magick", "convert"):
        if which(candidate):
            return candidate
    raise RuntimeError(
        "ImageMagick not found. Install it (e.g., `brew install imagemagick`) and ensure `magick` is on PATH."
    )


def iter_heic_files(root: Path, recursive: bool) -> Iterable[Path]:
    patterns: List[str] = ["*.heic", "*.HEIC"]
    if recursive:
        for pattern in patterns:
            yield from root.rglob(pattern)
    else:
        for pattern in patterns:
            yield from root.glob(pattern)


def convert_file(magick: str, src: Path, dst: Path, quality: int, overwrite: bool, dry_run: bool) -> bool:
    """Convert one HEIC file to JPG. Returns True on success, False otherwise."""
    if dst.exists() and not overwrite:
        print(f"[skip] {dst} already exists (use --overwrite to replace)")
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)

    cmd = [magick, str(src), "-quality", str(quality), str(dst)]
    if dry_run:
        print("[dry-run] ", " ".join(cmd))
        return True
    try:
        subprocess.run(cmd, check=True)
        print(f"[ok] {src.name} -> {dst.name}")
        return True
    except subprocess.CalledProcessError as exc:
        print(f"[error] Failed: {' '.join(cmd)}\n  {exc}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert .heic images to .jpg using ImageMagick")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to scan (default: current directory)")
    parser.add_argument("--recursive", action="store_true", help="Recurse into subfolders")
    parser.add_argument("--quality", type=int, default=85, help="JPEG quality 1-100 (default: 85)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .jpg files")
    parser.add_argument("--dry-run", action="store_true", help="Only print what would be done")
    args = parser.parse_args()

    try:
        magick = find_magick_executable()
    except RuntimeError as e:
        print(str(e))
        return 1

    root = Path(args.folder).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Folder not found or not a directory: {root}")
        return 1

    heic_files = list(iter_heic_files(root, args.recursive))
    if not heic_files:
        print("No .heic images found.")
        return 0

    total = 0
    success = 0
    for heic in heic_files:
        total += 1
        jpg = heic.with_suffix(".jpg")
        if convert_file(magick, heic, jpg, args.quality, args.overwrite, args.dry_run):
            success += 1

    print(f"Done: {success}/{total} converted.")
    return 0 if success == total else 2


if __name__ == "__main__":
    sys.exit(main())


