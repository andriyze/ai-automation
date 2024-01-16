import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    # Regular expression for extracting the video ID from a YouTube URL
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    matches = re.search(regex, url)
    return matches.group(1) if matches else None

# Read URL from standard input (pipe)
url = sys.stdin.readline().strip()

# Extract video ID from URL
video_id = extract_video_id(url)
if not video_id:
    print("Error: Invalid YouTube URL")
    sys.exit(1)

try:
    # Retrieve the available transcripts for the video
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Choose the first transcript from the list
    transcript = transcript_list.find_generated_transcript(['en', 'uk'])

    # Fetch the actual transcript data
    subtitles = transcript.fetch()

    # Print each line of the subtitles
    for line in subtitles:
        print(line['text'])

except Exception as e:
    print("Error:", e)
