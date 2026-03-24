from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from supabase import create_client, Client

from extrator_pdf import processar_extrato_bancario

# 1. Configuração do Supabase (Correta)
SUPABASE_URL = "https://plovibaoqrjxlfjwfopk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBsb3ZpYmFvcXJqeGxmandmb3BrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDM1OTA0MCwiZXhwIjoyMDg5OTM1MDQwfQ.8SUeDdCpglyfX4zFAfzwKqvPKcvxGpssO4-8gZXNerw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Inicialização do FastAPI
app = FastAPI(title="API Financeira", version="1.0")

# 3. Middleware de Segurança (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"mensagem": "API Financeira rodando 100% no Codespaces!"}

@app.get("/api/transacoes")
def listar_transacoes():
    try:
        response = supabase.table("transacoes").select("*").order("data_transacao", desc=True).execute()

        return {
            "mensagem": "Transações recuperadas com sucesso",
            "total": len(response.data),
            "dados": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro as buscar transações: {str(e)}")

@app.post("/api/upload-extrato/{banco}")
async def upload_extrato(banco:str, file: UploadFile = File(...)):
    if banco not in ["bradesco", "nubank", "picpay", "banco do brasil"]:
        raise HTTPException(status_code=400, detail="Banco não suportado")

    caminho_temp = f"temp_{file.filename}"
    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print(f"Processando arquivo {file.filename} do banco {banco}...")
        
        # Lê tudo o que tem no PDF
        dados_extraidos = processar_extrato_bancario(caminho_temp, banco)
        
        # FASE 1: BUSCAR HISTÓRICO NO BANCO PARA A TRAVA
        resposta_db = supabase.table("transacoes").select("*").eq("banco", banco).execute()
        transacoes_existentes = resposta_db.data

        # Cria um "Set" com as assinaturas únicas do que já está no banco
        assinaturas_existentes = set()
        for t in transacoes_existentes:
            assinatura = f"{t.get('data_transacao', '')}_{t.get('descricao', '')}_{t.get('valor', '')}"
            assinaturas_existentes.add(assinatura)

        # FASE 2: APLICAR FILTROS (ANTI-LIXO E DUPLICATAS)
        # -> AQUI ESTÁ A SUA LISTA DE BLOQUEIO APLICADA <-
        palavras_ignoradas = ["TOTAL", "SALDO", "SALDOS E LIMITES", "TRANSPORTADO", "SALDO ANTERIOR", "SALDO DO DIA"]
        transacoes_novas = []
        
        for transacao in dados_extraidos:
            transacao["banco"] = banco
            
            descricao = str(transacao.get("descricao", "")).upper().strip()
            
            # FILTRO A: É uma linha inútil de rodapé do banco?
            eh_lixo = any(descricao.startswith(palavra) for palavra in palavras_ignoradas)
            if eh_lixo:
                continue 

            # FILTRO B: Essa transação já existe no Supabase?
            assinatura_atual = f"{transacao.get('data_transacao', '')}_{transacao.get('descricao', '')}_{transacao.get('valor', '')}"
            
            if assinatura_atual not in assinaturas_existentes:
                transacoes_novas.append(transacao)
                assinaturas_existentes.add(assinatura_atual)

        # FASE 3: INSERIR APENAS AS SOBREVIVENTES
        if len(transacoes_novas) > 0:
            supabase.table("transacoes").insert(transacoes_novas).execute()
        
        return {
            "message": "Extrato processado com sucesso!",
            "linhas_no_pdf": len(dados_extraidos),
            "novas_inseridas": len(transacoes_novas),
            "data": transacoes_novas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")
    
    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)