# Tractian Hackathon - time Closed AI

Esse repositório foi feito para o Hackathon Tractian da SECOMP UNICAMP 2024.

Você pode acessar nosso site clicando [aqui](https://tractianhackathon.streamlit.app/). É recomendado o uso de um desktop para acessar o site.

### General

Este projeto é uma aplicação Streamlit para gerar e visualizar informações detalhadas sobre máquinas com base em imagens fornecidas. Ele utiliza a API OpenAI para extrair especificações de máquinas a partir das imagens e gera relatórios em formato Word para download.

#### Funcionalidades 

- Upload de Imagens: Permite que os usuários façam upload de imagens das máquinas.
- Extração de Dados: Utiliza a API OpenAI para analisar as imagens e extrair especificações técnicas.
- Exibição de Dados: Mostra as informações extraídas e outras informações fornecidas pelo usuário na interface do Streamlit.
- Geração de Relatório: Cria um documento Word com as especificações da máquina para download.

### Funcionamento

Nossa solução combina a extração de informações visuais pelo GPT com dados obtidos por RAG a partir do web-scraping de websites e processamento de PDFs disponibilizados online. O fluxograma abaixo representa, em alto nível, o passo a passo da nossa solução.

![Fluxogram](/images/diagram_hackathon.png)

Utilizamos o ```gpt-4o``` como LLM em todas as chamadas. A interface foi desenvolvida com o framework Streamlit. Já a busca online foi feita a partir do serviço Serper, que disponibiliza uma API para pesquisas no Google. Já para o scraping dos websites, utilizou-se a biblioteca Beautiful Soup e pyPDF2. Por fim, a geração do relatório Word foi feita com a biblioteca docx.

#### Estrutura do Projeto
- app.py: O script principal que define a interface do usuário e lógica da aplicação Streamlit.
- services/query_generator.py: Contém a função para gerar especificações e queries de pesquisa a partir das imagens usando a API OpenAI.
- services/report_generator.py: Contém a função generate_report_file para criar relatórios em formato Word.
- services/rag.py: Contém a função para gerar especificações baseadas em texto obtido da web.
- services/search.py: Contém a função do_query para buscar informações relacionadas à máquina.
- services/scraper.py: Contém a função scrape_text_from_links para extrair texto de links de pesquisa.
- prompts.py : Contém os prompts utilizados no projeto

### Contribuidores

Esse projeto foi feito pelos seguintes alunos de graduação da UNICAMP:

- Bruno Amaral Teixeira de Freitas
- Daniel Yuji Hosomi
- Vinicius Mókel Seidel