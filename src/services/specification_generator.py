from openai import OpenAI

from dotenv import load_dotenv

from ..prompts import GENERATE_SPECIFICATION_PROMPT

# Load environment variables from .env
load_dotenv()

def generate_machine_specifications(query, results):
    
    prompt = GENERATE_SPECIFICATION_PROMPT.format(query=query, results=results)

    client = OpenAI()

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": prompt}
      ]
    )

    specifications = response.choices[0].message.content.strip()
    
    return specifications

# Exemplo de uso
query = "Motor Elétrico Trifásico de 40 CV"
results = """
1. Potência: 40 CV (30 kW)
2. Tensão: 380V/660V
3. Frequência: 60 Hz
4. Rotação: 1750 RPM
5. Grau de Proteção: IP55
6. Eficiência: IE3 Premium
"""

specifications = generate_machine_specifications(query, results)
print("Especificações da Máquina Geradas pelo ChatGPT:\n")
print(specifications)
