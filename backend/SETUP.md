# Medical Research RAG - Complete Setup Guide

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API Key
Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```env
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### 3. Ingest Sample Data
```bash
python scripts/ingest_documents.py
```

Expected output:
```
✓ Loaded 4 documents
✓ Created 12 chunks
✓ Embedded and stored in ChromaDB
✓ Test query successful
```

### 4. Start Backend Server
```bash
python run.py
```

Server starts at: **http://localhost:8000**

### 5. Test API
```bash
# Health check
curl http://localhost:8000/api/health

# Sample query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the benefits of metformin for diabetes?"}'
```

### 6. Start Frontend (separate terminal)
```bash
cd ../frontend/med-scholar-ai
npm install  # or: bun install
npm run dev  # or: bun dev
```

Frontend at: **http://localhost:8080**

---

## Detailed Configuration

### Environment Variables (.env)

```env
# REQUIRED
ANTHROPIC_API_KEY=your_key_here

# Vector Database
CHROMA_DB_PATH=data/chroma_db
CHROMA_COLLECTION_NAME=medical_research
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# LLM Settings
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
LLM_TEMPERATURE=0              # 0 = deterministic (recommended)
LLM_MAX_TOKENS=4000

# RAG Pipeline
RETRIEVAL_TOP_K=8              # Number of documents to retrieve
MIN_YEAR_THRESHOLD=2020        # Filter old papers

# Server
DEBUG=True                     # Set False in production
LOG_LEVEL=INFO                 # DEBUG | INFO | WARNING | ERROR

# Optional: Redis Caching
# REDIS_URL=redis://localhost:6379
```

---

## Project Architecture

### Backend Stack
- **FastAPI** - Async REST API
- **LangGraph** - Multi-agent workflow
- **Anthropic Claude 3.5** - Validation & generation
- **ChromaDB** - Vector search
- **Sentence Transformers** - Embeddings

### RAG Workflow

```
┌─────────────┐
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  VALIDATE   │  ← Reject unsafe queries
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  RETRIEVE   │  ← Semantic search (top-8)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FILTER    │  ← Quality filtering (keep top-5)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  GENERATE   │  ← LLM answer with citations
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SCORE     │  ← Confidence calculation
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Response   │
└─────────────┘
```

### Directory Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Environment settings
│   ├── api/
│   │   ├── routes.py           # REST endpoints
│   │   └── schemas.py          # Pydantic models
│   ├── rag/
│   │   ├── graph.py            # LangGraph workflow
│   │   ├── types.py            # State TypedDict
│   │   ├── nodes/              # Workflow nodes
│   │   │   ├── validator.py   # Safety validation
│   │   │   ├── retriever.py   # Vector search
│   │   │   ├── filter.py      # Quality filtering
│   │   │   ├── generator.py   # LLM answer generation
│   │   │   └── scorer.py      # Confidence scoring
│   │   ├── prompts/            # LLM prompts
│   │   └── utils/              # Citation & scoring utilities
│   ├── vectorstore/            # ChromaDB integration
│   ├── llm/                    # Anthropic client
│   └── cache/                  # Redis (optional)
├── data/
│   ├── chroma_db/              # Vector database
│   └── sample_papers/          # Sample medical papers
├── scripts/
│   └── ingest_documents.py     # Data ingestion
├── run.py                      # Server entry point
└── requirements.txt
```

---

## API Reference

### POST /api/query

**Request:**
```json
{
  "query": "What are the latest treatments for type 2 diabetes?"
}
```

**Response:**
```json
{
  "answer": "Based on recent research [1][2], metformin...",
  "sources": [
    {
      "id": "1",
      "title": "Type 2 Diabetes Treatment Guidelines 2023",
      "authors": ["Smith J", "Doe A"],
      "journal": "Nature Medicine",
      "year": 2023,
      "pubmedId": "12345678",
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678"
    }
  ],
  "confidence": 0.85,
  "processing_time_ms": 1234,
  "query_validated": true,
  "citations_in_text": [1, 2],
  "warning_message": null
}
```

**Query Validation:**
Queries are rejected if they request:
- Personal diagnosis ("What do I have?")
- Personal treatment ("Prescribe X for me")
- Emergency medical help ("I'm dying")

**Confidence Score:**
- **0.8-1.0**: High confidence (5+ high-quality sources)
- **0.5-0.8**: Medium confidence (3-4 sources)
- **0.0-0.5**: Low confidence (1-2 sources or old data)

---

## Adding Your Own Documents

### 1. Prepare Documents

Create `.txt` files in `data/sample_papers/` with this format:

```
Title: Your Research Paper Title
Authors: Author 1, Author 2, Author 3
Journal: Journal of Medical Research
Year: 2023
PubMed ID: 12345678
URL: https://pubmed.ncbi.nlm.nih.gov/12345678

[Abstract or full text starts here...]

This is the content of your paper. It will be chunked
and embedded into the vector database.
```

### 2. Ingest Into ChromaDB

```bash
python scripts/ingest_documents.py
```

The script will:
1. Load all `.txt` files from `data/sample_papers/`
2. Extract metadata (title, authors, year, etc.)
3. Chunk documents (400 chars, 80 char overlap)
4. Generate embeddings (sentence-transformers)
5. Store in ChromaDB
6. Test retrieval

### 3. Verify Ingestion

```bash
# Check ChromaDB directory
ls data/chroma_db/

# Test query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What did you find about [your topic]?"}'
```

---

## Troubleshooting

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'langchain_community'`

**Fix:**
```bash
pip install --upgrade -r requirements.txt
```

### ChromaDB Errors

**Error:** `sqlite3.OperationalError: database is locked`

**Fix:**
```bash
# Stop all running instances
pkill -f uvicorn
pkill -f python

# Restart server
python run.py
```

### Empty Responses

**Error:** API returns "Insufficient research evidence"

**Fix:**
```bash
# Check if data is ingested
python scripts/ingest_documents.py

# Verify ChromaDB directory exists
ls data/chroma_db/

# Check document count
python -c "
from app.vectorstore.chromadb_init import initialize_vectorstore
vs = initialize_vectorstore()
print(f'Documents in DB: {vs._collection.count()}')
"
```

### API Key Errors

**Error:** `AuthenticationError: Invalid API key`

**Fix:**
1. Get key from: https://console.anthropic.com/
2. Update `.env`:
```env
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```
3. Restart server: `python run.py`

### CORS Errors (Frontend)

**Error:** `Access-Control-Allow-Origin` blocked

**Fix:**
Check `app/main.py` has correct frontend URL:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Match your frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance Optimization

### Enable Redis Caching (Optional)

1. Install Redis:
```bash
# Windows: Download from https://redis.io/download
# Mac: brew install redis
# Linux: sudo apt install redis
```

2. Start Redis:
```bash
redis-server
```

3. Update `.env`:
```env
REDIS_URL=redis://localhost:6379
```

4. Uncomment cache code in `app/cache/redis_cache.py`

### Batch Processing

For multiple queries, use async batch processing:

```python
import asyncio
import httpx

async def batch_query(queries):
    async with httpx.AsyncClient() as client:
        tasks = [
            client.post(
                "http://localhost:8000/api/query",
                json={"query": q}
            )
            for q in queries
        ]
        return await asyncio.gather(*tasks)

# Usage
queries = [
    "What are diabetes treatments?",
    "How does metformin work?",
    "What are Alzheimer's biomarkers?"
]

results = asyncio.run(batch_query(queries))
```

---

## Production Deployment

### 1. Update Configuration

```env
DEBUG=False
LOG_LEVEL=WARNING
LLM_TEMPERATURE=0
```

### 2. Use Production Server

```bash
# Install production server
pip install gunicorn

# Run with workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### 3. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Environment Variables

Use secrets management:
- AWS Secrets Manager
- HashiCorp Vault
- Docker secrets

Never commit `.env` to git!

---

## Testing

### Unit Tests

```bash
pytest tests/
```

### Integration Test

```bash
# Start server in background
python run.py &

# Run integration tests
pytest tests/integration/

# Stop server
pkill -f uvicorn
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host http://localhost:8000
```

---

## Support & Resources

- **LangChain Docs**: https://python.langchain.com/
- **LangGraph Guide**: https://langchain-ai.github.io/langgraph/
- **Anthropic API**: https://docs.anthropic.com/
- **ChromaDB Docs**: https://docs.trychroma.com/

---

## Next Steps

1. ✅ **Basic Setup** - You've completed this!
2. 🔄 **Add Real Data** - Replace sample papers with real medical research
3. 📊 **Evaluate RAG** - Use RAGAS for quality metrics
4. 🚀 **Deploy** - Move to production with proper scaling
5. 🎨 **Customize** - Adjust prompts for your domain

**Need help?** Check the troubleshooting section above or review the README.md.
