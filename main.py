# main.py
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# 1. Configuração inicial
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="POA OLACEFS", layout="wide")

# 1.1  CSS global  +  Top-bar
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    html, body, [class*="css"] { font-family:'Roboto',sans-serif; }

    /* Top-bar */
    .app-header{
        width:100%;
        background:#0072BC;
        color:#FFF;
        text-align:center;
        padding:12px 0;
        font-size:1.35rem;
        font-weight:500;
        border-bottom:3px solid #005a91;
        position:sticky;
        top:0;
        z-index:1000;
        margin-bottom:1.5rem;

     /* 🔽 Cantos arredondados somente embaixo */
        border-radius:0 0 16px 16px;
    }

    /* Fundo degradê */
    body{background:linear-gradient(180deg,#F4F9FC 0%,#EAF4FB 40%,#F4F9FC 100%);}

    /* Cartões / expander / abas */
    .stContainer, .stTabs, .stExpander{
        background:#FFFFFF;
        border-radius:12px;                /* ←▼ cantos arredondados  */
        box-shadow:0 2px 4px rgba(0,0,0,.06);
        padding:0.5rem 1rem;
    }

    /* Botões */
    button[data-baseweb="button"]{
        background:#0072BC !important; color:#FFF !important;
        border:none; border-radius:8px;  /* ←▼ */
        font-weight:500; transition:all .2s;
    }
    button[data-baseweb="button"]:hover{background:#005a91 !important;}

    /* Botão secundário (ex.: Voltar) */
    button[kind="secondary"]{background:#8BC540 !important; color:#FFF !important;
        border-radius:8px;}               /* ←▼ */

    /* Campos de entrada */
    input, textarea, .stNumberInput input{
        border:1px solid #C7DAEB; border-radius:6px;  /* ←▼ */
    }

    /* Cabeçalhos h2 / h3 */
    h2, h3{color:#0072BC; border-bottom:2px solid #0072BC20;
        padding-bottom:4px; margin-bottom:0.5rem;}

    /* Alertas */
    .stAlert-success{background:#E6F6D8;border-left:6px solid #8BC540; border-radius:6px;}
    .stAlert-error  {background:#FEE9E4;border-left:6px solid #F1592A; border-radius:6px;}
    </style>

    <div class="app-header">Cadastro POA - OLACEFS</div>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Banco de dados (cria se não existir)
# ─────────────────────────────────────────────────────────────────────────────
from modelos import criar_banco
criar_banco()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Importação dos módulos
# ─────────────────────────────────────────────────────────────────────────────
from novo_poa import show_novo_poa
from visualizar_poa import show_visualizar_poa
from login import show_login

# ─────────────────────────────────────────────────────────────────────────────
# 4. Autenticação simples
# ─────────────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    show_login()
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 5. Navegação de páginas
# ─────────────────────────────────────────────────────────────────────────────
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"

def trocar_pagina(p: str):
    st.session_state.pagina = p

# 5.1  Menu
if st.session_state.pagina == "menu":
    st.title("📚 Plataforma POA - OLACEFS")
    st.markdown("Escolha uma das opções para continuar:")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➕ Novos POAs", use_container_width=True):
            trocar_pagina("novo_poa")
        if st.button("📂 Acessar existentes", use_container_width=True):
            trocar_pagina("visualizar")

# 5.2  Páginas internas
elif st.session_state.pagina == "novo_poa":
    show_novo_poa()

elif st.session_state.pagina == "visualizar":
    show_visualizar_poa()

# 5.3  Botão voltar
if st.session_state.pagina != "menu":
    if st.button("🔙 Voltar ao menu", key="btn_voltar", type="secondary"):
        trocar_pagina("menu")
