import { ChatMessage as ChatMessageType } from '@/data/mockData';
import { ConfidenceScore } from './ConfidenceScore';
import { SourceCard } from './SourceCard';
import { cn } from '@/lib/utils';
import { User, Bot, AlertTriangle } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const [sourcesExpanded, setSourcesExpanded] = useState(false);
  const isUser = message.role === 'user';
  const isWarning = message.isWarning;

  const formatContent = (content: string) => {
    return content.split('\n').map((line, i) => {
      // Bold text
      let formatted = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // Citations
      formatted = formatted.replace(/\[(\d+)\]/g, '<span class="text-primary font-semibold">[$1]</span>');
      
      if (line.startsWith('- ')) {
        return (
          <li key={i} className="ml-4" dangerouslySetInnerHTML={{ __html: formatted.slice(2) }} />
        );
      }
      if (line.trim() === '') {
        return <br key={i} />;
      }
      return (
        <p key={i} className="mb-2" dangerouslySetInnerHTML={{ __html: formatted }} />
      );
    });
  };

  return (
    <div className={cn(
      'flex gap-3 animate-slide-in',
      isUser ? 'flex-row-reverse' : 'flex-row'
    )}>
      {/* Avatar */}
      <div className={cn(
        'flex h-9 w-9 shrink-0 items-center justify-center rounded-full',
        isUser ? 'bg-chat-user' : isWarning ? 'bg-destructive' : 'bg-primary/10'
      )}>
        {isUser ? (
          <User className="h-5 w-5 text-chat-user-foreground" />
        ) : isWarning ? (
          <AlertTriangle className="h-5 w-5 text-destructive-foreground" />
        ) : (
          <Bot className="h-5 w-5 text-primary" />
        )}
      </div>

      {/* Message Content */}
      <div className={cn(
        'flex flex-col max-w-[80%]',
        isUser ? 'items-end' : 'items-start'
      )}>
        <div className={cn(
          'rounded-2xl px-4 py-3',
          isUser 
            ? 'bg-chat-user text-chat-user-foreground rounded-tr-sm' 
            : isWarning
            ? 'bg-destructive/10 text-foreground border border-destructive/20 rounded-tl-sm'
            : 'bg-chat-ai text-chat-ai-foreground rounded-tl-sm'
        )}>
          <div className="text-sm leading-relaxed prose prose-sm max-w-none">
            {formatContent(message.content)}
          </div>
        </div>

        {/* Confidence Score */}
        {!isUser && message.confidence !== undefined && !isWarning && (
          <div className="mt-2 px-2">
            <ConfidenceScore score={message.confidence} />
          </div>
        )}

        {/* Sources */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-3 w-full">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSourcesExpanded(!sourcesExpanded)}
              className="text-muted-foreground hover:text-foreground"
            >
              {sourcesExpanded ? (
                <ChevronUp className="h-4 w-4 mr-1" />
              ) : (
                <ChevronDown className="h-4 w-4 mr-1" />
              )}
              {message.sources.length} Source{message.sources.length > 1 ? 's' : ''}
            </Button>
            
            {sourcesExpanded && (
              <div className="mt-2 grid gap-2">
                {message.sources.map((source, index) => (
                  <SourceCard key={source.id} source={source} index={index} />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Timestamp */}
        <span className="text-xs text-muted-foreground mt-1 px-2">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  );
};