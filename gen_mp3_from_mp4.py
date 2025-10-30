from moviepy import VideoFileClip

def extract_audio_from_video(video_file, output_audio_file):
  clip = VideoFileClip(video_file)
  audio = clip.audio
  audio.write_audiofile(output_audio_file)
  audio.close()
  clip.close()
  print(f"Audio extracted and saved to: {output_audio_file}")

if __name__ == "__main__":
  video_file = "input.mp4"  
  output_audio_file = "input.mp3"
  extract_audio_from_video(video_file, output_audio_file)