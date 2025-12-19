from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import time
import logging
from io import BytesIO
from uuid import uuid4

from app.api.schemas import QueryRequest, RAGResponse, HealthCheck
from app.rag.graph import rag_graph
from app.rag.nodes.retriever import get_vectorstore
from app.vectorstore.document_loader import chunk_documents, extract_metadata_from_content
from langchain_core.documents import Document
from pypdf import PdfReader

router = APIRouter(prefix="/api", tags=["medical_rag"])

# POST /api/query - Main RAG endpoint
@router.post("/query")
async def process_medical_query(request: QueryRequest) -> RAGResponse:
    """
    Main endpoint: Accept medical research query, return grounded answer
    """
    start = time.time()
    
    try:
        # Run LangGraph workflow
        result = await rag_graph.ainvoke(
            {
                "query": request.query,
                "include_guidelines": request.include_guidelines
            }
        )
        
        processing_time = (time.time() - start) * 1000
        
        return RAGResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
            processing_time_ms=processing_time,
            query_validated=result["query_validated"],
            warning_message=result.get("warning"),
            citations_in_text=result["citation_indices"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"RAG pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail="RAG processing failed")

# GET /api/health - Health check
@router.get("/health")
async def health_check() -> HealthCheck:
    """System status endpoint"""
    try:
        vs = get_vectorstore()
        vectorstore_loaded = vs is not None and vs._collection.count() > 0
    except:
        vectorstore_loaded = False
        
    return HealthCheck(
        status="operational",
        vectorstore_loaded=vectorstore_loaded,
        llm_available=True  # Check Anthropic API
    )

# POST /api/suggest - Query suggestions
@router.post("/suggest")
async def get_query_suggestions(prefix: str) -> dict:
    """Auto-complete suggestions"""
    suggestions = [
        "What are current treatments for Type 2 Diabetes?",
        "Compare Metformin vs Insulin efficacy",
        "Latest research on Alzheimer's biomarkers"
    ]
    return {"suggestions": suggestions}


# POST /api/upload - Upload and ingest a paper (pdf/txt)
@router.post("/upload")
async def upload_paper(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    authors: str | None = Form(None),
    journal: str | None = Form(None),
    year: int | None = Form(None),
    url: str | None = Form(None),
) -> dict:
    # Size guard (10 MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    text: str = ""
    if file.content_type == "application/pdf" or (file.filename and file.filename.lower().endswith(".pdf")):
        try:
            reader = PdfReader(BytesIO(content))
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception:
            raise HTTPException(status_code=400, detail="Unable to read PDF; ensure it is not scanned or encrypted")
    elif file.content_type in {"text/plain", "application/octet-stream"} or (file.filename and file.filename.lower().endswith(".txt")):
        text = content.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type; upload PDF or TXT")

    if not text.strip():
        raise HTTPException(status_code=400, detail="File is empty or text could not be extracted")

    # Derive metadata; fallback to header extraction for txt content
    derived = extract_metadata_from_content(text, file.filename or "uploaded.txt")
    authors_val = authors if authors is not None else derived.get("authors", "")
    if isinstance(authors_val, list):
        authors_val = "; ".join(authors_val)

    metadata = {
        "source": file.filename or f"upload-{uuid4()}",
        "title": title or derived.get("title", "Unknown"),
        "authors": authors_val or "",
        "journal": journal or derived.get("journal", "Unknown"),
        "year": year or derived.get("year", 2023),
        "pubmedId": derived.get("pubmedId", ""),
        "url": url or derived.get("url", ""),
    }

    document = Document(page_content=text, metadata=metadata)
    chunks = chunk_documents([document])

    try:
        vectorstore = get_vectorstore()
        vectorstore.add_documents(chunks)
    except Exception as e:
        logging.error(f"Upload ingest failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to store document")

    return {
        "status": "ok",
        "chunks_added": len(chunks),
        "title": metadata["title"],
        "document_id": metadata["source"],
    }