import argparse
import requests
import sys
import json
from datetime import datetime
import os

instructions = """
# IDENTITY and PURPOSE

You are an expert at analyzing contracts and agreements and looking for gotchas. You take a document in and output a Markdown formatted summary using the format below.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps.

# OUTPUT SECTIONS

- Combine all of your understanding of the content into a single, 30-word sentence in a section called DOCUMENT SUMMARY:.

- Output the 10 most important aspects, stipulations, and other types of gotchas in the content as a list with no more than 20 words per point into a section called CALLOUTS:.

- Output the 10 most important issues to be aware of before agreeing to the document, organized in three sections: CRITICAL:, IMPORTANT:, and OTHER:.

- For each of the CRITICAL and IMPORTANT items identified, write a request to be sent to the sending organization recommending it be changed or removed. Place this in a section called RESPONSES:.

# OUTPUT INSTRUCTIONS

- Create the output using the formatting above.
- You only output human readable Markdown.
- Output numbered lists, not bullets.
- Do not output warnings or notes—just the requested sections.
- Do not repeat items in the output sections.
- Do not start items with the same opening words.
- If the provided text is in Ukrainian provide your response in Ukrainian.

# INPUT:

INPUT:
"""

def query_gpt4_turbo(prompt, model="gpt-4-1106-preview"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables. run `export OPENAI_API_KEY=sk-...`")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer {}".format(api_key),
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": instructions + prompt}]
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

def format_and_save_as_md(content, filename):
    if 'choices' in content and len(content['choices']) > 0:
        formatted_text = content['choices'][0]['message']['content']
        print(formatted_text)
        with open(filename, 'w') as file:
            file.write(formatted_text)

def main():
    parser = argparse.ArgumentParser(description='Process input to analize article.')
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

    result = query_gpt4_turbo(input_text)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"agreement_{timestamp}.md"
    format_and_save_as_md(result, filename)
    print(f"Output saved to {filename}")

if __name__ == "__main__":
    main()
