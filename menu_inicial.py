# menu_inicial.py
import streamlit as st

st.set_page_config(page_title="Plataforma POA OLACEFS", layout="centered")

st.markdown("<h1 style='text-align: center;'>📚 Plataforma POA - OLACEFS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bem-vindo! Escolha uma das opções abaixo para continuar:</p>", unsafe_allow_html=True)

# Espaçamento
st.write("\n\n")

# Cria colunas para centralizar os botões
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("###")
    if st.button("➕ Novos POAs", use_container_width=True):
        st.switch_page("app_poa_olacefs.py")  # Caminho para cadastro de novos POAs

    st.markdown("###")
    if st.button("📂 Acessar existentes", use_container_width=True):
        st.switch_page("visualizar_poa.py")  # Página de visualização (você pode chamar como quiser)
