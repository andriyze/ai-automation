import argparse
import requests
import sys
import json
from datetime import datetime
import os

instructions = """
# IDENTITY and PURPOSE

You are an expert coder that takes code and documentation as input and do your best to explain it.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps. You have a lot of freedom in how to carry out the task to achieve the best result.

# OUTPUT SECTIONS

- If the content is code, you explain what the code does in a section called EXPLANATION:. 

- If the content is security tool output, you explain the implications of the output in a section called SECURITY IMPLICATIONS:.

- If the content is configuration text, you explain what the settings do in a section called CONFIGURATION EXPLANATION:.

- If there was a question in the input, answer that question about the input specifically in a section called ANSWER:.

# OUTPUT 

- Do not output warnings or notes—just the requested sections.

# INPUT:

INPUT:

"""

def query_gpt4_turbo(prompt, model="gpt-4-turbo-preview"):
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"Using model {model}")
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
    filename = f"code_explainer_{timestamp}.md"
    format_and_save_as_md(result, filename)
    print(f"Output saved to {filename}")

if __name__ == "__main__":
    main()
