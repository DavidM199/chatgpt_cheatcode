import os
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import easyocr
from openai import OpenAI
import time
import platform
import threading
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='model_v2.log', filemode='w')
logger = logging.getLogger(__name__)


client = OpenAI()

class Watcher:
    # Check the operating system
    if platform.system() == "Windows":
        DIRECTORY_TO_WATCH = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        DIRECTORY_TO_WATCH = os.path.join(os.environ['HOME'], 'Desktop')

    def __init__(self):
        self.observer = Observer()
        print(f"Watching directory {self.DIRECTORY_TO_WATCH}...")

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            logger.info("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
        last_processed = None
        @staticmethod
        def on_created(event):
            if is_intermediate_screenshot(event.src_path):
                logger.info(f"Detected intermediate screenshot file: {event.src_path}")
                final_path = event.src_path.replace('/.', '/')

                # Wait and check for the file to be renamed
                for _ in range(15):  # Try for 15 seconds, adjust as needed
                    time.sleep(1)  # Check every 1 second, adjust as needed
                    if os.path.exists(final_path):
                        logger.info(f"Screenshot processed: {final_path}")
                        process(final_path)
                        Handler.last_processed = final_path
                        break
            elif not event.is_directory and event.src_path.endswith('.png') and event.src_path != Handler.last_processed:
                try:
                    logger.info(f"Screenshot processed: {event.src_path}")
                    process(event.src_path)
                    Handler.last_processed = event.src_path
                except Exception as e:
                    logger.error(f"Error processing screenshot: {e}")
            else:
                 logger.error(f"This is not a screenshot file: {event.src_path}")
        
        start_time = datetime.datetime.now()
def process(final_path):
            if datetime.datetime.fromtimestamp(os.path.getmtime(final_path)) > Handler.start_time:
                        currentVariable = final_path
                        extractedString = extract_text(currentVariable)
                        response = query_gpt(extractedString)
                        display_response(response)
                        os.remove(final_path)

def is_intermediate_screenshot(path):
        # match the pattern '.Screenshot...png'
        return ".Screenshot" in path and path.endswith('.png')

def extract_text(image_path):
    
    try:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image_path)
        extracted_text = ' '.join([text[1] for text in result])
        return extracted_text
    except FileNotFoundError:
        logger.error(f"Extract_text attempt: File not found, retrying...")
        
    

def query_gpt(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "Provide the correct answer to the multiple choice question as short as possible."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error querying GPT: {e}")
        return "Error"

def display_response(response):
    print("Response:", response)

if __name__ == '__main__':
    w = Watcher()
    watcher_thread = threading.Thread(target=w.run)
    watcher_thread.daemon = True  # Set the thread as a daemon
    watcher_thread.start()

    try:
        while True:  # Keep the main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
