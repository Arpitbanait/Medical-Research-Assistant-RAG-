"""Document loading and processing utilities."""
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings


def load_text_file(file_path: Path) -> Document:
    """Load a single text file as a Document."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = extract_metadata_from_content(content, file_path.name)
    
    return Document(
        page_content=content,
        metadata=metadata
    )


def extract_metadata_from_content(content: str, filename: str) -> dict:
    """Extract metadata from document headers."""
    metadata = {
        "source": filename,
        "title": "Unknown",
        "authors": [],
        "journal": "Unknown",
        "year": 2023,
        "pubmedId": "",
        "url": "",
    }
    
    lines = content.split('\n')
    for line in lines[:20]:  # Check first 20 lines for metadata
        line = line.strip()
        if line.startswith('Title:'):
            metadata['title'] = line.replace('Title:', '').strip()
        elif line.startswith('Authors:'):
            authors_str = line.replace('Authors:', '').strip()
            metadata['authors'] = [a.strip() for a in authors_str.split(';')]
        elif line.startswith('Journal:'):
            metadata['journal'] = line.replace('Journal:', '').strip()
        elif line.startswith('Year:'):
            try:
                metadata['year'] = int(line.replace('Year:', '').strip())
            except ValueError:
                pass
        elif line.startswith('PubMed ID:') or line.startswith('Document ID:'):
            metadata['pubmedId'] = line.split(':', 1)[1].strip()
        elif line.startswith('URL:'):
            metadata['url'] = line.replace('URL:', '').strip()
    
    return metadata


def chunk_documents(documents: List[Document], chunk_size: int = 400, chunk_overlap: int = 80) -> List[Document]:
    """Split documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=['\n\n', '\n', '. ', ' ', '']
    )
    
    return text_splitter.split_documents(documents)


def load_directory(directory: Path) -> List[Document]:
    """Load all text files from a directory."""
    documents = []
    
    if not directory.exists():
        return documents
    
    for file_path in directory.glob('*.txt'):
        doc = load_text_file(file_path)
        documents.append(doc)
    
    return documents
