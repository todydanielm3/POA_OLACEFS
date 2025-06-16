import streamlit as st
from novo_poa import show_novo_poa

def show_menu():
    st.set_page_config(page_title="Menu Inicial", layout="centered")

    st.title("📊 POA OLACEFS")
    st.subheader("Bem-vindo!")

    col1, col2 = st.columns(2)

    if col1.button("➕ Novos POAs"):
        show_novo_poa()
    if col2.button("📁 Acessar existentes"):
        st.switch_page("visualizar_existentes.py")  # ou troque para a função correta
