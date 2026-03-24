import pdfplumber
import re
import json

def extrair_bradesco(caminho_pdf):
    transacoes = []
    data_atual = None 
    
    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if not texto: continue
            
            linhas = texto.split('\n')
            
            for linha in linhas:
                linha = linha.strip()
                if not linha: continue
                
                if "Extrato de:" in linha or "Saldo (R$)" in linha or "Folha:" in linha or "Bradesco" in linha or "Nome:" in linha or "Data:" in linha:
                    continue
                
                match_data = re.match(r'^(\d{2}/\d{2}/\d{4})', linha)
                if match_data:
                    data_atual = match_data.group(1)
                    linha = linha[10:].strip() 
                
                padrao_valores = r'((?:\d+\.)*\d+,\d{2})\s+((?:\d+\.)*\d+,\d{2})$'
                match_valores = re.search(padrao_valores, linha)
                
                if match_valores:
                    if not data_atual:
                        continue 
                    
                    valor = match_valores.group(1)
                    saldo = match_valores.group(2)
                    
                    desc_bruta = linha[:match_valores.start()].strip()
                    desc_limpa = re.sub(r'\s+\d{6,8}$', '', desc_bruta).strip()
                    
                    transacoes.append({
                        "data": data_atual,
                        "descricao": desc_limpa,
                        "valor": valor,
                        "saldo": saldo
                    })
                
                else:
                    if len(transacoes) > 0:
                        linha_sem_docto = re.sub(r'\s+\d{6,8}$', '', linha).strip()
                        if linha_sem_docto:
                            transacoes[-1]["descricao"] += f" - {linha_sem_docto}"

    return transacoes

def preparar_para_banco(transacoes_brutas):
    transacoes_limpas = []
    saldo_anterior = 0.0

    for i, t in enumerate(transacoes_brutas):
        valor_float = float(t['valor'].replace('.', '').replace(',', '.'))
        saldo_float = float(t['saldo'].replace('.', '').replace(',', '.'))
        
        dia, mes, ano = t['data'].split('/')
        data_sql = f"{ano}-{mes}-{dia}"
        
        if i == 0:
            sinal = -1 if "DES:" in t['descricao'] else 1
            valor_final = valor_float * sinal
        else:
            diferenca = round(saldo_float - saldo_anterior, 2)
            
            if diferenca > 0:
                valor_final = valor_float  
            else:
                valor_final = -valor_float 

        saldo_anterior = saldo_float
        
        desc_limpa = re.sub(r'^\d{6,8}\s*-\s*', '', t['descricao'])

        transacoes_limpas.append({
            "data_transacao": data_sql,
            "descricao": desc_limpa,
            "valor": valor_final,
            "saldo_apos_transacao": saldo_float
        })

    return transacoes_limpas

def processar_extrato_bancario(caminho_pdf, nome_banco):
    print(f"Iniciando extração para o banco: {nome_banco}")
    
    if nome_banco == "bradesco":
        dados_brutos = extrair_bradesco(caminho_pdf)
    else:
        raise ValueError(f"Banco {nome_banco} ainda não suportado no sistema.")
    
    dados_prontos = preparar_para_banco(dados_brutos)
    
    return dados_prontos

if __name__ == "__main__":
    arquivo = "extrato.pdf"
    nome_banco = "bradesco"
    
    print(f"📄 Lendo o arquivo {arquivo}...")
    dados_prontos_pro_banco = processar_extrato_bancario(arquivo, nome_banco)
    
    print(f"\n✅ Sucesso! Foram processadas {len(dados_prontos_pro_banco)} transações.\n")
    print("-" * 50)
    
    for i, d in enumerate(dados_prontos_pro_banco):
        sinal = "🟢 ENTRADA" if d['valor'] > 0 else "🔴 SAÍDA "
        print(f"{i+1:03d} | {d['data_transacao']} | {sinal} | R$ {d['valor']:8.2f} | {d['descricao'][:40]}...")
        
    print("-" * 50)
    
    nome_json = "extrato_limpo.json"
    with open(nome_json, "w", encoding="utf-8") as f:
        json.dump(dados_prontos_pro_banco, f, ensure_ascii=False, indent=4)
        
    print(f"💾 Arquivo '{nome_json}' salvo com sucesso na sua pasta!")
    print("Pronto para enviar para o banco de dados!")