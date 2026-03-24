import json
from supabase import create_client, Client

# 1. Suas Credenciais do Supabase
# Você encontra isso no Supabase em: Project Settings (ícone de engrenagem) -> API
SUPABASE_URL = "https://plovibaoqrjxlfjwfopk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBsb3ZpYmFvcXJqeGxmandmb3BrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzNTkwNDAsImV4cCI6MjA4OTkzNTA0MH0.pIx_i9VAf3bJqo_yCoUaBr5u69GhTUy7SDIcU5AML58" # Use a chave "anon public" ou "service_role"

# 2. Inicia o cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def subir_dados_para_nuvem():
    nome_arquivo = "extrato_limpo.json"
    
    print(f"📖 Lendo o arquivo {nome_arquivo}...")
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo JSON não encontrado! Rode o script do PDF primeiro.")
        return

    print(f"🚀 Enviando {len(dados)} transações para o Supabase...")
    
    # Insere todos os dados de uma vez só (Bulk Insert)
    try:
        response = supabase.table("transacoes").insert(dados).execute()
        print("✅ Dados inseridos com sucesso na nuvem!")
    except Exception as e:
        print(f"❌ Erro ao enviar para o banco: {e}")

if __name__ == "__main__":
    subir_dados_para_nuvem()