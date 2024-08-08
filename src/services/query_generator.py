import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os

from prompts import *

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Function to encode the image
def encode_image(image):
    image_bytes = image.getvalue()
    return base64.b64encode(image_bytes).decode('utf-8')

def get_response_openai_api(headers, payload):
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Check for API response status
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    

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
                "text": MACHINE_SPECIFICATION_PROMPT

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

    return get_response_openai_api(headers, payload)
    
def summarize_results(results):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": SUMMARY_PROMPT + " ".join(results)
            }
        ],
        "max_tokens": 1000
    }

    return get_response_openai_api(headers, payload)

def call_openai_ai_pipeline(images):
    base64_images = list(map(encode_image, images))

    results = []
    with ThreadPoolExecutor() as executor:
        future_to_image = {executor.submit(call_openai_api, base64_image): base64_image for base64_image in base64_images}
        for future in as_completed(future_to_image):
            result = future.result()
            results.append(result)
    
    summary = summarize_results(results)
    if summary is None:
        return "Não foi possível gerar um resumo das informações."
    return summary
