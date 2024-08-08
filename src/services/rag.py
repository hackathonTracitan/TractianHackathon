from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from prompts import GENERATE_SPECIFICATION_PROMPT

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


class OutputFormat(BaseModel):
    """
    Classe de modelo para formatar a saída das especificações da máquina.

    Attributes:
        additional_details (dict): Detalhes adicionais sobre a máquina.
        power (str): Potência da máquina.
        frequency (str): Frequência de operação da máquina.
        voltage (str): Tensão de operação da máquina.
        model (str): Modelo da máquina.
        manufacturer (str): Fabricante da máquina.
    """
    additional_details: dict
    power: str
    frequency: str
    voltage: str
    model: str
    manufacturer: str


def generate_machine_specifications(search_query: str, text_data: str) -> OutputFormat:
    """
    Gera as especificações de uma máquina com base em uma consulta de pesquisa e em dados textuais.

    Args:
        search_query (str): A consulta de pesquisa usada para gerar as especificações.
        text_data (str): Dados textuais contendo informações sobre a máquina.

    Returns:
        OutputFormat: Objeto contendo as especificações formatadas da máquina.
    """
    prompt = GENERATE_SPECIFICATION_PROMPT.format(
        search_query=search_query,
        text_data=text_data
    )

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt}
        ],
        response_format=OutputFormat
    )

    specifications = response.choices[0].message.parsed

    return specifications
