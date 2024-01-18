import argparse
from datetime import datetime
import openai
import os
import sys
from pydub import AudioSegment

def split_text(text, max_length=4096):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def process_chunk(client, chunk, model, voice, filename):
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=chunk
    )
    with open(filename, 'wb') as f:
        f.write(response.content)

def concatenate_audios(file_list, output_file):
    combined = AudioSegment.empty()
    for file in file_list:
        audio = AudioSegment.from_mp3(file)
        combined += audio
    combined.export(output_file, format="mp3")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables. run `export OPENAI_API_KEY=sk-...`")

parser = argparse.ArgumentParser(description='Process input to analyze security article.')
parser.add_argument('-f', '--file', type=str, help='Path to a file containing article')
args = parser.parse_args()

if args.file:
    with open(args.file, 'r') as file:
        input_text = file.read().strip()
elif not sys.stdin.isatty():
    input_text = sys.stdin.read().strip()
else:
    print("No input provided")
    sys.exit(1)

client = openai.OpenAI(api_key=api_key)
chunks = split_text(input_text)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
filenames = []

for i, chunk in enumerate(chunks):
    chunk_filename = f"audio_{timestamp}_{i}.mp3"
    filenames.append(chunk_filename)
    process_chunk(client, chunk, "tts-1", "onyx", chunk_filename) # Available voices: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'

final_audio_filename = f"audio_{timestamp}.mp3"
concatenate_audios(filenames, final_audio_filename)

# Optionally, delete the individual chunk files
for filename in filenames:
    os.remove(filename)

print(f"Final audio output saved to {final_audio_filename}")
