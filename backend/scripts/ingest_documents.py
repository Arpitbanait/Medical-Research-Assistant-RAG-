"""
Document loader and ingestion pipeline for Medical Research RAG.
Loads sample papers and populates the ChromaDB vector store.
"""
import os
import sys
from pathlib import Path
from typing import List

# Add backend to path
BACKEND_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.config import settings


def load_text_files(directory: str) -> List[Document]:
    """Load all text files from a directory."""
    documents = []
    data_dir = Path(directory)
    
    if not data_dir.exists():
        print(f"Directory not found: {directory}")
        return documents
    
    for file_path in data_dir.glob("*.txt"):
        print(f"Loading: {file_path.name}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract metadata from first few lines
        metadata = extract_metadata(content, file_path.name)
        
        doc = Document(
            page_content=content,
            metadata=metadata
        )
        documents.append(doc)
    
    print(f"Loaded {len(documents)} documents")
    return documents


def extract_metadata(content: str, filename: str) -> dict:
    """Extract metadata from document headers."""
    metadata = {
        "source": filename,
        "title": "Unknown",
        "authors": "",
        "journal": "Unknown",
        "year": 2023,
        "pubmedId": "",
        "url": "",
    }
    
    lines = content.split("\n")
    for line in lines[:20]:  # Check first 20 lines
        line = line.strip()
        if line.startswith("Title:"):
            metadata["title"] = line.replace("Title:", "").strip()
        elif line.startswith("Authors:"):
            # Keep as comma-separated string for ChromaDB compatibility
            metadata["authors"] = line.replace("Authors:", "").strip()
        elif line.startswith("Journal:"):
            metadata["journal"] = line.replace("Journal:", "").strip()
        elif line.startswith("Year:"):
            try:
                metadata["year"] = int(line.replace("Year:", "").strip())
            except ValueError:
                pass
        elif line.startswith("PubMed ID:") or line.startswith("Document ID:"):
            metadata["pubmedId"] = line.split(":", 1)[1].strip()
        elif line.startswith("URL:"):
            metadata["url"] = line.replace("URL:", "").strip()
    
    return metadata


def chunk_documents(documents: List[Document]) -> List[Document]:
    """Split documents into smaller chunks for better retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks


def ingest_documents():
    """Main ingestion pipeline."""
    print("=" * 60)
    print("Medical Research RAG - Document Ingestion")
    print("=" * 60)
    
    # Paths
    sample_papers_dir = BACKEND_ROOT / "data" / "sample_papers"
    chroma_path = BACKEND_ROOT / settings.chroma_db_path
    
    print(f"\nSample papers directory: {sample_papers_dir}")
    print(f"ChromaDB path: {chroma_path}")
    
    # Load documents
    print("\n1. Loading documents...")
    documents = load_text_files(sample_papers_dir)
    
    if not documents:
        print("❌ No documents found. Exiting.")
        return
    
    # Chunk documents
    print("\n2. Chunking documents...")
    chunks = chunk_documents(documents)
    
    # Initialize embeddings
    print("\n3. Initializing embeddings model...")
    print(f"Model: {settings.embedding_model}")
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model
    )
    
    # Create vector store
    print("\n4. Creating ChromaDB vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=settings.chroma_collection_name,
        persist_directory=str(chroma_path)
    )
    
    print(f"✅ Successfully ingested {len(chunks)} chunks into ChromaDB")
    print(f"Collection: {settings.chroma_collection_name}")
    
    # Test retrieval
    print("\n5. Testing retrieval...")
    test_query = "What is the first-line treatment for type 2 diabetes?"
    results = vectorstore.similarity_search(test_query, k=3)
    
    print(f"\nQuery: {test_query}")
    print(f"Retrieved {len(results)} documents:\n")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.metadata.get('title', 'Unknown')}")
        print(f"   Snippet: {doc.page_content[:150]}...\n")
    
    print("=" * 60)
    print("✅ Ingestion complete!")
    print("=" * 60)


if __name__ == "__main__":
    ingest_documents()
