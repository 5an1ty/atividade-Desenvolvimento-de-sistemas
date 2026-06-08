import os
import logging
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="Sistema de Chamados Internos - MVP :-)",
    description="API conectada ao Supabase via Client SDK."
)

# Configurações do Supabase (Buscando do ambiente ou usando seus valores padrões)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://cybthwnqquqoxxqnqgrf.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_secret_wKFpFr5JZBChVy32DyPwyw_fRVAuRT2")

# Inicializa o cliente global do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

    # SALVANDO NO SUPABASE
    try:
        dados_chamado = {
            "titulo": chamado.titulo,
            "descricao": chamado.descricao,
            "cep": cep_limpo,
            "cidade": cidade,
            "estado": estado,
            "status": "Aberto"
        }
        
        # O método .insert() envia os dados. O .execute() roda a query na API do Supabase.
        # Nota: Certifique-se de que o nome da tabela no seu banco é 'chamados' ou 'Chamados'.
        response = supabase.table("Chamados").insert(dados_chamado).execute()
        
        # Pegando o ID do registro inserido retornado pelo Supabase
        chamado_id = response.data[0]['id']
        
        return {"id": chamado_id, "titulo": chamado.titulo, "status": "Aberto", "localidade": f"{cidade}-{estado}"}
        
    except Exception as e:
        logging.warning(f"Erro ao conectar ou salvar no Supabase. Erro real: {e}")
        return {"status": "Simulado", "titulo": chamado.titulo, "localidade": f"{cidade}-{estado}"}

@app.get("/chamados")
def listar_chamados():
    try:
        # Busca todos os dados da tabela 'chamados'
        response = supabase.table("chamados").select("*").execute()
        return response.data
    except Exception as e:
        logging.warning(f"Retornando dados simulados. Erro: {e}")
        return [{"id": 1, "titulo": "Ajustar Ar Condicionado (Simulado)", "status": "Aberto"}]
