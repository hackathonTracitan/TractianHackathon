import streamlit as st
import json 
from typing import List, Dict, Optional
from io import BytesIO
from services.query_generator import call_openai_ai_pipeline
from services.report_generator import generate_report_file
from services.rag import perform_rag
from services.search import do_query
from services.scraper import scrape_text_from_links
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Informações da Máquina", page_icon="📊", layout="wide")

# Custom CSS para melhorar o estilo e limitar a altura das imagens
st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px;
        }
        .stSubheader {
            color: #4CAF50;
            font-weight: bold;
        }
        .uploaded-image img {
            max-height: 150px;
            object-fit: contain;
        }
    </style>
    """, unsafe_allow_html=True)

# Título
st.title("📊 Informações da Máquina")

st.subheader("Detalhes da Máquina")

machine_name: str = st.text_input("Nome da Máquina (obrigatório)")
machine_type: str = st.selectbox("Tipo de Máquina", ["Motor", "Compressor", "Gerador", "Bomba"])
machine_description: str = st.text_area("Descrição da Máquina (opcional)")
st.subheader("Imagens da Máquina")
uploaded_files: Optional[List[BytesIO]] = st.file_uploader("Escolha as imagens", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Criação dos placeholders
info_placeholder = st.empty()

# Botão de atualização
if st.button("Atualizar Ficha Técnica"):

    infos_to_print: List[str] = []
    table_to_print: pd.DataFrame = pd.DataFrame()

    if machine_name == "":
        st.error("Por favor, preencha o nome da máquina.")
    elif uploaded_files is not None:
        
        info_placeholder.info("🚀 Iniciando o processamento das imagens...")

        visual_results: str = call_openai_ai_pipeline(uploaded_files)
        visual_results = visual_results.replace("```", "").replace("json", "")
        visual_results_dict: Dict = json.loads(visual_results)

        info_placeholder.info("🔍 Extraindo informações visuais da máquina...")

        condition: str = visual_results_dict["conditions"]
        search_query: str = visual_results_dict["search_query"]
        additional_visual_details: Dict[str, str] = visual_results_dict["additional_details"]
        power: str = visual_results_dict["power"]
        frequency: str = visual_results_dict["frequency"]
        voltage: str = visual_results_dict["voltage"]
        model: str = visual_results_dict["model"]
        manufacturer: str = visual_results_dict["manufacturer"]

        info_placeholder.info("🌐 Realizando pesquisa online para informações adicionais...")

        search_links: List[str] = do_query(search_query)
        text_data: str = scrape_text_from_links(search_links)

        info_placeholder.info("🤖 Analisando e gerando especificações com RAG...")

        rag_results = perform_rag(
            search_query,
            text_data
        )
        rag_results = rag_results.replace("```", "").replace("json", "")
        rag_results = json.loads(rag_results)

        power = rag_results["power"] if power is None else power
        frequency = rag_results["frequency"] if frequency is None else frequency
        voltage = rag_results["voltage"] if voltage is None else voltage
        model = rag_results["model"] if model is None else model
        manufacturer = rag_results["manufacturer"] if manufacturer is None else manufacturer
        additional_rag_details = rag_results["additional_details"]
        additional_details = {**additional_visual_details, **additional_rag_details}

        info_placeholder.success("✅ Especificações da máquina encontradas com sucesso!")

        # Substituindo as informações anteriores
        with info_placeholder.container():
            st.subheader("📋 Especificações gerais da máquina")
            st.write(f"**Nome:** {machine_name}")
            st.write(f"**Tipo:** {machine_type}")
            st.write(f"**Modelo:** {model}")
            st.write(f"**Condição:** {condition}")
            st.write(f"**Potência:** {power}")
            st.write(f"**Tensão:** {voltage}")
            st.write(f"**Frequência:** {frequency}")
            st.write(f"**Fabricante:** {manufacturer}")

            infos_to_print = [
                "📋 Especificações gerais da máquina\n",
                f"**Nome:** {machine_name}\n",
                f"**Tipo:** {machine_type}\n",
                f"**Modelo:** {model}\n",
                f"**Condição:** {condition}\n",
                f"**Potência:** {power}\n",
                f"**Tensão:** {voltage}\n",
                f"**Frequência:** {frequency}\n",
                f"**Fabricante:** {manufacturer}\n"
            ]

            st.subheader("🔧 Especificações Técnicas Adicionais")
            
            # Convertendo o dicionário para um DataFrame do Pandas
            df = pd.DataFrame(list(additional_details.items()), columns=["Especificação", "Valor"])
            table_to_print = df
            # Exibindo a tabela
            st.table(df)

        with st.container():
            st.subheader("🔍 Links Complementares\n")
            infos_to_print.append("🔍 Links Complementares")

            for link in search_links:
                st.write(link)
                infos_to_print.append(link+'\n')

    else:
        st.error("Por favor, faça o upload de pelo menos uma imagem.")

    st.subheader(
        "👇 Você pode baixar as especificações como um documento Word pelo botão abaixo"
    )
    docx: bytes = generate_report_file(infos_to_print, table_to_print)
    st.download_button(
        "Baixar especificações como documento Word",
        docx,
        file_name="relatorio.docx",
    )

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Desenvolvido por Bruno Amaral Teixeira de Freitas, Daniel Yuji Hosomi e Vinícius Mókél Seidel")
