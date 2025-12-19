import requests

# Test upload endpoint
url = "http://localhost:8000/api/upload"

# Create a simple test file
files = {'file': ('test.txt', 'Title: Test Paper\nAuthors: Smith, J.\nJournal: Test\nYear: 2024\n\nThis is test content for the paper.', 'text/plain')}

try:
    response = requests.post(url, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
