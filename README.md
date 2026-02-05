**[🇺🇸 English](README.en.md)** · **[🇧🇷 Português](README.md)**

---

# 🤖 ChatBot IA

> Chatbot inteligente para **WhatsApp** com IA generativa e **RAG** (Retrieval-Augmented Generation), respondendo com base em documentos indexados e histórico da conversa.

---

## 📋 Visão geral

Sistema que recebe mensagens via webhook do WhatsApp (WAHA), consulta um banco vetorial (ChromaDB) para contexto e gera respostas usando **Groq** (LLaMA) com LangChain. Ideal para atendimento ou consultas baseadas em materiais (PDFs, manuais, etc.).

| Componente | Função |
|------------|--------|
| **Flask API** | Recebe webhooks, orquestra fluxo e responde |
| **WAHA** | API WhatsApp (envio, histórico, "digitando…") |
| **AIBot** | LangChain + Groq + ChromaDB para RAG e respostas |
| **RAG** | Script para indexar PDFs no ChromaDB |

---

## 🏗️ Arquitetura

```
┌─────────────┐     webhook      ┌─────────────┐     histórico      ┌─────────────┐
│  WhatsApp   │ ───────────────► │  Flask API  │ ◄───────────────── │    WAHA     │
│   (usuário) │                  │  (port 5000)│                    │  (port 3000) │
└─────────────┘                  └──────┬──────┘                    └─────────────┘
                                        │
                                        │ pergunta + histórico
                                        ▼
                               ┌────────────────┐     busca vetorial    ┌─────────────┐
                               │    AIBot       │ ◄──────────────────── │  ChromaDB   │
                               │ (Groq + RAG)   │                       │  (vetores)  │
                               └────────┬───────┘                       └─────────────┘
                                        │
                                        │ resposta
                                        ▼
                               ┌────────────────┐
                               │  WAHA → envio  │ ──────► WhatsApp
                               └────────────────┘
```

---

## 🛠️ Stack

- **Python 3.11** · **Flask** — API e webhook  
- **LangChain** · **LangChain-Chroma** · **LangChain-Groq** — RAG e LLM  
- **ChromaDB** — banco vetorial para documentos  
- **HuggingFace Embeddings** — embeddings dos textos  
- **Groq (LLaMA 3.1 70B)** — modelo de linguagem  
- **WAHA** — integração WhatsApp  
- **Docker & Docker Compose** — execução em containers  

---

## ⚙️ Pré-requisitos

- [Python 3.11+](https://www.python.org/) ou [Docker](https://www.docker.com/)
- Conta e API key no [Groq](https://console.groq.com/)
- Token/API key no [Hugging Face](https://huggingface.co/settings/tokens) (embeddings)
- WAHA configurado (via Docker no projeto) com sessão WhatsApp

---

## 🔐 Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY='sua-groq-api-key'
WAHA_API_KEY='sua-waha-api-key'
HUGGINGFACE_API_KEY='sua-huggingface-api-key'
```

No `docker-compose.yaml`, ajuste também a variável `WAHA_API_KEY` do serviço `waha` se necessário.

---

## 🚀 Como rodar

### Com Docker (recomendado)

1. Clone o repositório e entre na pasta do projeto.
2. Crie o `.env` com as chaves acima.
3. Suba os serviços:

```bash
docker-compose up -d
```

4. A API estará em `http://localhost:5000` e o WAHA em `http://localhost:3000`.
5. Configure o webhook do seu provedor WhatsApp para:  
   `POST http://<seu-host>/chatbot/webhook/`

### Sem Docker (local)

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Configure o `.env`.
3. Rode o WAHA separadamente (ex.: outro container ou instância) e aponte a API para a URL do WAHA (no código, `http://waha:3000` — para local, altere para `http://localhost:3000` no `services/waha.py`).
4. Inicie a API:

```bash
python app.py
```

A API sobe em `http://0.0.0.0:5000`.

---

## 📚 RAG — Indexar documentos (PDF)

Para o bot usar seus PDFs como contexto:

1. Coloque o(s) PDF(s) em `rag/data/` (ex.: `rag/data/django_master.pdf`).
2. No script `rag/rag.py`, ajuste `file_path` se usar outro arquivo ou caminho.
3. Execute o script (com o mesmo ambiente onde o ChromaDB será usado):

```bash
python rag/rag.py
```

Isso gera os chunks, cria os embeddings e persiste em `chroma_data/`. Com Docker, use o volume `./chroma_data:/app/chroma_data` para persistir entre subidas.

---

## 📁 Estrutura do projeto

```
ChatBot IA/
├── app.py                 # Entrada Flask e rota do webhook
├── bot/
│   └── ai_bot.py          # Lógica do bot (Groq + RAG + ChromaDB)
├── rag/
│   └── rag.py             # Script para indexar PDFs no ChromaDB
├── services/
│   └── waha.py            # Cliente da API WAHA (envio, histórico, typing)
├── chroma_data/           # Dados do ChromaDB (gerado ao rodar RAG)
├── docker-compose.yaml
├── Dockerfile.api
├── requirements.txt
├── README.md              # Este arquivo (português)
├── README.en.md           # Documentação em inglês
└── .env                   # Chaves (não versionar)
```

---

## 🔌 Webhook

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/chatbot/webhook/` | Recebe mensagens do WhatsApp (payload com `payload.from`, `payload.body`). Ignora grupos; em DMs, responde via IA. |

O fluxo interno: indicar "digitando" → buscar último histórico no WAHA → chamar o AIBot (RAG + Groq) → enviar resposta pelo WAHA → parar "digitando".

---

## 📄 Licença

Uso interno / projeto pessoal. Ajuste conforme sua necessidade.

---

**Desenvolvido para automação e agentes de IA.** 🚀
