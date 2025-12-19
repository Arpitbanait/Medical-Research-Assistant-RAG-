# Medical Research RAG Backend

AI-powered medical research assistant using RAG (Retrieval Augmented Generation) with LangChain, LangGraph, and Anthropic Claude.

## Architecture

- **FastAPI** - REST API server
- **LangGraph** - Multi-agent workflow orchestration
- **Anthropic Claude 3.5 Sonnet** - LLM for validation and generation
- **ChromaDB** - Vector database for semantic search
- **Sentence Transformers** - Embeddings (all-MiniLM-L6-v2)

## Workflow

```
Query → Validate → Retrieve → Filter → Generate → Score → Response
```

1. **Validate**: Safety check (reject personal diagnosis/emergency queries)
2. **Retrieve**: Semantic search in ChromaDB (top-8 documents)
3. **Filter**: Quality filtering (year ≥ 2020, PubMed/DOI sources, keep top-5)
4. **Generate**: LLM answer with strict citation enforcement
5. **Score**: Confidence calculation based on sources and quality

## Setup

### Prerequisites
- Python 3.9+
- Anthropic API key

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Configuration

Create `.env` file:

```env
ANTHROPIC_API_KEY=your_key_here

# Optional overrides
CHROMA_DB_PATH=data/chroma_db
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
RETRIEVAL_TOP_K=8
MIN_YEAR_THRESHOLD=2020
LLM_TEMPERATURE=0
LLM_MAX_TOKENS=4000
DEBUG=True
LOG_LEVEL=INFO
```

### Ingest Sample Data

```bash
python scripts/ingest_documents.py
```

This loads sample medical papers into ChromaDB.

### Run Server

```bash
# Option 1: Using run.py
python run.py

# Option 2: Direct uvicorn
uvicorn app.main:app --reload --port 8000
```

Server runs at: `http://localhost:8000`

## API Endpoints

### POST /api/query
Query the medical research database.

**Request:**
```json
{
  "query": "What are the latest treatments for type 2 diabetes?"
}
```

**Response:**
```json
{
  "answer": "Based on research [1][2], metformin remains first-line...",
  "sources": [
    {
      "id": "doc_123",
      "title": "Type 2 Diabetes Treatment Guidelines",
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

### GET /api/health
Health check endpoint.

### POST /api/suggest
Get query suggestions (placeholder).

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Pydantic settings
│   ├── api/
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Pydantic models
│   ├── rag/
│   │   ├── graph.py         # LangGraph workflow
│   │   ├── types.py         # TypedDict state
│   │   ├── nodes/           # RAG nodes
│   │   │   ├── validator.py
│   │   │   ├── retriever.py
│   │   │   ├── filter.py
│   │   │   ├── generator.py
│   │   │   └── scorer.py
│   │   ├── prompts/         # LLM prompts
│   │   │   ├── validation.py
│   │   │   ├── generation.py
│   │   │   └── templates.py
│   │   └── utils/           # Utilities
│   │       ├── citations.py
│   │       └── scoring.py
│   ├── vectorstore/
│   │   ├── embeddings.py
│   │   ├── chromadb_init.py
│   │   └── document_loader.py
│   ├── llm/
│   │   └── anthropic_client.py
│   └── cache/
│       └── redis_cache.py
├── data/
│   ├── chroma_db/           # Vector database
│   └── sample_papers/       # Sample documents
├── scripts/
│   └── ingest_documents.py  # Data ingestion
├── run.py                   # Entry point
└── requirements.txt
```

## Key Features

✅ **Strict Grounding**: Answers ONLY from retrieved documents, no hallucinations
✅ **Citation Enforcement**: Every claim must reference sources with [1], [2], etc.
✅ **Safety Validation**: Rejects personal diagnosis/emergency queries
✅ **Quality Filtering**: Prioritizes recent (≥2020) and reputable sources (PubMed, DOI)
✅ **Confidence Scoring**: Transparent scoring based on source quality and quantity
✅ **Schema Alignment**: API matches frontend TypeScript types (camelCase fields)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Required | Anthropic API key |
| `CHROMA_DB_PATH` | `data/chroma_db` | ChromaDB persistence path |
| `ANTHROPIC_MODEL` | `claude-3-5-sonnet-20241022` | Claude model |
| `RETRIEVAL_TOP_K` | `8` | Number of documents to retrieve |
| `MIN_YEAR_THRESHOLD` | `2020` | Minimum publication year |
| `LLM_TEMPERATURE` | `0` | LLM temperature (0=deterministic) |
| `LLM_MAX_TOKENS` | `4000` | Max tokens per response |
| `DEBUG` | `True` | Debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |

## Development

### Add New Documents

Place `.txt` files in `data/sample_papers/` with this format:

```
Title: Your Paper Title
Authors: Author 1, Author 2, Author 3
Journal: Journal Name
Year: 2023
PubMed ID: 12345678
URL: https://pubmed.ncbi.nlm.nih.gov/12345678

[Paper content starts here...]
```

Then run: `python scripts/ingest_documents.py`

### Testing

```bash
# Health check
curl http://localhost:8000/api/health

# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are metformin benefits for diabetes?"}'
```

## Frontend Integration

Backend is CORS-enabled for `http://localhost:8080` (React frontend).

Start backend first, then frontend will connect automatically.

## Troubleshooting

**ChromaDB path errors:**
- Ensure `data/chroma_db` exists or run ingestion script

**Empty responses:**
- Check if documents are ingested: `ls data/chroma_db/`
- Verify `ANTHROPIC_API_KEY` is set

**Import errors:**
- Reinstall dependencies: `pip install -r requirements.txt`
- Use Python 3.9+

**CORS errors:**
- Frontend URL must be `http://localhost:8080`
- Check CORS config in `app/main.py`

## License

MIT
