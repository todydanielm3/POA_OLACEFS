# login.py
import streamlit as st

def show_login():
    st.title("🔐 Login - POA OLACEFS")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username == "poa_mvp" and password == "olacefs2025":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
