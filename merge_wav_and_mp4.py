from moviepy import VideoFileClip, AudioFileClip

video = VideoFileClip("input.mp4")
audio = AudioFileClip("input.wav")

final_video = video.with_audio(audio)
final_video.write_videofile("output_with_audio.mp4", codec="libx264", audio_codec="aac")

video.close()
audio.close()
final_video.close()