# src/clipper.py
from moviepy.editor import VideoFileClip
import os

def create_clip(source_path, start_s, end_s, out_path):
    clip = VideoFileClip(source_path).subclip(start_s, end_s)
    clip.write_videofile(out_path, codec="libx264", audio_codec="aac", threads=2, logger=None)
    return out_path

# Note: You must have access to the source video file locally. YouTube terms apply if you download your own videos.
