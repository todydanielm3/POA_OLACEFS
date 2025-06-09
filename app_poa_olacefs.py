import streamlit as st
import pandas as pd
import os
from importador import importar_pdf  # ← função que você já criou
from modelos import SessionLocal, Documento, Responsavel, Atividade, Alineamento, Recurso

st.set_page_config(page_title="Cadastro POA OLACEFS", layout="wide")

# Sessões
if 'responsables' not in st.session_state:
    st.session_state.responsables = []
if 'actividades' not in st.session_state:
    st.session_state.actividades = []
if 'alineaciones' not in st.session_state:
    st.session_state.alineaciones = []
if 'recursos' not in st.session_state:
    st.session_state.recursos = []

st.title("📋 Cadastro POA - OLACEFS")

# I. INFORMACIÓN GENERAL
st.header("I. INFORMACIÓN GENERAL")
organo = st.text_input("Órgano")
presidencia = st.text_input("Presidência")
ano = st.text_input("Ano")

# Responsables
st.subheader("Responsables de la formulación del POA")
with st.form("form_resp"):
    cols = st.columns(4)
    nome = cols[0].text_input("Nombre")
    cargo = cols[1].text_input("Cargo")
    email = cols[2].text_input("Correo")
    contato = cols[3].text_input("Contacto")
    if st.form_submit_button("Adicionar"):
        st.session_state.responsables.append({
            "Nombre": nome, "Cargo": cargo,
            "Correo": email, "Contacto": contato
        })
st.dataframe(pd.DataFrame(st.session_state.responsables))

# Atividades
st.header("Actividades Generales")
with st.form("form_activ"):
    meta = st.text_input("Meta estratégica")
    act = st.text_input("Actividad")
    objetivo = st.text_area("Objetivo")
    if st.form_submit_button("Adicionar"):
        st.session_state.actividades.append({
            "Meta": meta, "Actividad": act, "Objetivo": objetivo
        })
st.dataframe(pd.DataFrame(st.session_state.actividades))

# Presupuesto total
st.subheader("Presupuesto Total")
col1, col2, col3 = st.columns(3)
pres_efs = col1.number_input("EFS (USD$)", min_value=0)
pres_olacefs = col2.number_input("OLACEFS (USD$)", min_value=0)
pres_otros = col3.number_input("OTROS (USD$)", min_value=0)
st.success(f"💰 Presupuesto Total: ${pres_efs + pres_olacefs + pres_otros:,.2f}")

# II. ALINEACIÓN
st.header("II. ALINEACIÓN CON EL PLAN ESTRATÉGICO")
with st.form("form_alin"):
    act_po = st.text_input("Actividad del Plan Operativo")
    meta_est = st.text_input("Meta Estratégica")
    estrategia = st.text_area("Estrategia")
    if st.form_submit_button("Adicionar"):
        st.session_state.alineaciones.append({
            "Actividad PO": act_po, "Meta Estratégica": meta_est, "Estrategia": estrategia
        })
st.dataframe(pd.DataFrame(st.session_state.alineaciones))

# III. RECURSOS
st.header("III. ASIGNACIÓN DE RECURSOS")
with st.form("form_recursos"):
    act_r = st.text_input("Actividad")
    efs_r = st.number_input("EFS (USD$)", min_value=0, key="efs_r")
    olacefs_r = st.number_input("OLACEFS (USD$)", min_value=0, key="olacefs_r")
    otros_r = st.number_input("OTROS (USD$)", min_value=0, key="otros_r")
    if st.form_submit_button("Adicionar"):
        st.session_state.recursos.append({
            "Actividad": act_r, "EFS": efs_r, "OLACEFS": olacefs_r,
            "OTROS": otros_r, "TOTAL": efs_r + olacefs_r + otros_r
        })
st.dataframe(pd.DataFrame(st.session_state.recursos))

st.header("📥 Importar POA a partir de PDF")

uploaded_file = st.file_uploader("Selecione um arquivo PDF do POA", type=["pdf"])
nome_doc = st.text_input("Nome do Documento (ex: COINFRA)")

if uploaded_file and nome_doc:
    caminho_temp = f"temp_{uploaded_file.name}"
    with open(caminho_temp, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("📄 Importar PDF para o banco de dados"):
        try:
            importar_pdf(caminho_temp, nome_doc)
            st.success(f"Documento '{nome_doc}' importado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao importar: {e}")
        finally:
            os.remove(caminho_temp)

st.header("📊 Visualização dos Dados")

# Inicia sessão do banco
session = SessionLocal()

tab_doc, tab_resp, tab_ativ, tab_ali, tab_rec = st.tabs([
    "📁 Documentos", "👥 Responsáveis", "📝 Atividades", "🧭 Alineamentos", "💰 Recursos"
])

with tab_doc:
    docs = session.query(Documento).all()
    df = pd.DataFrame([{
        "ID": d.id,
        "Nome": d.nome,
        "Ano": d.ano,
        "Órgão": d.orgao,
        "Presidência": d.presidencia
    } for d in docs])
    st.dataframe(df)

with tab_resp:
    resps = session.query(Responsavel).all()
    df = pd.DataFrame([{
        "Documento ID": r.documento_id,
        "Nome": r.nome,
        "Cargo": r.cargo,
        "Email": r.email,
        "Contato": r.contato
    } for r in resps])
    st.dataframe(df)

with tab_ativ:
    atividades = session.query(Atividade).all()
    df = pd.DataFrame([{
        "Documento ID": a.documento_id,
        "Meta": a.meta,
        "Atividade": a.atividade,
        "Objetivo": a.objetivo
    } for a in atividades])
    st.dataframe(df)

with tab_ali:
    alinhamentos = session.query(Alineamento).all()
    df = pd.DataFrame([{
        "Documento ID": a.documento_id,
        "Atividade PO": a.atividade_po,
        "Meta Estratégica": a.meta_estrategica,
        "Estratégia": a.estrategia
    } for a in alinhamentos])
    st.dataframe(df)

with tab_rec:
    recursos = session.query(Recurso).all()
    df = pd.DataFrame([{
        "Documento ID": r.documento_id,
        "Atividade": r.atividade,
        "EFS": r.efs,
        "OLACEFS": r.olacefs,
        "Outros": r.outros,
        "Total": r.total
    } for r in recursos])
    st.dataframe(df)
