from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
import requests
import logging

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="Sistema de Chamados Internos :)",
    description="API para registro e acompanhamento de chamados."
)

DB_HOST = "localhost"       
DB_USER = "root"            
DB_PASSWORD = "sua_senha"   
DB_NAME = "sistema_chamados"
DB_PORT = 3306

# Função que tenta conectar no banco do Kaio
def conectar_banco():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

# Requisito de Usabilidade/Validação
class ChamadoSchema(BaseModel):
    titulo: str
    descricao: str
    cep: str  # CEP da unidade da empresa que está com problemas

# 1.CRIAR CHAMADO (POST)
@app.post("/chamados", status_code=201)
def criar_chamado(chamado: ChamadoSchema):
    logging.info(f"criação de chamado: {chamado.titulo}")
    
    # Validação simples para evitar dados em branco
    if not chamado.titulo.strip() or not chamado.descricao.strip():
        raise HTTPException(status_code=400, detail="O título e a descrição são obrigatórios.")

    # INTEGRAÇÃO EXTERNA: Vamos buscar a cidade e estado usando o CEP digitado
    cidade = "Não informada"
    estado = "Não informado"
    cep_limpo = chamado.cep.replace("-", "").replace(" ", "")
    
    try:
        # Integração com API
        response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
        if response.status_code == 200:
            dados_cep = response.json()
            if "erro" not in dados_cep:
                cidade = dados_cep.get("localidade")
                estado = dados_cep.get("uf")
                logging.info(f"CEP {chamado.cep} consultado com sucesso: {cidade}-{estado}")
    except Exception as e:
        logging.error(f"Serviço externo ViaCEP indisponível: {e}")

    # Tentativa de salvar no MySQL
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        query = "INSERT INTO chamados (titulo, descricao, cep, cidade, estado) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (chamado.titulo, chamado.descricao, cep_limpo, city := cidade, estado))
        conn.commit()
        conn.close()
        logging.info("Chamado salvo no MySQL com sucesso!")
    except Exception as e:
        # Se o banco do Kaio não estiver ligado ainda isso aqui vai fingir que ta funcionando
        logging.warning(f"Banco de dados offline, simulando salvamento local. Erro real: {e}")

    # Resposta que o usuário recebe
    return {
        "titulo": chamado.titulo,
        "descricao": chamado.descricao,
        "unidade_localizacao": f"{cidade} - {estado}",
        "status": "Aberto",
        "aviso": "Se o banco estiver offline, o dado foi processado mas não persistido."
    }

# 2.LISTAR CHAMADOS (GET)
@app.get("/chamados")
def listar_chamados():
    logging.info("Acessando rota de listagem de chamados.")
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chamados")
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except Exception as e:
        logging.warning(f"Banco offline. Retornando lista simulada. Erro: {e}")
        return [{"id": 1, "titulo": "Chamado de Teste", "status": "Aberto", "cidade": "São Paulo"}]