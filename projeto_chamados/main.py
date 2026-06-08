from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="Sistema de Chamados Internos - MVP :-)",
    description="API conectada ao Supabase do Kaio."
)

# buscar o .env
# Se não encontrar, ele usa uma string vazia para não quebrar o código ao iniciar
DATABASE_URL = os.getenv("DATABASE_URL", "https://cybthwnqquqoxxqnqgrf.supabase.co/rest/v1/Chamados")

def conectar_banco():
    # Conecta no PostgreSQL usando a URL direta do supabase
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

class ChamadoSchema(BaseModel):
    titulo: str
    descricao: str
    cep: str

@app.post("/chamados", status_code=201)
def criar_chamado(chamado: ChamadoSchema):
    logging.info(f"Criando chamado: {chamado.titulo}")
    
    if not chamado.titulo.strip() or not chamado.descricao.strip():
        raise HTTPException(status_code=400, detail="Título e descrição são obrigatórios.")

    # INTEGRAÇÃO EXTERNA - ViaCEP
    cidade, estado = "Não informada", "Não informado"
    cep_limpo = chamado.cep.replace("-", "").replace(" ", "")
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
        if response.status_code == 200:
            dados_cep = response.json()
            if "erro" not in dados_cep:
                cidade = dados_cep.get("localidade")
                estado = dados_cep.get("uf")
    except Exception as e:
        logging.error(f"Erro ViaCEP: {e}")

    # SALVANDO NO POSTGRESQL DO SUPABASE
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        query = """
            INSERT INTO chamados (titulo, descricao, cep, cidade, estado, status) 
            VALUES (%s, %s, %s, %s, %s, 'Aberto') RETURNING id;
        """
        cursor.execute(query, (chamado.titulo, chamado.descricao, cep_limpo, cidade, estado))
        chamado_id = cursor.fetchone()['id']
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"id": chamado_id, "titulo": chamado.titulo, "status": "Aberto", "localidade": f"{cidade}-{estado}"}
    except Exception as e:
        logging.warning(f"Banco offline/Não configurado. Erro real: {e}")
        return {"status": "Simulado", "titulo": chamado.titulo, "localidade": f"{cidade}-{estado}"}

@app.get("/chamados")
def listar_chamados():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chamados;")
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado
    except Exception as e:
        logging.warning(f"Retornando dados simulados. Erro: {e}")
        return [{"id": 1, "titulo": "Ajustar Ar Condicionado (Simulado)", "status": "Aberto"}]
