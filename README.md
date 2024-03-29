# ai-automation
Set of python scripts for task automation using AI

Influenced by Daniel Miessler's talk about [Fabric](https://github.com/danielmiessler/fabric) on David Bombal's [podcast](https://www.youtube.com/watch?v=vF-MQmVxnCs)

## Setup

First export your [OpenAI key](https://platform.openai.com/api-keys) and install Python requirements

`cd ai-automation`

`export OPENAI_API_KEY=sk-...`

`pip install -r requirements.txt` or `pip3 install -r requirements.txt`

## Usage 

### Security incident analysis tool (security.py)
1. copy security article and save it to a text file (text.txt)

2. run `python3 security.py -f text.txt`

3. output will be saved as json file


or 


1. copy security article you want to analyze (copy the web page contents)

2. on macOS* `pbpaste | python3 security.py`

3. output will be saved as json file


### Knowledge extraction tool (extractor.py)

1. copy security article and save it to a text file (text.txt)

2. run `python3 extractor.py -f text.txt`

3. output will be saved as markdown file

or

1. copy article you want to analyze (crtl+c the web page contents or text of the article)

2. on macOS* `pbpaste | python3 extractor.py`

3. output will be saved as markdown file


### Code explainer tool (explain_code.py)

1. copy security article and save it to a text file (text.txt)

2. run `python3 explain_code.py -f text.txt`

3. output will be saved as markdown file

or

1. copy code you want to analyze (crtl+c the piece of code)

2. on macOS* `pbpaste | python3 explain_code.py`

3. output will be saved as markdown file


## Chaining commands: Extract knowledge from YouTube video (subtitles) and provide a readout (mp3 file)


1. copy url of the YouTube video (e.g. `https://www.youtube.com/watch?v=vF-MQmVxnCs`)

2. on macOS* `pbpaste | python3 youtube.py | python3 extractor.py | python3 tts.py`

3. output will be saved as mp3 file


This will:
- Get subtitles of the Youtube video.
- Extract knowledge using ChatGPT
- Get audio of the result in mp3 format


## Linux*

On Linux you can install xclip. 

`sudo apt install xclip`

The same as way `pbpaste` on macOS it will paste contents from clipboard to your Linux terminal.

Example `xclip -selection clipboard -o | python3 youtube.py | python3 extractor.py`

You can also set alias in your .bashrc profile

 `alias pbpaste='xclip -selection clipboard -o'`


## Windows*

On Windows use `Get-Clipboard` for pasting into your PowerShell terminal

Example `Get-Clipboard | python3 youtube.py | python3 extractor.py`