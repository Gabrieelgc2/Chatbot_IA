**[🇧🇷 Português](README.md)** · **[🇺🇸 English](README.en.md)**

---

# 🤖 ChatBot IA

> Intelligent **WhatsApp** chatbot with generative AI and **RAG** (Retrieval-Augmented Generation), answering from indexed documents and conversation history.

---

## 📋 Overview

System that receives messages via WhatsApp webhook (WAHA), queries a vector store (ChromaDB) for context, and generates replies using **Groq** (LLaMA) with LangChain. Suited for support or document-based Q&A (PDFs, manuals, etc.).

| Component | Role |
|-----------|------|
| **Flask API** | Handles webhooks, orchestrates flow, and responds |
| **WAHA** | WhatsApp API (send, history, typing indicator) |
| **AIBot** | LangChain + Groq + ChromaDB for RAG and replies |
| **RAG** | Script to index PDFs into ChromaDB |

---

## 🏗️ Architecture

```
┌─────────────┐     webhook      ┌─────────────┐     history        ┌─────────────┐
│  WhatsApp   │ ───────────────► │  Flask API  │ ◄───────────────── │    WAHA     │
│   (user)    │                  │  (port 5000)│                    │  (port 3000) │
└─────────────┘                  └──────┬──────┘                    └─────────────┘
                                        │
                                        │ question + history
                                        ▼
                               ┌────────────────┐     vector search   ┌─────────────┐
                               │    AIBot       │ ◄──────────────────── │  ChromaDB   │
                               │ (Groq + RAG)   │                       │  (vectors)  │
                               └────────┬───────┘                       └─────────────┘
                                        │
                                        │ response
                                        ▼
                               ┌────────────────┐
                               │  WAHA → send   │ ──────► WhatsApp
                               └────────────────┘
```

---

## 🛠️ Stack

- **Python 3.11** · **Flask** — API and webhook  
- **LangChain** · **LangChain-Chroma** · **LangChain-Groq** — RAG and LLM  
- **ChromaDB** — vector store for documents  
- **HuggingFace Embeddings** — text embeddings  
- **Groq (LLaMA 3.1 70B)** — language model  
- **WAHA** — WhatsApp integration  
- **Docker & Docker Compose** — containerized run  

---

## ⚙️ Prerequisites

- [Python 3.11+](https://www.python.org/) or [Docker](https://www.docker.com/)
- Account and API key at [Groq](https://console.groq.com/)
- Token/API key at [Hugging Face](https://huggingface.co/settings/tokens) (for embeddings)
- WAHA set up (via Docker in this repo) with a WhatsApp session

---

## 🔐 Environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY='your-groq-api-key'
WAHA_API_KEY='your-waha-api-key'
HUGGINGFACE_API_KEY='your-huggingface-api-key'
```

In `docker-compose.yaml`, set the `WAHA_API_KEY` for the `waha` service if needed.

---

## 🚀 How to run

### With Docker (recommended)

1. Clone the repo and `cd` into the project folder.
2. Create `.env` with the keys above.
3. Start the services:

```bash
docker-compose up -d
```

4. API will be at `http://localhost:5000` and WAHA at `http://localhost:3000`.
5. Point your WhatsApp webhook to:  
   `POST http://<your-host>/chatbot/webhook/`

### Without Docker (local)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure `.env`.
3. Run WAHA separately (e.g. another container) and point the API to WAHA’s URL (in code it’s `http://waha:3000` — for local, change to `http://localhost:3000` in `services/waha.py`).
4. Start the API:

```bash
python app.py
```

API runs at `http://0.0.0.0:5000`.

---

## 📚 RAG — Index documents (PDF)

To use your PDFs as bot context:

1. Put PDF(s) in `rag/data/` (e.g. `rag/data/django_master.pdf`).
2. In `rag/rag.py`, set `file_path` if using a different file or path.
3. Run the script (in the same environment where ChromaDB will be used):

```bash
python rag/rag.py
```

This creates chunks, embeddings, and persists to `chroma_data/`. With Docker, use volume `./chroma_data:/app/chroma_data` so data persists across restarts.

---

## 📁 Project structure

```
ChatBot IA/
├── app.py                 # Flask entry and webhook route
├── bot/
│   └── ai_bot.py          # Bot logic (Groq + RAG + ChromaDB)
├── rag/
│   └── rag.py             # Script to index PDFs into ChromaDB
├── services/
│   └── waha.py            # WAHA API client (send, history, typing)
├── chroma_data/           # ChromaDB data (created when running RAG)
├── docker-compose.yaml
├── Dockerfile.api
├── requirements.txt
├── README.md              # This doc (Portuguese)
├── README.en.md           # Documentation in English
└── .env                   # Keys (do not commit)
```

---

## 🔌 Webhook

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/chatbot/webhook/` | Receives WhatsApp messages (payload with `payload.from`, `payload.body`). Ignores groups; in DMs, replies via AI. |

Internal flow: show typing → fetch recent history from WAHA → call AIBot (RAG + Groq) → send reply via WAHA → stop typing.

---

## 📄 License

Internal / personal use. Adjust as needed.

---

**Built for automation and AI agents.** 🚀
