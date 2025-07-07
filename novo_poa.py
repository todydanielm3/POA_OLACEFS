import streamlit as st
import pandas as pd
from modelos import SessionLocal, Documento, Responsavel, Atividade, Alineamento, Recurso, Lote
from sqlalchemy.exc import IntegrityError


def show_novo_poa():
    st.title("📋 Cadastro POA - OLACEFS")

    # ---------------- Session state lists ----------------
    for key in ("responsables", "actividades", "alineaciones", "recursos"):
        st.session_state.setdefault(key, [])

    # ----------------------- Metas -----------------------
    metas_estrategicas = [
        "Seleccione uno de las Metas",
        "Meta Estratégica 1: Consolidar la Sostenibilidad Técnico-Financiera de la Organización",
        "Meta Estratégica 2: Fortalecer la Gestión Interna hacia Resultados e Impacto",
        "Meta Estratégica 3: Fortalecer la Comunicación y el Posicionamiento Internacional.",
        "Meta Estratégica 4: Potenciar el Valor y Beneficio de las EFS para la Ciudadanía mediante Estándares y Buenas Prácticas; así como Impulsar el Rol de las EFS en la Agenda 2030; y la Participación Ciudadana en el Control Fiscal.",
        "Meta Estratégica 5: Fortalecer y Armonizar el Servicio de Creación de Capacidades.",
        "Meta Estratégica 6: Impulsar la Transformación Digital y la Gestión del Conocimiento"
    ]

    # ---------------- I. INFORMACIÓN GENERAL -------------
    st.header("I. INFORMACIÓN GENERAL")

    opciones_organos = {
        "COMITÉS": [
            "CCC - Creación de Capacidades",
            "CAJ - Asesoria jurídica"
        ],
        "COMISIONES": [
            "CTPBG - Buena Gobernanza",
            "COMTEMA - Medio Ambiente",
            "CPC - Participación Ciudadana",
            "CEDEIR - Evaluación del Desempeño",
            "CTIC - Tecnologías de la Información",
            "CTCT - Corrupción Transnacional",
            "CGID - Género, Inclusión y Diversidad",
            "CPE - PARLAMENTOS Y EFS",
            "COINFRA -Infraestructura y Transiciones Energéticas"
        ],
        "GRUPOS DE TRABAJO": ["GTFD - Fiscalización de desastres"]
    }

    with st.expander("Seleccionar Órgão"):
        grupo_orgao = st.radio("Selecciona el tipo de órgano:", list(opciones_organos.keys()))
        organo = st.selectbox("Órgão", opciones_organos[grupo_orgao])

    presidencia = st.text_input("Presidência")
    ano = st.text_input("Ano")

    # ---------------- Responsables -----------------------
    st.subheader("Responsables de la formulación del POA")
    with st.form("form_resp"):
        cols = st.columns(4)
        nome = cols[0].text_input("Nombre")
        cargo = cols[1].text_input("Cargo")
        email = cols[2].text_input("Correo")
        contato = cols[3].text_input("Contato")
        if st.form_submit_button("Adicionar"):
            st.session_state.responsables.append({
                "Nombre": nome, "Cargo": cargo, "Correo": email, "Contacto": contato
            })
    st.dataframe(pd.DataFrame(st.session_state.responsables))

    # ---------------- Actividades ------------------------
    st.header("Actividades Generales")
    with st.form("form_activ"):
        meta = st.selectbox("Meta estratégica", metas_estrategicas)
        act = st.text_input("Actividad")
        objetivo = st.text_area("Objetivo")
        if st.form_submit_button("Adicionar"):
            st.session_state.actividades.append({
                "Meta": meta, "Actividad": act, "Objetivo": objetivo
            })
    st.dataframe(pd.DataFrame(st.session_state.actividades))

    # ---------------- Presupuesto ------------------------
    st.subheader("Presupuesto Total")
    col1, col2, col3 = st.columns(3)
    pres_efs = col1.number_input("EFS (USD$)", min_value=0)
    pres_olacefs = col2.number_input("OLACEFS (USD$)", min_value=0)
    pres_otros = col3.number_input("OTROS (USD$)", min_value=0)
    st.success(f"💰 Presupuesto Total: ${pres_efs + pres_olacefs + pres_otros:,.2f}")

    # ---------------- Alineación -------------------------
    st.header("II. ALINEACIÓN CON EL PLAN ESTRATÉGICO")
    with st.form("form_alin"):
        act_po = st.text_input("Actividad del Plan Operativo")
        meta_est = st.selectbox("Meta Estratégica", metas_estrategicas, key="sel_meta_est")
        estrategia = st.text_area("Estrategia")
        if st.form_submit_button("Adicionar"):
            st.session_state.alineaciones.append({
                "Actividad PO": act_po, "Meta Estratégica": meta_est, "Estrategia": estrategia
            })
    st.dataframe(pd.DataFrame(st.session_state.alineaciones))

    # ---------------- Recursos ---------------------------
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

    # ---------------- Envio ------------------------------
    st.markdown("---")
    if st.button("📤 Enviar formulário para análise"):
        session = SessionLocal()
        try:
            lote = Lote(orgao=organo, presidencia=presidencia, ano=ano)
            session.add(lote)
            session.flush()

            doc = Documento(
                nome=f"POA_{organo}_{ano}", ano=ano, orgao=organo,
                presidencia=presidencia, lote_id=lote.id
            )
            session.add(doc)
            session.flush()

            for r in st.session_state.responsables:
                session.add(Responsavel(
                    documento_id=doc.id,
                    nome=r.get("Nombre", ""), cargo=r.get("Cargo", ""),
                    email=r.get("Correo", ""), contato=r.get("Contato", "")
                ))
            for a in st.session_state.actividades:
                session.add(Atividade(
                    documento_id=doc.id, meta=a.get("Meta", ""),
                    atividade=a.get("Actividad", ""), objetivo=a.get("Objetivo", "")
                ))
            for a in st.session_state.alineaciones:
                session.add(Alineamento(
                    documento_id=doc.id, atividade_po=a.get("Actividad PO", ""),
                    meta_estrategica=a.get("Meta Estratégica", ""), estrategia=a.get("Estrategia", "")
                ))
            for r in st.session_state.recursos:
                session.add(Recurso(
                    documento_id=doc.id, atividade=r.get("Actividad", ""),
                    efs=r.get("EFS", 0), olacefs=r.get("OLACEFS", 0),
                    outros=r.get("OTROS", 0), total=r.get("TOTAL", 0)
                ))

            session.commit()
            st.success("✅ Formulário enviado com sucesso para análise!")

            for key in ("responsables", "actividades", "alineaciones", "recursos"):
                st.session_state[key].clear()
        except IntegrityError:
            session.rollback()
            st.error("❌ Já existe um POA para esse órgão e ano. Verifique e tente novamente.")
        except Exception as e:
            session.rollback()
            st.error(f"❌ Erro ao salvar no banco de dados: {e}")
        finally:
            session.close()
