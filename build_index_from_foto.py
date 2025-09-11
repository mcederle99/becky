#!/usr/bin/env python3
"""
Generate index.json from all .jpg images inside the foto/ directory.

By default, scans ./foto (non-recursive) and writes ./index.json with paths
that include the folder prefix (e.g., "foto/image.jpg"). Only .jpg files are added.

Usage examples:
  python3 build_index_from_foto.py                   # scan ./foto, write ./index.json
  python3 build_index_from_foto.py --recursive      # include subfolders
  python3 build_index_from_foto.py --folder ./foto2 # scan custom folder
  python3 build_index_from_foto.py --out ./index.json
"""

import argparse
import json
from pathlib import Path
from typing import List


def list_jpg_files(root: Path, recursive: bool) -> List[Path]:
    patterns = [
        "**/*.jpg" if recursive else "*.jpg",
        "**/*.JPG" if recursive else "*.JPG",
        "**/*.JPEG" if recursive else "*.JPEG",
        "**/*.jpeg" if recursive else "*.jpeg",
        "**/*.PNG" if recursive else "*.PNG",
    ]
    results: List[Path] = []
    for pattern in patterns:
        results.extend(p for p in root.glob(pattern) if p.is_file())
    # De-duplicate while preserving order
    seen = set()
    unique: List[Path] = []
    for p in results:
        if p.resolve() in seen:
            continue
        seen.add(p.resolve())
        unique.append(p)
    return sorted(unique)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build index.json from .jpg files in a folder")
    parser.add_argument("--folder", default="./foto", help="Folder to scan (default: ./foto)")
    parser.add_argument("--out", default="./index.json", help="Output JSON file (default: ./index.json)")
    parser.add_argument("--recursive", action="store_true", help="Recurse into subfolders")
    args = parser.parse_args()

    root = Path(args.folder).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print(f"Folder not found or not a directory: {root}")
        return 1

    jpgs = list_jpg_files(root, args.recursive)
    if not jpgs:
        print("No .jpg images found. index.json will contain an empty list.")

    # Ensure paths in JSON are relative to project root, and include folder prefix
    # Compute project root as the parent of the output file
    project_root = out_path.parent
    entries: List[str] = []
    for p in jpgs:
        try:
            rel = p.relative_to(project_root)
        except ValueError:
            # If not inside project root, fall back to name under folder
            rel = p.name
        # Normalize to POSIX-style strings
        entries.append(rel.as_posix())

    # Write JSON array
    out_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


