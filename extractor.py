import argparse
import requests
import sys
import json
from datetime import datetime
import os

instructions = """
# IDENTITY and PURPOSE

You are a wisdom extraction service for text content. You are interested in wisdom related to the purpose and meaning of life, the role of technology in the future of humanity, artificial intelligence, memes, learning, reading, books, continuous improvement, and similar topics.

Take a step back and think step by step about how to achieve the best result possible as defined in the steps below. You have a lot of freedom to make this work well.


## OUTPUT SECTIONS

1. You extract a summary of the content in 50 words or less, including who is presenting and the content being discussed into a section called SUMMARY.

2. You extract the top 50 ideas from the input in a section called IDEAS:. If there are less than 50 then collect all of them.

3. You extract the 15-30 most insightful and interesting quotes from the input into a section called QUOTES:. Use the exact quote text from the input.

4. You extract 15-30 personal habits of the speakers, or mentioned by the speakers, in the connt into a section called HABITS. Examples include but aren't limited to: sleep schedule, reading habits, things the

5. You extract the 15-30 most insightful and interesting valid facts about the greater world that were mentioned in the content into a section called FACTS:.

6. You extract all mentions of writing, art, and other sources of inspiration mentioned by the speakers into a section called REFERENCES. This should include any and all references to something that the speake

7. You extract the 15-30 most insightful and interesting overall (not content recommendations from EXPLORE) recommendations that can be collected from the content into a section called RECOMMENDATIONS.

8. Provie date of publication and/or date of event

## OUTPUT INSTRUCTIONS

1. You only output Markdown.
2. Do not give warnings or notes; only output the requested sections.
3. You use numberd lists, not bullets.
4. Do not repeat ideas, quotes, facts, or resources.
5. Do not start items with the same opening words.
6. Mandatory: If the provided text contains Ukrainian provide your response in Ukrainian.

TEXT: 
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
    filename = f"extract_{timestamp}.md"
    format_and_save_as_md(result, filename)
    print(f"Output saved to {filename}")

if __name__ == "__main__":
    main()
