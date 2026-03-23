# 💸 Assistente Financeiro Inteligente (Smart Finance Tracker)

A maioria dos aplicativos financeiros apenas olha para o passado, mostrando onde você gastou seu dinheiro. Este projeto tem um objetivo diferente: ser uma ferramenta **ativa e prescritiva**, ajudando a projetar o futuro e tomar decisões de compra em tempo real.

## 🚀 O que este projeto faz?

Em vez de limites fixos mensais que são facilmente ignorados, o sistema utiliza o conceito de **Saldo Livre Dinâmico (Safe-to-Spend)**. Ele lê seus extratos, entende seus custos fixos e calcula exatamente quanto você pode gastar *hoje* sem comprometer o resto do mês.

### ✨ Principais Funcionalidades

- **Extração Automatizada de PDF:** Ingestão de extratos bancários em PDF convertidos em dados estruturados (via `pdfplumber`).
- **Detecção de Anomalias:** Identificação de picos de gastos e "assinaturas fantasmas" invisíveis no dia a dia.
- **Regra 50/30/20 Automática:** Categorização inteligente para diagnóstico rápido da saúde financeira.
- **Cálculo de Burn Rate:** Atualização diária do seu ritmo ideal de gastos.
- **[EM BREVE] Agente de Gastos com IA:** Integração com LLM via *Function Calling* (Tools). Um chat onde você pergunta "Posso comprar esse fone de R$ 300?" e a IA responde cruzando os dados do seu banco com as despesas futuras.

## 🏗️ Arquitetura e Tech Stack

O projeto adota uma arquitetura desacoplada, pronta para escalar para um modelo SaaS (Multi-Tenant):

* **Frontend:** Angular (Painel interativo e chat com o Agente).
* **Backend:** Python + FastAPI (Motor de processamento pesado e comunicação com IA).
* **Banco de Dados:** PostgreSQL hospedado no Supabase.
* **Ambiente de Desenvolvimento:** GitHub Codespaces (100% conteinerizado e na nuvem).

## 💻 Como rodar o projeto (Ambiente de Desenvolvimento)

Este projeto foi configurado para rodar instantaneamente via **GitHub Codespaces**. Nenhuma instalação local é necessária.

1. Abra este repositório no GitHub.
2. Clique no botão verde `<> Code` > aba **Codespaces** > **Create codespace on main**.
3. O ambiente virtual subirá automaticamente com Python, Node.js e Angular CLI pré-configurados (via `devcontainer.json`).
4. Configure sua connection string do Supabase nas variáveis de ambiente.

---
**Autor:** Khalyl
