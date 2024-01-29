import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import easyocr
import openai
import tkinter as tk

# EasyOCR inditása (itt lehet majd majomkodni azzal hogy más nyelven is müködjön)
reader = easyocr.Reader(['en'])

# Nem tudtam felallitani a virtual enviromentet szoval igy oldottam meg bruh
openai.api_key = 'your-api-key'

# Ezt at kell irni majd a sajat dekstop path-ra
desktop_path = "/Users/szilardmate/desktop"

# Timestamp
start_timestamp = time.time()

# Új tab
root = tk.Tk()
root.title("Output Window")
root.geometry("300x100")
root.attributes("-alpha", 0.5)  # Alpha 0.5

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            file_creation_time = os.path.getctime(file_path)

            # Csekkeli, hogy screenshot benne van-e a file nevében illetve, hogy a timestamp utan készült-e
            if "screenshot" in file_name.lower() and file_creation_time > start_timestamp:
                print(f"Processing: {file_name}")
                self.process(file_path)

    def process(self, file_path):
        # Image to text
        extracted_text = reader.readtext(file_path, detail = 0)
        extracted_string = ' '.join(extracted_text)

        # Gpt prompt
        prompt = f"Find the multiple choice question in the following paragraph: {extracted_string} What is the correct answer? Only return the correct answer."

        # Send text to GPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60  # Még tesztelni kell meddig lehet levinni
        )

        # Extract just the answer from the response
        answer = response.choices[0].text.strip()

        # A taben kiírja a valaszt
        output_label.config(text=f"Answer: {answer}")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=desktop_path, recursive=False)
    observer.start()

    # UI inditása
    root.mainloop()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
