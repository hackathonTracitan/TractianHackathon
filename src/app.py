import streamlit as st
from PIL import Image

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
    # Exibindo informações da máquina após o botão ser pressionado
    with st.container():
        st.subheader("📋 Especificações da Máquina")
        st.write(f"**Nome:** {machine_name}")
        st.write(f"**Tipo:** {machine_type}")
        st.write(f"**Descrição:** {machine_description}")
        st.write("**Modelo:** Motor Elétrico Trifásico")
        st.write("**Identificação:** 10009204")
        st.write("**Fabricante:** WEG")
        st.write("**Localização:** MOINHO 7")
    # Exibindo especificações técnicas
    with st.container():
        st.subheader("🔧 Especificações Técnicas")
        specs = {
            "Potência": "40 CV (30 kW)",
            "Tensão": "380V/660V (estimado)",
            "Frequência": "60 Hz",
            "Rotação": "1750 RPM (estimado)",
            "Grau de Proteção": "IP55",
            "Eficiência": "IE3 Premium (estimado)"
        }
        cols = st.columns(2)
        for i, (key, value) in enumerate(specs.items()):
            cols[i % 2].write(f"**{key}:** {value}")

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Desenvolvido por Bruno Amaral Teixeira de Freitas, Daniel Yuji Hosomi e Vinícius Mókél Seidel")