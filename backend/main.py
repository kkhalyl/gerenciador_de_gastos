from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from supabase import create_client, Client

from extrator_pdf import processar_extrato_bancario

SUPABASE_URL = "https://plovibaoqrjxlfjwfopk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBsb3ZpYmFvcXJqeGxmandmb3BrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDM1OTA0MCwiZXhwIjoyMDg5OTM1MDQwfQ.8SUeDdCpglyfX4zFAfzwKqvPKcvxGpssO4-8gZXNerw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI(title="API Financeira", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.get("/")

def home():
    return {"mensagem": "API Financeira rodando 100% no Codespaces!"}

@app.post("/api/upload-extrato/{banco}")
async def upload_extrato(banco:str, file: UploadFile = File(...)):
    if banco not in ["bradesco", "nubank", "picpay", "banco do brasil"]:
        raise HTTPException(status_code=400, detail="Banco não suportado")

    caminho_temp = f"temp_{file.filename}"
    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print(f"Processando arquivo {file.filename} do banco {banco}...")
        dados_extraidos = processar_extrato_bancario(caminho_temp, banco)
        
        for transacao in dados_extraidos:
            transacao["banco"] = banco
            
        supabase.table("transacoes").insert(dados_extraidos).execute()
        
        return {
            "message": "Extrato processado e salvo no banco com sucesso!",
            "total_transactions": len(dados_extraidos),
            "data": dados_extraidos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")
    
    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    