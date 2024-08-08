# Tractian Hackathon - Close AI

Esse repositório foi feito para o Hackathon Tractian da SECOMP UNICAMP 2024.

Você pode acessar nosso site clicando [aqui](https://tractianhackathon.streamlit.app/). É recomendado o uso de um desktop para acessar o site.

### General

Este projeto é uma aplicação Streamlit para gerar e visualizar informações detalhadas sobre máquinas com base em imagens fornecidas. Ele utiliza a API OpenAI para extrair especificações de máquinas a partir das imagens e gera relatórios em formato Word para download.

#### Funcionalidades 

-Upload de Imagens: Permite que os usuários façam upload de imagens das máquinas.
-Extração de Dados: Utiliza a API OpenAI para analisar as imagens e extrair especificações técnicas.
-Exibição de Dados: Mostra as informações extraídas e outras informações fornecidas pelo usuário na interface do Streamlit.
-Geração de Relatório: Cria um documento Word com as especificações da máquina para download.

#### Estrutura do Projeto
-app.py: O script principal que define a interface do usuário e lógica da aplicação Streamlit.
-services/query_generator.py: Contém a função call_openai_ai_pipeline para gerar especificações a partir das imagens usando a API OpenAI.
-services/report_generator.py: Contém a função generate_report_file para criar relatórios em formato Word.
-services/rag.py: Contém a função generate_machine_specifications para gerar especificações baseadas em texto.
-services/search.py: Contém a função do_query para buscar informações relacionadas à máquina.
-services/scraper.py: Contém a função scrape_text_from_links para extrair texto de links de pesquisa.



### Contribuidores

Esse projeto foi feito pelos seguintes alunos de graduação da UNICAMP:

- Bruno Amaral Teixeira de Freitas
- Daniel Yuji Hosomi
- Vinicius Mókel Seidel