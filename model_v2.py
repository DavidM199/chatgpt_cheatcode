import os
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import easyocr
from openai import OpenAI
import time
import platform
import threading

client = OpenAI()

class Watcher:
    # Check the operating system
    if platform.system() == "Windows":
        DIRECTORY_TO_WATCH = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        DIRECTORY_TO_WATCH = os.path.join(os.environ['HOME'], 'Desktop')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        print("Detected new file:", event.src_path)
        time.sleep(1)  # Short delay before processing the file
        if 'screenshot' in event.src_path.lower() and datetime.datetime.fromtimestamp(os.path.getmtime(event.src_path)) > Handler.start_time:
            currentVariable = event.src_path
            extractedString = extract_text(currentVariable)
            response = query_gpt(extractedString)
            display_response(response)

    start_time = datetime.datetime.now()

def extract_text(image_path, max_attempts=5, delay=1):
    for attempt in range(max_attempts):
        try:
            reader = easyocr.Reader(['en'])
            result = reader.readtext(image_path)
            extracted_text = ' '.join([text[1] for text in result])
            print(extract_text)
            return extracted_text
        except FileNotFoundError:
            print(f"Attempt {attempt+1}: File not found, retrying...")
            time.sleep(delay)
    return "Error: File not found after multiple attempts."

def query_gpt(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "Extract the multiple choice question and provide the correct answer."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error querying GPT: {e}")
        return "Error"

def display_response(response):
    print("Response:", response)

if __name__ == '__main__':
    w = Watcher()
    watcher_thread = threading.Thread(target=w.run)  # Create a thread for the watcher
    watcher_thread.start()  # Start the watcher thread
