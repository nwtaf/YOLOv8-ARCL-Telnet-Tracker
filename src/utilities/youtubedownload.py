import os
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Specify the YouTube URL
youtube_url = '' # provide URL

# Create a YouTube object
yt = YouTube(youtube_url)

# Specify the relative path to the data directory
data_dir = os.path.join(os.getcwd(), 'data')

# debug
print(f"Here is the output: {data_dir}")

# Download the highest quality video to the data directory
download_path = yt.streams.get_highest_resolution().download(data_dir)

# Optional:
# Specify the start and end times of the segment you want to save (in seconds)

start_time = 0
end_time = 100

# Specify the output file for the segment - change filename as needed
output_file = os.path.join(data_dir, 'filename.mp4')

# Extract the segment and save it
ffmpeg_extract_subclip(download_path, start_time, end_time, targetname=output_file)