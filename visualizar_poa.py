# visualizar_poa.py
import streamlit as st
import pandas as pd
from modelos import SessionLocal, Documento, Responsavel, Atividade, Alineamento, Recurso

def show_visualizar_poa():
    st.header("📂 Visualização dos POAs Existentes")
    session = SessionLocal()

    tabs = st.tabs(["📁 Documentos", "👥 Responsáveis", "📝 Atividades", "🧭 Alineamentos", "💰 Recursos"])

    with tabs[0]:
        st.subheader("📁 Documentos")
        docs = session.query(Documento).all()
        df = pd.DataFrame([{
            "ID": d.id, "Nome": d.nome, "Ano": d.ano, "Órgão": d.orgao, "Presidência": d.presidencia
        } for d in docs])
        st.dataframe(df, use_container_width=True)

    with tabs[1]:
        st.subheader("👥 Responsáveis")
        resps = session.query(Responsavel).all()
        df = pd.DataFrame([{
            "Documento ID": r.documento_id, "Nome": r.nome, "Cargo": r.cargo,
            "Email": r.email, "Contato": r.contato
        } for r in resps])
        st.dataframe(df, use_container_width=True)

    with tabs[2]:
        st.subheader("📝 Atividades")
        atividades = session.query(Atividade).all()
        df = pd.DataFrame([{
            "Documento ID": a.documento_id, "Meta": a.meta,
            "Atividade": a.atividade, "Objetivo": a.objetivo
        } for a in atividades])
        st.dataframe(df, use_container_width=True)

    with tabs[3]:
        st.subheader("🧭 Alineamentos")
        alis = session.query(Alineamento).all()
        df = pd.DataFrame([{
            "Documento ID": a.documento_id, "Atividade PO": a.atividade_po,
            "Meta Estratégica": a.meta_estrategica, "Estratégia": a.estrategia
        } for a in alis])
        st.dataframe(df, use_container_width=True)

    with tabs[4]:
        st.subheader("💰 Recursos")
        recursos = session.query(Recurso).all()
        df = pd.DataFrame([{
            "Documento ID": r.documento_id, "Atividade": r.atividade,
            "EFS": r.efs, "OLACEFS": r.olacefs, "Outros": r.outros, "Total": r.total
        } for r in recursos])
        st.dataframe(df, use_container_width=True)
