from app.vectorstore.embeddings import get_embeddings
from langchain_chroma import Chroma
import os

embeddings = get_embeddings()
persist_directory = 'data/chroma_db'

if os.path.exists(persist_directory):
    vectorstore = Chroma(
        collection_name='medical_research',
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    print(f'Collection size: {vectorstore._collection.count()}')
    results = vectorstore.similarity_search('metformin diabetes', k=5)
    print(f'Found {len(results)} results')
    for i, doc in enumerate(results):
        print(f'{i+1}. {doc.metadata.get("title", "Unknown")}')
else:
    print('ChromaDB directory not found')
