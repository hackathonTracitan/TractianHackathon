import base64
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional
from io import BytesIO

from prompts import *

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

def encode_image(image: BytesIO) -> str:
    """
    Encodes an image to base64 string.

    Args:
        image (BytesIO): Image file as a BytesIO object.

    Returns:
        str: Base64 encoded string of the image.
    """
    image_bytes = image.getvalue()
    return base64.b64encode(image_bytes).decode('utf-8')

def get_response_openai_api(headers: Dict[str, str], payload: Dict) -> Optional[str]:
    """
    Sends a request to the OpenAI API and retrieves the response.

    Args:
        headers (Dict[str, str]): HTTP headers for the request.
        payload (Dict): JSON payload for the request.

    Returns:
        Optional[str]: The content of the response or None if an error occurs.
    """
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Check for API response status
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def call_openai_api(base64_image: str) -> Optional[str]:
    """
    Calls the OpenAI API with the provided base64 encoded image.

    Args:
        base64_image (str): Base64 encoded image string.

    Returns:
        Optional[str]: The content of the API response or None if an error occurs.
    """
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

def summarize_results(results: List[str]) -> Optional[str]:
    """
    Summarizes the results using the OpenAI API.

    Args:
        results (List[str]): List of results to summarize.

    Returns:
        Optional[str]: The summary of the results or None if an error occurs.
    """
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
        "max_tokens": 1000,
        "response_format": { "type": "json_object" }
    }

    return get_response_openai_api(headers, payload)

def call_openai_ai_pipeline(images: List[BytesIO]) -> str:
    """
    Processes a list of images using the OpenAI API and returns a summary.

    Args:
        images (List[BytesIO]): List of images as BytesIO objects.

    Returns:
        str: Summary of the processed images or an error message if summary could not be generated.
    """
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
