# importador.py
import fitz  # PyMuPDF
import re
from modelos import SessionLocal, Documento, Responsavel, Atividade, Alineamento, Recurso, criar_banco

criar_banco()

def extrair_texto_pdf(caminho_pdf: str) -> str:
    doc = fitz.open(caminho_pdf)
    texto = ""
    for page in doc:
        texto += page.get_text()
    return texto

def parse_info_geral(texto):
    orgao = re.search(r"Órgano\s+([^\n]+)", texto)
    presidencia = re.search(r"Presidencia\s+([^\n]+)", texto)
    ano = re.search(r"Año\s+(\d{4})", texto)
    return {
        "orgao": orgao.group(1).strip() if orgao else "Desconhecido",
        "presidencia": presidencia.group(1).strip() if presidencia else "Desconhecido",
        "ano": ano.group(1).strip() if ano else "2025",
    }

def parse_responsaveis(texto):
    blocos = re.findall(r"Nombre\s+([^\n]+)\s+Cargo\s+([^\n]+)\s+Correo electrónico\s+([^\n]+)\s+Contacto\s+([^\n]+)", texto)
    return [{"nome": n, "cargo": c, "email": e, "contato": t} for n, c, e, t in blocos]

def parse_atividades(texto):
    blocos = re.findall(r"M\s*\d+\s+([^\n]+)\n\n(.+?)(?=\nM\s*\d+|\Z)", texto, re.DOTALL)
    atividades = []
    for atividade, objetivo in blocos:
        atividades.append({
            "meta": "M4",  # simplificação para fins de exemplo
            "atividade": atividade.strip(),
            "objetivo": objetivo.strip()
        })
    return atividades

def importar_pdf(path_pdf, nome_documento):
    texto = extrair_texto_pdf(path_pdf)
    info = parse_info_geral(texto)
    responsaveis = parse_responsaveis(texto)
    atividades = parse_atividades(texto)

    session = SessionLocal()

    doc = Documento(nome=nome_documento, **info)
    session.add(doc)
    session.flush()

    for r in responsaveis:
        session.add(Responsavel(documento_id=doc.id, **r))

    for a in atividades:
        session.add(Atividade(documento_id=doc.id, **a))

    session.commit()
    session.close()
    print
