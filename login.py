# login.py
import streamlit as st

def show_login():
    st.title("🔐 Login - POA OLACEFS")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    cred_user = st.secrets["credentials"]["username"]
    cred_pass = st.secrets["credentials"]["password"]

    if st.button("Entrar"):
        if username == cred_user and password == cred_pass:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
