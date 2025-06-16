import streamlit as st
from sqlalchemy.orm import Session
from modelos import SessionLocal, Documento, Responsavel, Atividade, Alineamento, Recurso
from datetime import datetime

def show_novo_poa():
    st.title("📋 Cadastro POA - OLACEFS")
    session: Session = SessionLocal()

    st.subheader("I. INFORMACIÓN GENERAL")

    col1, col2 = st.columns(2)
    orgao = col1.text_input("Órgano", placeholder="Comisione Participación Ciudadana")
    presidencia = col2.text_input("Presidencia", placeholder="Contraloría General de la República del Perú")
    ano = st.number_input("Año", min_value=2000, max_value=2100, value=datetime.now().year)

    st.markdown("**Responsables de la formulación del POA**")
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nombre")
    cargo = col2.text_input("Cargo")
    col1, col2 = st.columns(2)
    email = col1.text_input("Correo")
    telefone = col2.text_input("Contacto")

    st.markdown("**Actividades Generales**")
    col1, col2 = st.columns(2)
    meta_estrategica = col1.text_input("Meta estratégica")
    atividade = col2.text_input("Actividad")
    objetivo = st.text_area("Objetivo")

    st.markdown("**Presupuesto Total**")
    col1, col2, col3 = st.columns(3)
    efs = col1.number_input("EFS (USD$)", min_value=0.0, step=100.0)
    olacefs = col2.number_input("OLACEFS (USD$)", min_value=0.0, step=100.0)
    outros = col3.number_input("OTROS (USD$)", min_value=0.0, step=100.0)

    total = efs + olacefs + outros
    st.success(f"💰 Presupuesto Total: ${total:,.2f}")

    st.subheader("II. ALINEACIÓN CON EL PLAN ESTRATÉGICO")
    plano_atividade = st.text_area("Actividad del Plan Operativo")
    meta = st.text_input("Meta Estratégica")
    estrategia = st.text_input("Estrategia")

    st.subheader("III. ASIGNACIÓN DE RECURSOS")
    col1, col2, col3 = st.columns(3)
    r_efs = col1.number_input("EFS (USD$)", key="r_efs", min_value=0.0, step=100.0)
    r_olacefs = col2.number_input("OLACEFS (USD$)", key="r_olacefs", min_value=0.0, step=100.0)
    r_outros = col3.number_input("OTROS (USD$)", key="r_outros", min_value=0.0, step=100.0)

    if st.button("💾 Guardar POA"):
        try:
            doc = Documento(
                orgao=orgao,
                presidencia=presidencia,
                ano=ano,
                plano_atividade=plano_atividade,
                meta=meta,
                estrategia=estrategia
            )
            session.add(doc)
            session.flush()  # para obter doc.id

            resp = Responsavel(
                nome=nome,
                cargo=cargo,
                email=email,
                telefone=telefone,
                documento_id=doc.id
            )
            session.add(resp)

            ativ = Atividade(
                meta_estrategica=meta_estrategica,
                descricao=atividade,
                objetivo=objetivo,
                efs=efs,
                olacefs=olacefs,
                outros=outros,
                documento_id=doc.id
            )
            session.add(ativ)

            alin = Alineamento(
                atividade=plano_atividade,
                meta=meta,
                estrategia=estrategia,
                documento_id=doc.id
            )
            session.add(alin)

            recurso = Recurso(
                atividade=atividade,
                efs=r_efs,
                olacefs=r_olacefs,
                outros=r_outros,
                documento_id=doc.id
            )
            session.add(recurso)

            session.commit()
            st.success("✅ POA guardado correctamente.")
        except Exception as e:
            session.rollback()
            st.error(f"❌ Error al guardar el POA: {e}")
        finally:
            session.close()
