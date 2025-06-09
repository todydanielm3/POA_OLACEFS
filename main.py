# main.py
import streamlit as st
from novo_poa import show_novo_poa
from visualizar_poa import show_visualizar_poa

# Só aqui fazemos set_page_config
st.set_page_config(page_title="POA OLACEFS", layout="wide")

# Estado inicial
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"

def trocar_pagina(p):
    st.session_state.pagina = p

# ─────────────────────────────── MENU INICIAL ────────────────────────────────
if st.session_state.pagina == "menu":
    st.title("📚 Plataforma POA - OLACEFS")
    st.markdown("Escolha uma das opções para continuar:")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➕ Novos POAs", use_container_width=True):
            trocar_pagina("novo_poa")
        if st.button("📂 Acessar existentes", use_container_width=True):
            trocar_pagina("visualizar")

# ────────────────────────────── PÁGINAS INTERNAS ─────────────────────────────
elif st.session_state.pagina == "novo_poa":
    show_novo_poa()

elif st.session_state.pagina == "visualizar":
    show_visualizar_poa()

# ─────────────────────────────── VOLTAR AO MENU ──────────────────────────────
if st.session_state.pagina != "menu":
    if st.button("🔙 Voltar ao menu"):
        trocar_pagina("menu")
