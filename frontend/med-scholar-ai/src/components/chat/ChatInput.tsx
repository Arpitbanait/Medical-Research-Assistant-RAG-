import { useState, KeyboardEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Send, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
  className?: string;
}

export const ChatInput = ({ onSend, isLoading, disabled, className }: ChatInputProps) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !isLoading && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestions = [
    'What are current treatments for Type 2 Diabetes?',
    'Compare Metformin vs Insulin efficacy',
    'Latest research on Alzheimer\'s biomarkers',
  ];

  return (
    <div className={cn('space-y-3', className)}>
      {/* Quick Suggestions */}
      {!input && (
        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => setInput(suggestion)}
              className="text-xs px-3 py-1.5 rounded-full bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      {/* Input Area */}
      <div className="relative flex items-end gap-2 p-2 rounded-xl bg-card border border-border shadow-sm">
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a medical research question..."
          disabled={isLoading || disabled}
          className="min-h-[44px] max-h-[200px] resize-none border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 text-sm pr-12"
          rows={1}
        />
        <Button
          onClick={handleSend}
          disabled={!input.trim() || isLoading || disabled}
          size="icon"
          className="shrink-0 h-10 w-10 rounded-lg"
        >
          {isLoading ? (
            <Loader2 className="h-5 w-5 animate-spin" />
          ) : (
            <Send className="h-5 w-5" />
          )}
        </Button>
      </div>

      {/* Disclaimer */}
      <p className="text-xs text-center text-muted-foreground">
        For research and academic purposes only. Not medical advice.
      </p>
    </div>
  );
};