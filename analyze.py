import argparse
import requests
import sys
import json
from datetime import datetime
import os

instructions = """
# IDENTITY and PURPOSE

You are a research paper analysis service focused on determining the primary findings of the paper and analyzing its scientific quality.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps.

# OUTPUT SECTIONS

- Extract a summary of the content in 50 words or less, including who is presenting and the content being discussed into a section called SUMMARY.

- Extract the list of authors in a section called AUTHORS.

- Extract the list of organizations the authors are associated, e.g., which university they're at, with in a section called AUTHOR ORGANIZATIONS.

- Extract the primary paper findings into a bulleted list of no more than 50 words per bullet into a section called FINDINGS.

- You extract the size and details of the study for the research in a section called STUDY DETAILS.

- Extract the study quality by evaluating the following items in a section called STUDY QUALITY:

### Sample size

- **Check the Sample Size**: The larger the sample size, the more confident you can be in the findings. A larger sample size reduces the margin of error and increases the study's power.

### Confidence intervals

- **Look at the Confidence Intervals**: Confidence intervals provide a range within which the true population parameter lies with a certain degree of confidence (usually 95% or 99%). Narrower confidence intervals suggest a higher level of precision and confidence in the estimate.

### P-Value

- **Evaluate the P-value**: The P-value tells you the probability that the results occurred by chance. A lower P-value (typically less than 0.05) suggests that the findings are statistically significant and not due to random chance.

### Effect size

- **Consider the Effect Size**: Effect size tells you how much of a difference there is between groups. A larger effect size indicates a stronger relationship and more confidence in the findings.

### Study design

- **Review the Study Design**: Randomized controlled trials are usually considered the gold standard in research. If the study is observational, it may be less reliable.

### Consistency of results

- **Check for Consistency of Results**: If the results are consistent across multiple studies, it increases the confidence in the findings.

### Data analysis methods

- **Examine the Data Analysis Methods**: Check if the data analysis methods used are appropriate for the type of data and research question. Misuse of statistical methods can lead to incorrect conclusions.

### Researcher's interpretation

- **Assess the Researcher's Interpretation**: The researchers should interpret their results in the context of the study's limitations. Overstating the findings can misrepresent the confidence level.

### Summary

You output a 50 word summary of the quality of the paper and it's likelihood of being replicated in future work as one of three levels: High, Medium, or Low. You put that sentence and ratign into a section called SUMMARY.

# OUTPUT INSTRUCTIONS

- Create the output using the formatting above.
- You only output human readable Markdown.
- Do not output warnings or notes—just the requested sections.
- Mandatory: If the provided text contains Ukrainian provide your response in Ukrainian.

# INPUT:

INPUT:



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
    filename = f"analyze_{timestamp}.md"
    format_and_save_as_md(result, filename)
    print(f"Output saved to {filename}")

if __name__ == "__main__":
    main()
