import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader

# Cabeçalhos HTTP para simular um usuário real acessando a página
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_text_from_url(url):
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

def scrape_text_from_links(links):
    all_texts = []
    for link in links:
        print(f"Extraindo texto de: {link}")
        text = extract_text_from_url(link)
        all_texts.append(text)
    return all_texts

# Exemplo de uso:
links = [
    'https://mesindustrial.com.br/fornecedores/weg/mes-industrial-weg-guia-de-especificacao-de-motores-eletricos-50032749-manual-portugues-br.pdf'
]

text_data = scrape_text_from_links(links)

# Exibindo os textos extraídos
for idx, text in enumerate(text_data):
    print(f"Texto extraído do link {idx + 1}:\n{text}\n{'-'*50}")
