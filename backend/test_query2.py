from app.main import app
from fastapi.testclient import TestClient
import json

c = TestClient(app)
resp = c.post('/api/query', json={
    'query': 'Compare the efficacy of different diabetes treatments',
    'include_guidelines': False
})

data = resp.json()
print(f"Query validated: {data['query_validated']}")
print(f"Sources found: {len(data['sources'])}")
print(f"Confidence: {data['confidence']:.2%}")
print(f"Answer length: {len(data['answer'])} chars")
print(f"Status code: {resp.status_code}")
