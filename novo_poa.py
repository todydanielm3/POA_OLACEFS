# novo_poa.py
import streamlit as st
import pandas as pd
from modelos import SessionLocal, Documento, Responsavel, Atividade, Alineamento, Recurso, Lote
from sqlalchemy.exc import IntegrityError


def show_novo_poa():
    st.title("📋 Cadastro POA - OLACEFS")

    if 'responsables' not in st.session_state:
        st.session_state.responsables = []
    if 'actividades' not in st.session_state:
        st.session_state.actividades = []
    if 'alineaciones' not in st.session_state:
        st.session_state.alineaciones = []
    if 'recursos' not in st.session_state:
        st.session_state.recursos = []

    # I. INFORMACIÓN GENERAL
    st.header("I. INFORMACIÓN GENERAL")
    organo = st.text_input("Órgão")
    presidencia = st.text_input("Presidência")
    ano = st.text_input("Ano")

    # Responsables
    st.subheader("Responsables de la formulación del POA")
    with st.form("form_resp"):
        cols = st.columns(4)
        nome = cols[0].text_input("Nombre")
        cargo = cols[1].text_input("Cargo")
        email = cols[2].text_input("Correo")
        contato = cols[3].text_input("Contato")
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
                "Actividad": act_r, "EFS": efs_r,
                "OLACEFS": olacefs_r, "OTROS": otros_r,
                "TOTAL": efs_r + olacefs_r + otros_r
            })
    st.dataframe(pd.DataFrame(st.session_state.recursos))

    st.markdown("---")
    if st.button("📤 Enviar formulário para análise"):
        session = SessionLocal()
        try:
            lote = Lote(orgao=organo, presidencia=presidencia, ano=ano)
            session.add(lote)
            session.flush()

            doc = Documento(
                nome=f"POA_{organo}_{ano}", ano=ano,
                orgao=organo, presidencia=presidencia,
                lote_id=lote.id
            )
            session.add(doc)
            session.flush()

            for r in st.session_state.responsables:
                session.add(Responsavel(
                    documento_id=doc.id,
                    nome=r.get("Nombre", ""),
                    cargo=r.get("Cargo", ""),
                    email=r.get("Correo", ""),
                    contato=r.get("Contacto", "")
                ))
            for a in st.session_state.actividades:
                session.add(Atividade(
                    documento_id=doc.id,
                    meta=a.get("Meta", ""),
                    atividade=a.get("Actividad", ""),
                    objetivo=a.get("Objetivo", "")
                ))
            for a in st.session_state.alineaciones:
                session.add(Alineamento(
                    documento_id=doc.id,
                    atividade_po=a.get("Actividad PO", ""),
                    meta_estrategica=a.get("Meta Estratégica", ""),
                    estrategia=a.get("Estrategia", "")
                ))
            for r in st.session_state.recursos:
                session.add(Recurso(
                    documento_id=doc.id,
                    atividade=r.get("Actividad", ""),
                    efs=r.get("EFS", 0),
                    olacefs=r.get("OLACEFS", 0),
                    outros=r.get("OTROS", 0),
                    total=r.get("TOTAL", 0)
                ))

            session.commit()
            st.success("✅ Formulário enviado com sucesso para análise!")

            st.session_state.responsables.clear()
            st.session_state.actividades.clear()
            st.session_state.alineaciones.clear()
            st.session_state.recursos.clear()
        except IntegrityError:
            session.rollback()
            st.error("❌ Já existe um POA para esse órgão e ano. Verifique e tente novamente.")
        except Exception as e:
            session.rollback()
            st.error(f"❌ Erro ao salvar no banco de dados: {e}")
        finally:
            session.close()