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

def call_openai_api(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

    payload = {
        "model": "gpt-4o",
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
        "max_tokens": 500
        }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']

def call_openai_ai_pipeline(image_path):
    base64_image = encode_image(image_path)
    return call_openai_api(base64_image)

print(call_openai_ai_pipeline('data/0c66f66c-97ac-4b66-98ec-550994441fd1.jpg'))