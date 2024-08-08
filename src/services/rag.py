from openai import OpenAI
from pydantic import BaseModel

import os

from dotenv import load_dotenv
from prompts import RAG_PROMPT

# Carrega variáveis de ambiente do arquivo .env
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

#Exemplo de uso
query = "Motor Elétrico Trifásico de 40 CV"
results = """
1. Potência: 40 CV (30 kW)
2. Tensão: 380V/660V
3. Frequência: 60 Hz
4. Rotação: 1750 RPM
5. Grau de Proteção: IP55
6. Eficiência: IE3 Premium
"""

specifications = perform_rag(query, results)
print("Especificações da Máquina Geradas pelo ChatGPT:\n")
print(specifications)
