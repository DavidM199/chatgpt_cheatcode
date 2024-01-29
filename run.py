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

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
filehandler = logging.FileHandler('run.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

while True:
    new_screenshots = asc.get_new_screenshots(desktop_path)
    if len(new_screenshots) > 0:
        # Convert the files to JPEG and clean up
        screenshots = asc.convert_to_jpeg_and_clean(new_screenshots)
        logger.info(f"Found {len(screenshots)} new screenshots")
        try:
            for screenshot in screenshots: 
                answer = bot.answer_question(screenshot)
                print("\n Screenshot: " + screenshot + "\n Solution: " + answer[0] + "\n Tokens: " + answer[1] + "\n")
                os.remove(screenshot)
                time.sleep(10)
            logger.info(f"Processed and deleted {len(screenshots)} screenshots")
        except Exception as e:
            logger.error(f"Failed to process screenshots. Error: {e}")
            continue
    else:
        time.sleep(10)
        continue 


