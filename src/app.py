import streamlit as st
import json 
from typing import List, Dict, Optional
from io import BytesIO
from services.query_generator import call_openai_ai_pipeline
from services.report_generator import generate_report_file
from services.rag import generate_machine_specifications
from services.search import do_query
from services.scraper import scrape_text_from_links

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

machine_name: str = st.text_input("Nome da Máquina")
machine_type: str = st.selectbox("Tipo de Máquina", ["Motor", "Compressor", "Gerador", "Bomba"])
machine_description: str = st.text_area("Descrição da Máquina")
st.subheader("Imagens da Máquina")
uploaded_files: Optional[List[BytesIO]] = st.file_uploader("Escolha as imagens", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Botão de atualização
if st.button("Atualizar Ficha Técnica"):

    infos_to_print: List[str] = []

    if uploaded_files is not None:
        visual_results: str = call_openai_ai_pipeline(uploaded_files)
        visual_results = visual_results.replace("```", "")
        visual_results = visual_results.replace("json", "")
        visual_results_dict: Dict = json.loads(visual_results)

        condition: str = visual_results_dict["conditions"]
        search_query: str = visual_results_dict["search_query"]
        additional_visual_details: Dict[str, str] = visual_results_dict["additional_details"]
        power: str = visual_results_dict["power"]
        frequency: str = visual_results_dict["frequency"]
        voltage: str = visual_results_dict["voltage"]
        model: str = visual_results_dict["model"]
        manufacturer: str = visual_results_dict["manufacturer"]

        search_links: List[str] = do_query(search_query)
        text_data: str = scrape_text_from_links(search_links)

        with st.container():
            st.subheader("📋 Especificações gerais da máquina")
            st.write(f"**Nome:** {machine_name}")
            st.write(f"**Tipo:** {machine_type}")
            st.write(f"**Modelo:** {model}")
            st.write(f"**Condição:** {condition}")
            st.write(f"**Potência:** {power}")
            st.write(f"**Tensão:** {voltage}")
            st.write(f"**Frequência:** {frequency}")
            st.write(f"**Fabricante:** {manufacturer}")
            
            infos_to_print.append("📋 Especificações gerais da máquina\n")
            infos_to_print.append(f"**Nome:** {machine_name}\n")
            infos_to_print.append(f"**Tipo:** {machine_type}\n")
            infos_to_print.append(f"**Modelo:** {model}\n")
            infos_to_print.append(f"**Condição:** {condition}\n")
            infos_to_print.append(f"**Potência:** {power}\n")
            infos_to_print.append(f"**Tensão:** {voltage}\n")
            infos_to_print.append(f"**Frequência:** {frequency}\n")
            infos_to_print.append(f"**Fabricante:** {manufacturer}\n")

        with st.container():
            st.subheader("🔧 Especificações Técnicas Adicionais")
            infos_to_print.append("🔧 Especificações Técnicas Adicionais")
            cols = st.columns(2)
            for i, (key, value) in enumerate(additional_visual_details.items()):
                add_info: str = f"**{key}:** {value}"
                cols[i % 2].write(add_info)
                add_info += '\n'
                infos_to_print.append(add_info)
    else:
        st.error("Por favor, faça o upload de pelo menos uma imagem.")

    st.write(
        "👇 Você pode baixar as especificações como um documento Word pelo botão abaixo"
    )
    docx: bytes = generate_report_file(infos_to_print)
    st.download_button(
        "Baixar especificações como documento Word",
        docx,
        file_name="relatorio.docx",
    )

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Desenvolvido por Bruno Amaral Teixeira de Freitas, Daniel Yuji Hosomi e Vinícius Mókél Seidel")
