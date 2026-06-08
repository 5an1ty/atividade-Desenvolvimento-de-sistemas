from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis do ficheiro oculto .env (Segurança da Informação)
load_dotenv()

# Configuração de Logs (Requisito de Qualidade da Governaça de TI)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="Sistema de Chamados Internos - MVP",
    description="API REST ligada ao Supabase e integrada com a API do ViaCEP."
)

# Configurações do Supabase obtidas de forma segura através do .env
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://cybthwnqquqoxxqnqgrf.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_secret_wKFpFr5JZBChVy32DyPwyw_fRVAuRT2")

# Inicializa o cliente oficial do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Modelo de dados que a API espera receber no corpo da requisição
class ChamadoSchema(BaseModel):
    titulo: str
    descricao: str
    cep: str

# 1. ROTA PARA CRIAR CHAMADO (POST)
@app.post("/chamados", status_code=201)
def criar_chamado(chamado: ChamadoSchema):
    logging.info(f"A criar novo chamado: {chamado.titulo}")
    
    # Validação para impedir campos em branco
    if not chamado.titulo.strip() or not chamado.descricao.strip():
        raise HTTPException(status_code=400, detail="O título e a descrição são obrigatórios.")

    # INTEGRAÇÃO EXTERNA - ViaCEP
    cidade, estado = "Não informada", "Não informado"
    cep_limpo = chamado.cep.replace("-", "").replace(" ", "")
    try:
        response_cep = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
        if response_cep.status_code == 200:
            dados_cep = response_cep.json()
            if "erro" not in dados_cep:
                cidade = dados_cep.get("localidade")
                estado = dados_cep.get("uf")
                logging.info(f"CEP {chamado.cep} consultado com sucesso: {cidade}-{estado}")
    except Exception as e:
        logging.error(f"Erro na integração com o ViaCEP: {e}")

    # SALVANDO NO SUPABASE 
    try:
        dados_chamado = {
            "titulo": chamado.titulo,
            "descricao": f"{chamado.descricao} | Unidade: {cidade}-{estado} (CEP: {cep_limpo})",
            "status": "Aberto"
        }
        
        response = supabase.table("Chamados").insert(dados_chamado).execute()
        
        # Resgata o ID gerado automaticamente pela base de dados na nuvem
        chamado_id = response.data[0]['id']
        logging.info(f"Chamado {chamado_id} gravado com sucesso no Supabase.")
        
        return {
            "id": chamado_id, 
            "titulo": chamado.titulo, 
            "status": "Aberto", 
            "localidade_identificada": f"{cidade} - {estado}",
            "mensagem": "Chamado salvo com sucesso na base de dados!"
        }
        
    except Exception as e:
        logging.error(f"Erro crítico ao salvar no Supabase: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao salvar na base de dados: {e}")

# 2. ROTA PARA LISTAR CHAMADOS (GET)
@app.get("/chamados")
def listar_chamados():
    logging.info("A aceder à rota de listagem de chamados da base de dados real.")
    try:
        # Procura todos os registos na tabela 'Chamados'
        response = supabase.table("Chamados").select("*").execute()
        
        # Trava de Segurança: Verifica se o banco retornou dados válidos para evitar erro 500 (NoneType)
        if response and hasattr(response, 'data') and response.data is not None:
            return response.data
        
        # Se não houver nada ou falhar a estrutura, devolve uma lista vazia de segurança
        return []
        
    except Exception as e:
        logging.error(f"Erro ao procurar chamados no Supabase: {e}")
        raise HTTPException(status_code=500, detail="Erro ao procurar dados na base de dados.")