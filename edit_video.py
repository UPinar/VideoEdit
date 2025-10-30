import os
import re
import pytesseract
from PIL import Image
from moviepy import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips

# Set Tesseract path IMMEDIATELY after import
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

INPUT_FOLDER = r"C:\Users\uygrp\OneDrive\Resimler\Screenshots"
VIDEO_FILE = r"C:\Users\uygrp\OneDrive\Desktop\VideoEdit\input.mp4" 

times_array = []

def merge_video_segments(segment_files, output_file):
  clips = []
  for file in segment_files:
    clip = VideoFileClip(file)
    clips.append(clip)
    clip.close()
    
  # Re-open clips for merging
  clips = [VideoFileClip(f) for f in segment_files if os.path.exists(f)]
  final_clip = concatenate_videoclips(clips)
  final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
  final_clip.close()

  for clip in clips:
    clip.close()

def cut_video_segment(video_file, start_time, end_time, video_segment_file):
  clip = VideoFileClip(video_file)
  subclip = clip.subclipped(start_time, end_time)
  subclip.write_videofile(video_segment_file, codec='libx264', audio_codec='aac')
  subclip.close()
  clip.close()
  
  return video_segment_file

def process_video_with_timestamps(video_file, timestamps):
  clip = VideoFileClip(video_file)
  video_duration = clip.duration
  clip.close()
  
  valid_timestamps = []
  for i in range(0, len(timestamps) - 1, 2):
    raw_start   = int(timestamps[i])
    raw_end     = int(timestamps[i + 1])
    start_time  = raw_start / 1000.0
    end_time    = raw_end / 1000.0
    valid_timestamps.append((start_time, end_time))

  ##############################################################
  
  segment_files = []
  current_time = 0

  for i, (cut_start, cut_end) in enumerate(valid_timestamps):
    if current_time < cut_start:
      duration = cut_start - current_time
      if duration > 0.1:
        video_segment_file = f"video_segment_{i}.mp4"
        result = cut_video_segment(video_file, current_time, cut_start, video_segment_file)
        if result:
          segment_files.append(result)
    current_time = cut_end

  # Keep the final part after the last cut range
  if current_time < video_duration:
    duration = video_duration - current_time

    if duration > 0.1:
      video_segment_file = f"video_segment_{len(valid_timestamps)}.mp4"
      result = cut_video_segment(video_file, current_time, video_duration, video_segment_file)
      if result:
        segment_files.append(result)

  ##############################################################

  if segment_files:
    merge_video_segments(segment_files, "output.mp4")



def process_image_with_ocr(image_path):
  img = Image.open(image_path)

  # Configure Tesseract to only recognize digits
  custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
  text = pytesseract.image_to_string(img, config=custom_config).strip()
  
  lines = text.split('\n')

  for line in lines:
    line = line.strip()
    digits_only = re.sub(r'[^0-9]', '', line)
    
    if digits_only:
      last_9_digits = digits_only[-9:] if len(digits_only) >= 9 else digits_only
      times_array.append(last_9_digits)
      print(f"Extracted time from {os.path.basename(image_path)}: {last_9_digits}")

def process_directory_and_find_images(folder_path):
  for filename in os.listdir(folder_path):
    if filename.lower().endswith('.png'):
      full_path = os.path.join(folder_path, filename)
      process_image_with_ocr(full_path)

def main():
  times_array.clear()

  process_directory_and_find_images(INPUT_FOLDER)
  
  if times_array:
    process_video_with_timestamps(VIDEO_FILE, times_array)
  else:
    print("Error: No timestamps extracted from screenshots.")

if __name__ == "__main__":
  main()