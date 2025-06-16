import streamlit as st

# ✅ Deve ser a PRIMEIRA chamada do Streamlit
st.set_page_config(page_title="POA OLACEFS", layout="wide")

# ✅ Criação automática do banco de dados
from modelos import criar_banco
criar_banco()

# Módulos da aplicação
from novo_poa import show_novo_poa
from visualizar_poa import show_visualizar_poa
from login import show_login
from menu_inicial import show_menu

# ─────────────────────────────── AUTENTICAÇÃO ───────────────────────────────
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    show_login()
    st.stop()  # ✅ Garante que o restante do código não será executado sem login

# ───────────────────────────── ESTADO INICIAL ───────────────────────────────
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
