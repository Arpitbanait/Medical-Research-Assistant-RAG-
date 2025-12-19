import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import os
from app.config import settings

# These are where we actually are - this is the backend root
backend_root = os.path.dirname(os.path.abspath(__file__))
chroma_path_correct = os.path.join(backend_root, settings.chroma_db_path)

# This is what the retriever calculates - it's in app/rag/nodes/retriever.py
# So it goes up 4 levels
retriever_file = os.path.join(backend_root, 'app', 'rag', 'nodes', 'retriever.py')
BACKEND_ROOT_retriever = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(retriever_file))))
chroma_path_retriever = os.path.join(BACKEND_ROOT_retriever, settings.chroma_db_path)

print(f"Current working directory: {os.getcwd()}")
print(f"Backend root (from debug_path.py): {backend_root}")
print(f"Correct path: {chroma_path_correct}")
print(f"Correct path exists: {os.path.exists(chroma_path_correct)}")
print()
print(f"Retriever would compute (from retriever.py): {BACKEND_ROOT_retriever}")
print(f"Retriever path: {chroma_path_retriever}")
print(f"Retriever path exists: {os.path.exists(chroma_path_retriever)}")

