# ChatCheatPT model for multiple choice

This project was made for demonstration purposes only.

## Collaborators

[Szilárd](https://github.com/szilrdmate) - Founder of many companies and will probably try to make this idea lucrative

[David](https://github.com/DavidM199) - Student at WU and definitely won't use this bot on his next exam

## Goal of the project

We wanted to showcase the true disruptive qualities of ChatGPT in the university environment and create a *working example of a bot streamlining the usage of illegal aids during exams.* 

The bot can take any multiple choice question after it has been screenshotted and answer it in the form of a notification. This way, the user doesn't have to leave the current window which would cause suspicion in the lecturer or any other person. 

## Clarification

The bot can be run with _**model_v2.py**_.

Files _all_screenshots_extract.py, bot_base64.py, bot_url.py, config.py, run.py_ were used for preliminary idea exploration
that lead us to the final version and completion of the project. 

### _**Important:**_ 

Before running model_v2.py, you have to _add your openai api key as an environment variable_ with the line \
`export OPENAI_API_KEY='yourapikey'`. (add to ~/.zshrc or ~/.bash_profile)

## Using the bot

1. Take a Screenshot with cmd shift 4 (on MacOs) to be able to select a region
2. Select the region where your multiple choice question is
3. The script will look for new screenshot files and once one is detected and processed, it will delete your screenshot (we don't want to leave evidence)
4. Your question and answers are fed to ChatGPT via API
5. *The response appears in a form of a sneaky notification*

### Requirements
The following packages are required for model_v2.py to work. All requirements and versions are in requirements.txt (requirements for other files are also included).
- easyocr
- watchdog
- openai

