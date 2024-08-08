import streamlit as st
import json 
from services.query_generator import call_openai_ai_pipeline
from services.report_generator import generate_report_file
<<<<<<< Updated upstream

from services.specification_generator import generate_machine_specifications
=======
from services.rag import generate_machine_specifications
>>>>>>> Stashed changes
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

machine_name = st.text_input("Nome da Máquina")
machine_type = st.selectbox("Tipo de Máquina", ["Motor", "Compressor", "Gerador", "Bomba"])
machine_description = st.text_area("Descrição da Máquina")
st.subheader("Imagens da Máquina")
uploaded_files = st.file_uploader("Escolha as imagens", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
# Botão de atualização
if st.button("Atualizar Ficha Técnica"):

    if uploaded_files is not None:
        visual_results = call_openai_ai_pipeline(uploaded_files)
        visual_results = visual_results.replace("```", "")
        visual_results = visual_results.replace("json", "")
        visual_results = json.loads(visual_results)

        print(visual_results)

        condition = visual_results["conditions"]
        search_query = visual_results["search_query"]
        additional_visual_details = visual_results["additional_details"]
        power = visual_results["power"],
        frequency = visual_results["frequency"],
        voltage = visual_results["voltage"],
        model = visual_results["model"],
        manufacturer = visual_results["manufacturer"]

        search_links = do_query(search_query)
        text_data = scrape_text_from_links(search_links)

        rag_results = generate_machine_specifications(
            search_query,
            text_data
        )

        power = rag_results["power"] if power is None else power
        frequency = rag_results["frequency"] if frequency is None else frequency
        voltage = rag_results["voltage"] if voltage is None else voltage
        model = rag_results["model"] if model is None else model
        manufacturer = rag_results["manufacturer"] if manufacturer is None else manufacturer
        additional_rag_details = rag_results["additional_details"]
        additional_details = {**additional_visual_details, **additional_rag_details}
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

        with st.container():
            st.subheader("🔧 Especificações Técnicas Adicionais")
            cols = st.columns(2)
            for i, (key, value) in enumerate(additional_details.items()):
                cols[i % 2].write(f"**{key}:** {value}")
    
    else:
        st.error("Por favor, faça o upload de pelo menos uma imagem.")

    st.write(
        "👇 Você pode baixar as especificações como um documento Word pelo botão abaixo"
    )
    docx = generate_report_file("teste")
    st.download_button(
        "Baixar especificações como documento Word",
        docx,
        file_name="relatorio.docx",
    )

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Desenvolvido por Bruno Amaral Teixeira de Freitas, Daniel Yuji Hosomi e Vinícius Mókél Seidel")