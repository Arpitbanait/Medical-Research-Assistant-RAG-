# Medical Research RAG

End-to-end RAG application with FastAPI (backend), ChromaDB, HuggingFace embeddings, Anthropic Claude, and a Vite + React (TypeScript) frontend.

## Prerequisites
- Windows PowerShell
- Git
- Python 3.12 (recommended) or 3.11
- Node.js 18+

Tip: Python 3.13 can hang when importing `torch` via `transformers`. Prefer Python 3.12.

## Backend Setup (FastAPI)

### 1) Create and activate environment
```powershell
cd "C:\Users\HP\Desktop\Medical_Research_RAG\backend"
# If using venv
python -m venv .venv
.venv\Scripts\activate

# Or conda (recommended)
# conda create -n backend-py312 python=3.12 -y
# conda activate backend-py312
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Configure environment variables
Create a `.env` file in `backend/` with:
```
ANTHROPIC_API_KEY=sk-ant-...
# Optional for private HF models
HF_TOKEN=hf_...
```

### 4) Ingest sample documents (optional)
Place `.txt` papers under `backend/data/sample_papers/` and run:
```powershell
python scripts/ingest_documents.py
```
This populates ChromaDB at `backend/data/chroma_db`.

### 5) Run the server
```powershell
uvicorn app.main:app --reload --port 8000
```
If you see import issues with `torch` on Python 3.13, use Python 3.12.

### 6) API Endpoints
- POST `/api/query` — run RAG pipeline
- GET  `/api/health` — status
- POST `/api/upload` — upload PDF/TXT and ingest into vector store

Example upload via `curl`:
```powershell
curl -F "file=@C:\path\to\paper.pdf" -F "title=My Paper" -F "authors=Smith; Doe" http://localhost:8000/api/upload
```

## Frontend Setup (Vite + React)

### 1) Configure API base
Create `frontend/med-scholar-ai/.env.local`:
```
VITE_API_BASE_URL=http://localhost:8000
```

### 2) Install and run
```powershell
cd "C:\Users\HP\Desktop\Medical_Research_RAG\frontend\med-scholar-ai"
npm install
npm run dev
```
Open http://localhost:5173.

### 3) Features
- Chat panel sends queries to `/api/query`
- Sidebar includes an "Upload Paper" form (PDF/TXT) — ingests into ChromaDB
- Confidences and sources shown per response

## Adding More Papers (without UI)
Place `.txt` files in `backend/data/sample_papers/` using header lines:
```
Title: Your paper title
Authors: Lastname, A.; Lastname, B.
Journal: Journal Name
Year: 2024
PubMed ID: 123456
URL: https://...

<body of the article>
```
Then re-run:
```powershell
cd "C:\Users\HP\Desktop\Medical_Research_RAG\backend"
python scripts/ingest_documents.py
```

## Troubleshooting
- 400 on upload: ensure PDF/TXT, <10MB, not encrypted/scanned.
- 422 on query: backend enforces minimum 10 chars for `query`.
- Python 3.13 import hang: use Python 3.12.
- Vector store empty: re-run `scripts/ingest_documents.py` and verify with `python test_retrieval.py`.

## Push to GitHub
Repository is initialized with `.gitignore` to keep secrets and heavy artifacts out.

```powershell
cd "C:\Users\HP\Desktop\Medical_Research_RAG"
# If not yet set
git remote add origin https://github.com/<your-username>/<your-repo>.git

# Push main branch
git push -u origin main
```

## Structure
- `backend/` — FastAPI app, RAG pipeline, vector store, ingestion scripts
- `frontend/med-scholar-ai/` — Vite + React client
- `.gitignore` — excludes venv, env files, node_modules, ChromaDB persistence
