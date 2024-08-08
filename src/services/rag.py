from openai import OpenAI

from pydantic import BaseModel

import os

from dotenv import load_dotenv

from prompts import RAG_PROMPT

# Load environment variables from .env
load_dotenv()

def perform_rag(
    search_query,
    text_data
    ):

    prompt = RAG_PROMPT.format(search_query=search_query, text_data=text_data)

    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": prompt}
      ],
    )

    specifications = response.choices[0].message.content

    return specifications
