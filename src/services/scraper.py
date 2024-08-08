import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader

# Cabeçalhos HTTP para simular um usuário real acessando a página
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    )
}


def extract_text_from_url(url: str) -> str:
    """
    Extrai o texto de uma URL, processando o conteúdo como HTML ou PDF.

    Args:
        url (str): A URL de onde o texto será extraído.

    Returns:
        str: O texto extraído da URL ou uma mensagem de erro.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP não bem-sucedidos

        content_type = response.headers.get('Content-Type')

        if 'text/html' in content_type:
            # Processar como HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ')
            return text

        elif 'application/pdf' in content_type:
            # Processar como PDF
            pdf_reader = PdfReader(BytesIO(response.content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        else:
            return f"Tipo de conteúdo não suportado: {content_type}"

    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a URL: {e}"


def scrape_text_from_links(links: list) -> list:
    """
    Extrai textos de uma lista de links, processando cada um conforme necessário.

    Args:
        links (list): Lista de URLs de onde os textos serão extraídos.

    Returns:
        list: Lista de textos extraídos de cada URL.
    """
    all_texts = []
    for link in links:
        text = extract_text_from_url(link)
        all_texts.append(text)
    return all_texts
