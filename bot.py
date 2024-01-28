from openai import OpenAI
import openai
import os

client = OpenAI()

def assistant(url):
    response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Answer the multiple choice question in the image."},
        {
          "type": "image_url",
          "image_url": {
            "url": url,
            "detail": "low"
          },
        },
      ],
    }
  ],
  max_tokens=100,
)

    return response.choices[0].message.content

url = None # image url
if __name__ == "__main__":
    print(assistant(url))