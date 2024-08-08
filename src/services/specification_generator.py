from openai import OpenAI

# Defina sua chave de API da OpenAI aqui
openai.api_key = 'sua-chave-api'

def generate_machine_specifications(query, results):
    # Prepara o prompt para o ChatGPT
    prompt = f"""
    Você é um assistente especializado em engenharia de máquinas. 
    Eu tenho uma consulta sobre a seguinte máquina: {query}.
    Aqui está uma lista de informações e resultados relacionados:
    
    {results}
    
    Com base nessas informações, você pode gerar as especificações detalhadas para essa máquina?
    """

    # Chama o ChatGPT para gerar as especificações
    response = openai.Completion.create(
        engine="gpt-4o",  # ou outro modelo mais recente, se disponível
        prompt=prompt,
        max_tokens=500,  # Ajuste conforme necessário
        temperature=0.7,
        n=1,
        stop=None
    )

    # Extrai o texto gerado
    specifications = response.choices[0].text.strip()
    
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
