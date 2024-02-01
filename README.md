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

## Flow of the script

1. Take a screenshot
2. Extract text using EasyOCR
3. Send API request to GPT-api
4. Display response in MacOs notification
5. Screenshot gets deleted after response

## Using the bot

1. Clone repository
```bash
  git clone https://github.com/DavidM199/chatgpt_cheatcode
``` 

2. Install Requirements
```bash
  pip install -r requirements.txt
```

3. Set the OPENAI api key to env
```bash
  export OPENAI_API_KEY="yourapikey"
```

4. Run the bot:
```bash
  python model_v2.py
```

5. Wait for Terminal to showcase:
```bash
  Listening on desktop...
```
#### 6. Take an area screenshot of the question
- On Mac: SHIFT + CMD + 4
- On Windows: ALT + PrntScr
  ![Test](https://help.blackboard.com/sites/default/files/images/2020-02/ultra_stud_view_MC_ques.png)

#### 7. Wait for response
- Usually takes a few seconds
  
  ![push_not](https://github.com/DavidM199/chatgpt_cheatcode/assets/147255010/37bde15f-9385-4519-8257-ab7c0798ba00)


## Requirements
The following packages are required for model_v2.py to work. All requirements and versions are in requirements.txt (requirements for other files are also included).
- EasyOCR
- PyTorch
- Watchdog
- OpenAI

