import base64
import requests

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Function to encode the image
def encode_image(image):
    image_bytes = image.getvalue()
    return base64.b64encode(image_bytes).decode('utf-8')

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

    print(response.json())

    return response.json()['choices'][0]['message']['content']

def call_openai_ai_pipeline(images):

    base64_images = map(encode_image, images)
    results = []
    for image in base64_images:
        results.append(call_openai_api(image))

    print(results)