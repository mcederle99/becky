#!/usr/bin/env python3
"""
Generate videos.json from all video files inside a folder (default: ./video).

Extensions included: .mp4, .MP4, .MOV

Output schema (array of objects):
[
  { "src": "video/clip.mp4", "title": "clip.mp4", "poster": "" },
  ...
]

Usage examples:
  python3 build_videos_manifest.py                   # scan ./video, write ./videos.json
  python3 build_videos_manifest.py --recursive      # include subfolders
  python3 build_videos_manifest.py --folder ./vids  # scan custom folder
  python3 build_videos_manifest.py --out ./videos.json
"""

import argparse
import json
from pathlib import Path
from typing import List


VIDEO_EXTS = {".mp4", ".MP4", ".MOV"}


def list_videos(root: Path, recursive: bool) -> List[Path]:
    if recursive:
        files = [p for p in root.rglob("*") if p.is_file() and p.suffix in VIDEO_EXTS]
    else:
        files = [p for p in root.glob("*") if p.is_file() and p.suffix in VIDEO_EXTS]
    # Sort by name for stable output
    return sorted(files, key=lambda p: p.as_posix().lower())


def main() -> int:
    parser = argparse.ArgumentParser(description="Build videos.json from video files in a folder")
    parser.add_argument("--folder", default="./video", help="Folder to scan (default: ./video)")
    parser.add_argument("--out", default="./videos.json", help="Output JSON file (default: ./videos.json)")
    parser.add_argument("--recursive", action="store_true", help="Recurse into subfolders")
    parser.add_argument(
        "--base-url",
        default="",
        help=(
            "Optional base URL to prefix each src with. If provided, the src will be "
            "constructed as '<base-url>/<filename>'. This is useful when hosting videos "
            "externally (e.g., GitHub Releases, object storage)."
        ),
    )
    args = parser.parse_args()

    root = Path(args.folder).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print(f"Folder not found or not a directory: {root}")
        return 1

    vids = list_videos(root, args.recursive)
    if not vids:
        print("No video files found. videos.json will contain an empty list.")

    # Make paths relative to project root (parent of output file)
    project_root = out_path.parent
    entries: List[dict] = []
    base_url = (args.base_url or "").rstrip("/")
    for p in vids:
        try:
            rel = p.relative_to(project_root)
        except ValueError:
            rel = p
        rel_str = rel.as_posix()
        # If base_url is provided, prefer using only the filename to form the URL,
        # since many hosts (like GitHub Releases) don't preserve folder structure.
        src = f"{base_url}/{p.name}" if base_url else rel_str
        entries.append({
            "src": src,
            "title": p.name,
            "poster": ""
        })

    out_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


