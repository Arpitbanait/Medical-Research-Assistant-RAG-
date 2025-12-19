import { useState, useRef, useEffect } from 'react';
import { ChatMessage as ChatMessageComponent } from '@/components/chat/ChatMessage';
import { ChatInput } from '@/components/chat/ChatInput';
import { QueryHistory } from '@/components/chat/QueryHistory';
import { 
  ChatMessage, 
  QueryHistoryItem, 
  unsafeKeywords,
  initialQueryHistory 
} from '@/data/mockData';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  PanelLeftClose, 
  PanelLeft, 
  Plus, 
  Stethoscope,
  Info
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Link } from 'react-router-dom';
import { sendQuery, sendUpload } from '@/lib/api';
import { Input } from '@/components/ui/input';

const Index = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [history, setHistory] = useState<QueryHistoryItem[]>(initialQueryHistory);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadAuthors, setUploadAuthors] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const makeId = () => (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString());

  const handleUpload = async () => {
    if (!uploadFile) {
      setUploadStatus('Select a PDF or TXT first.');
      return;
    }

    setIsUploading(true);
    setUploadStatus('Uploading...');

    try {
      const resp = await sendUpload(uploadFile, {
        title: uploadTitle || undefined,
        authors: uploadAuthors || undefined,
      });

      setUploadStatus(`Ingested ${resp.chunks_added} chunks from "${resp.title}".`);
      setUploadFile(null);
      setUploadTitle('');
      setUploadAuthors('');
    } catch (error: any) {
      setUploadStatus(`Upload failed: ${error?.message || error}`);
    } finally {
      setIsUploading(false);
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const checkUnsafeQuery = (query: string): boolean => {
    return unsafeKeywords.some(keyword => 
      query.toLowerCase().includes(keyword)
    );
  };

  const handleSend = async (query: string) => {
    if (!query.trim()) return;

    const userMessage: ChatMessage = {
      id: makeId(),
      role: 'user',
      content: query,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Check for unsafe query
    if (checkUnsafeQuery(query)) {
      const warningMessage: ChatMessage = {
        id: makeId(),
        role: 'assistant',
        content: `**⚠️ Medical Advice Not Supported**

I cannot provide personal medical advice, diagnoses, or emergency guidance.

This system is designed for **research and educational purposes only**.

For personal health concerns, please:
- Consult a licensed healthcare professional
- Call emergency services if urgent
- Visit your local healthcare facility`,
        timestamp: new Date(),
        isWarning: true,
      };
      setMessages(prev => [...prev, warningMessage]);
      setIsLoading(false);
      return;
    }

    try {
      const response = await sendQuery(query, true);

      const aiMessage: ChatMessage = {
        id: makeId(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
        confidence: response.confidence,
        sources: response.sources ?? [],
        isWarning: !response.query_validated,
      };
      setMessages(prev => [...prev, aiMessage]);

      const historyItem: QueryHistoryItem = {
        id: makeId(),
        query,
        timestamp: new Date(),
        preview: (response.answer || '').slice(0, 80) + '...',
      };
      setHistory(prev => [historyItem, ...prev.slice(0, 9)]);
    } catch (error: any) {
      const errorMessage: ChatMessage = {
        id: makeId(),
        role: 'assistant',
        content: `**Connection issue**\n\nI couldn't reach the backend API. Please ensure the server is running on port 8000.\n\nDetails: ${error?.message || error}`,
        timestamp: new Date(),
        confidence: 0,
        sources: [],
        isWarning: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
  };

  const handleHistorySelect = (query: string) => {
    handleSend(query);
  };

  const handleClearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside className={cn(
        'flex flex-col bg-sidebar border-r border-sidebar-border transition-all duration-300',
        sidebarOpen ? 'w-72' : 'w-0 overflow-hidden'
      )}>
        {/* Sidebar Header */}
        <div className="flex items-center gap-3 px-4 py-4 border-b border-sidebar-border">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <Stethoscope className="h-5 w-5" />
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="font-serif font-bold text-sidebar-foreground truncate">
              MedRAG
            </h1>
            <p className="text-xs text-sidebar-foreground/60">
              Research Assistant
            </p>
          </div>
        </div>

        {/* New Chat Button */}
        <div className="p-3">
          <Button 
            onClick={handleNewChat}
            className="w-full justify-start gap-2"
            variant="outline"
          >
            <Plus className="h-4 w-4" />
            New Research Query
          </Button>
        </div>

        {/* Upload Paper */}
        <div className="px-3 pb-3 space-y-2">
          <div className="text-xs font-semibold text-sidebar-foreground/70">Upload Paper</div>
          <Input
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
          />
          <Input
            placeholder="Title (optional)"
            value={uploadTitle}
            onChange={(e) => setUploadTitle(e.target.value)}
          />
          <Input
            placeholder="Authors e.g. Smith; Doe"
            value={uploadAuthors}
            onChange={(e) => setUploadAuthors(e.target.value)}
          />
          <Button onClick={handleUpload} disabled={isUploading} className="w-full">
            {isUploading ? 'Uploading...' : 'Ingest to RAG'}
          </Button>
          {uploadStatus && (
            <p className="text-xs text-sidebar-foreground/70 leading-snug">{uploadStatus}</p>
          )}
        </div>

        {/* Query History */}
        <QueryHistory
          history={history}
          onSelect={handleHistorySelect}
          onClear={handleClearHistory}
          className="flex-1"
        />

        {/* About Link */}
        <div className="p-3 border-t border-sidebar-border">
          <Link to="/about">
            <Button variant="ghost" size="sm" className="w-full justify-start gap-2 text-sidebar-foreground/70">
              <Info className="h-4 w-4" />
              About & Disclaimer
            </Button>
          </Link>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="flex items-center gap-2 px-4 py-3 border-b border-border bg-card/50">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="shrink-0"
          >
            {sidebarOpen ? (
              <PanelLeftClose className="h-5 w-5" />
            ) : (
              <PanelLeft className="h-5 w-5" />
            )}
          </Button>
          <div className="flex-1">
            <h2 className="font-medium text-sm">Medical Research Assistant</h2>
            <p className="text-xs text-muted-foreground">
              Evidence-based answers from PubMed & medical guidelines
            </p>
          </div>
        </header>

        {/* Messages */}
        <ScrollArea className="flex-1 p-4" ref={scrollRef}>
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center px-4">
              <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-4">
                <Stethoscope className="h-8 w-8 text-primary" />
              </div>
              <h2 className="font-serif text-2xl font-bold text-foreground mb-2">
                Medical Research RAG
              </h2>
              <p className="text-muted-foreground max-w-md mb-6">
                Ask evidence-based questions about medical research. 
                I'll search verified sources and provide citations with confidence scores.
              </p>
              <div className="flex flex-wrap justify-center gap-2 text-xs text-muted-foreground">
                <span className="px-2 py-1 rounded-full bg-secondary">PubMed Papers</span>
                <span className="px-2 py-1 rounded-full bg-secondary">WHO Guidelines</span>
                <span className="px-2 py-1 rounded-full bg-secondary">Systematic Reviews</span>
              </div>
            </div>
          ) : (
            <div className="space-y-6 max-w-3xl mx-auto">
              {messages.map((message) => (
                <ChatMessageComponent key={message.id} message={message} />
              ))}
              {isLoading && (
                <div className="flex gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary/10">
                    <Stethoscope className="h-5 w-5 text-primary animate-pulse-soft" />
                  </div>
                  <div className="bg-chat-ai rounded-2xl rounded-tl-sm px-4 py-3">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span className="animate-pulse-soft">Searching medical literature</span>
                      <span className="flex gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
                        <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
                        <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </ScrollArea>

        {/* Input */}
        <div className="p-4 border-t border-border bg-card/30">
          <div className="max-w-3xl mx-auto">
            <ChatInput onSend={handleSend} isLoading={isLoading} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;