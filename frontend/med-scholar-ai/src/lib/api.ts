const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface Source {
  id: string;
  title: string;
  authors: string[];
  journal: string;
  year: number;
  pubmedId: string;
  url: string;
  relevance_score?: number;
}

export interface RAGResponse {
  answer: string;
  sources: Source[];
  confidence: number;
  processing_time_ms: number;
  query_validated: boolean;
  warning_message?: string | null;
  citations_in_text?: number[];
}

export interface UploadResponse {
  status: string;
  chunks_added: number;
  title: string;
  document_id: string;
}

export async function sendQuery(query: string, includeGuidelines = true): Promise<RAGResponse> {
  const response = await fetch(`${API_BASE}/api/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query, include_guidelines: includeGuidelines })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API ${response.status}: ${text}`);
  }

  const data = await response.json();
  return data as RAGResponse;
}

export async function sendUpload(file: File, meta?: { title?: string; authors?: string; journal?: string; year?: number; url?: string; }): Promise<UploadResponse> {
  const form = new FormData();
  form.append('file', file);
  if (meta?.title) form.append('title', meta.title);
  if (meta?.authors) form.append('authors', meta.authors);
  if (meta?.journal) form.append('journal', meta.journal);
  if (meta?.year) form.append('year', String(meta.year));
  if (meta?.url) form.append('url', meta.url);

  const response = await fetch(`${API_BASE}/api/upload`, {
    method: 'POST',
    body: form,
  });

  if (!response.ok) {
    let errorMsg = `${response.status} ${response.statusText}`;
    try {
      const errorData = await response.json();
      errorMsg = errorData.detail || JSON.stringify(errorData);
      console.error('Upload error detail:', errorData);
    } catch {
      const text = await response.text();
      if (text) errorMsg = text;
      console.error('Upload error text:', text);
    }
    console.error('Upload failed:', errorMsg);
    throw new Error(errorMsg);
  }

  return (await response.json()) as UploadResponse;
}
