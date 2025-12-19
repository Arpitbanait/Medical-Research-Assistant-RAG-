import requests
import json

# Test the query endpoint
url = "http://localhost:8000/api/query"

# Valid input matching the schema
payload = {
    "query": "What are the latest treatments for Type 2 Diabetes?",
    "session_id": "test-session-123",
    "include_guidelines": True
}

print("Sending request to:", url)
print("Payload:", json.dumps(payload, indent=2))
print("\n" + "="*60 + "\n")

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Query Validated: {data.get('query_validated')}")
        print(f"Sources Found: {len(data.get('sources', []))}")
        print(f"Confidence: {data.get('confidence', 0):.1%}")
        print(f"Processing Time: {data.get('processing_time_ms', 0):.0f}ms")
        print(f"\nAnswer Preview:\n{data.get('answer', '')[:300]}...")
        
        if data.get('sources'):
            print(f"\nTop 3 Sources:")
            for src in data['sources'][:3]:
                print(f"  • {src['title']}")
                print(f"    Authors: {', '.join(src['authors'][:2])}...")
                print(f"    {src['journal']} ({src['year']})")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: Is the server running on port 8000?")
    print("Start server with: uvicorn app.main:app --reload")
except Exception as e:
    print(f"❌ Error: {e}")
