import os

# Simulate retriever.py path
retriever_file = r"C:\Users\HP\Desktop\Medical_Research_RAG\backend\app\rag\nodes\retriever.py"

print(f"File: {retriever_file}")
print(f"Dir 1: {os.path.dirname(retriever_file)}")
print(f"Dir 2: {os.path.dirname(os.path.dirname(retriever_file))}")
print(f"Dir 3: {os.path.dirname(os.path.dirname(os.path.dirname(retriever_file)))}")
print(f"Dir 4: {os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(retriever_file))))}")

backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(retriever_file))))
print(f"\nBACKEND_ROOT (3 levels): {backend_root}")
print(f"Chroma path would be: {os.path.join(backend_root, 'data/chroma_db')}")
print(f"Exists: {os.path.exists(os.path.join(backend_root, 'data/chroma_db'))}")
