#!/usr/bin/env python3
"""
Script to add all video filenames from video_new/ folder to videos.json
"""

import json
import os
from pathlib import Path

def update_videos_json():
    """Add all videos from video_new/ folder to videos.json"""
    
    # Read current videos.json
    videos_file = Path("videos.json")
    
    if videos_file.exists():
        with open(videos_file, 'r') as f:
            videos = json.load(f)
    else:
        videos = []
    
    # Get all video files from video_new/ folder
    video_new_folder = Path("video_new")
    if not video_new_folder.exists():
        print("Error: video_new/ folder does not exist!")
        return
    
    # Supported video extensions
    video_extensions = ['.mp4', '.MP4', '.mov', '.MOV', '.avi', '.AVI', '.mkv', '.MKV']
    
    # Find all video files
    video_files = []
    for file_path in video_new_folder.iterdir():
        if file_path.is_file() and file_path.suffix in video_extensions:
            video_files.append(file_path.name)
    
    # Sort files for consistent ordering
    video_files.sort()
    
    print(f"Found {len(video_files)} video files in video_new/ folder")
    
    # Add each video to the JSON
    for i, filename in enumerate(video_files, 1):
        # Generate a title from filename
        title = filename.replace('.MP4', '').replace('.mp4', '').replace('.MOV', '').replace('.mov', '')
        
        # Create video entry
        video_entry = {
            "src": f"video_new/{filename}",
            "title": title,
            "poster": ""
        }
        
        # Check if this video already exists in the JSON
        exists = any(video.get("src") == f"video_new/{filename}" for video in videos)
        
        if not exists:
            videos.append(video_entry)
            print(f"Added: {filename}")
        else:
            print(f"Already exists: {filename}")
    
    # Write updated JSON back to file
    with open(videos_file, 'w') as f:
        json.dump(videos, f, indent=2)
    
    print(f"\nUpdated videos.json with {len(videos)} total videos")

if __name__ == "__main__":
    update_videos_json()
