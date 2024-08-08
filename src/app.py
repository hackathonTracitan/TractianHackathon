import base64
import requests

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "data/7ba51969-3fd4-4864-8a57-565a5045eefa.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

def call_openai_api(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Analyze the image and describe the machine in string format. Include the following details: 1) 'specification' –\
                ALL specifications of the machine possible found like motor, brand, voltage, rotations, 2) 'origin' – where the machine is from, and 3) 'answer' – a summary of this information in Portuguese.\
                The response MUST be a single string following this structure: {specification: 'maximum specification', origin: 'country or place of origin', answer: 'summary in Portuguese'}."
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

    print(response.json()['choices'][0]['message']['content'])

call_openai_api(base64_image)