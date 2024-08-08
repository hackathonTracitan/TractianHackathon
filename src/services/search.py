import http.client
import json
import os
from dotenv import load_dotenv

# Configuração da conexão HTTPS para a API do Serper
CONN = http.client.HTTPSConnection("google.serper.dev")

# Carregamento das variáveis de ambiente
load_dotenv()

# Configuração dos headers para a requisição HTTP
HEADERS = {
    'X-API-KEY': os.getenv('SERPER_KEY'),
    'Content-Type': 'application/json'
}


def get_links(result_dict: dict) -> list:
    """
    Extrai os links dos resultados de busca orgânica.

    Args:
        result_dict (dict): Dicionário contendo os resultados da busca.

    Returns:
        list: Lista de links extraídos dos resultados orgânicos.
    """
    links = []

    for result in result_dict["organic"]:
        links.append(result["link"])

    return links


def do_query(query: str) -> list:
    """
    Executa uma consulta na API do Serper e retorna os links dos resultados.

    Args:
        query (str): A consulta a ser feita.

    Returns:
        list: Lista de links dos resultados da consulta.
    """
    payload = json.dumps({
        "q": query,
        "location": "Brazil",
        "gl": "br",
        "hl": "pt-br"
    })

    CONN.request("POST", "/search", payload, HEADERS)

    query_result = json.loads(CONN.getresponse().read().decode("utf-8"))

    print(query_result)

    return get_links(query_result)
