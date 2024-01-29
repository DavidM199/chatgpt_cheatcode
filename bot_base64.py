import base64
import requests
import os
import json
import all_screenshots_extract as asc
from config import api_key

def extract_content(byte_str):
    # Decode byte string to string
    decoded_str = byte_str.decode('utf-8')

    # Parse string as JSON
    data = json.loads(decoded_str)

    # Extract the content string
    content_str = data['choices'][0]['message']['content'] 

    tokens = str(data["usage"]["total_tokens"])
    # Output the content string
    return [content_str, tokens]

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
def input_to_image_path():
    user_input = input("Enter name of image in Desktop: ")
    return "/Users/davidandreas/Desktop/" + user_input + ".jpeg"


# Getting the base64 string
def answer_question(image_path):
    base64_image = encode_image(image_path)

    headers = {
     "Content-Type": "application/json",
     "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
         "role": "user",
          "content": [
         {
              "type": "text",
              "text": "Answer the multiple choice question in the image. Output the solution only." 
              #and a one sentence explanation in a python dictionary with keys 'solution' and 'explanation'."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
             }
          }
          ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    answer = extract_content(response.content)

    return answer



run = False
if __name__ == "__main__":
    #screenshot mean the screenshot path
   screenshots = asc.convert_to_jpeg_and_clean(asc.get_screenshot_files("/Users/davidandreas/Desktop"))
   if run:
    for screenshot in screenshots: 
        answer = answer_question(screenshot)
        print("\n Screenshot: " + screenshot + "\n Solution: " + answer[0] + "\n Tokens: " + answer[1] + "\n")

