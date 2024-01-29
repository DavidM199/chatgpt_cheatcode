import os
import logging
import json
import base64
import requests
import bot_base64 as bot
import all_screenshots_extract as asc
import config
import time

desktop_path = "/Users/davidandreas/Desktop"


while True:
    new_screenshots = asc.get_new_screenshots(desktop_path)
    if len(new_screenshots) > 0:
        # Convert the files to JPEG and clean up
        screenshots = asc.convert_to_jpeg_and_clean(new_screenshots)
        for screenshot in screenshots: 
            answer = bot.answer_question(screenshot)
            print("\n Screenshot: " + screenshot + "\n Solution: " + answer[0] + "\n Tokens: " + answer[1] + "\n")
            time.sleep(10)
    
    else:
        time.sleep(10)
        continue 


