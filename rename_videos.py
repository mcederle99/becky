#!/usr/bin/env python3
"""
Script to rename all .MOV files in the video/ folder with sequential numbering.
Renames files to video1.MOV, video2.MOV, video3.MOV, etc.
"""

import os
import glob
from pathlib import Path

def rename_mov_files():
    """Rename all .MOV files in video/ folder with sequential numbering."""
    
    # Define the video folder path
    video_folder = Path("video")
    
    # Check if video folder exists
    if not video_folder.exists():
        print(f"Error: {video_folder} folder does not exist!")
        return
    
    # Get all .MOV files (case insensitive)
    mov_files = []
    for ext in ['*.MOV', '*.mov']:
        mov_files.extend(glob.glob(str(video_folder / ext)))
    
    if not mov_files:
        print("No .MOV files found in video/ folder.")
        return
    
    # Sort files for consistent ordering
    mov_files.sort()
    
    print(f"Found {len(mov_files)} .MOV files to rename:")
    for i, file_path in enumerate(mov_files, 1):
        print(f"  {file_path}")
    
    # Ask for confirmation
    response = input(f"\nRename {len(mov_files)} files to video1.MOV, video2.MOV, etc.? (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Rename files
    renamed_count = 0
    for i, old_path in enumerate(mov_files, 1):
        old_file = Path(old_path)
        new_name = f"video{i}.MOV"
        new_path = video_folder / new_name
        
        try:
            # Check if target already exists
            if new_path.exists() and new_path != old_file:
                print(f"Warning: {new_name} already exists, skipping {old_file.name}")
                continue
            
            # Rename the file
            old_file.rename(new_path)
            print(f"Renamed: {old_file.name} -> {new_name}")
            renamed_count += 1
            
        except Exception as e:
            print(f"Error renaming {old_file.name}: {e}")
    
    print(f"\nSuccessfully renamed {renamed_count} files.")

if __name__ == "__main__":
    rename_mov_files()
