import { QueryHistoryItem } from '@/data/mockData';
import { cn } from '@/lib/utils';
import { Clock, MessageSquare, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';

interface QueryHistoryProps {
  history: QueryHistoryItem[];
  onSelect: (query: string) => void;
  onClear: () => void;
  className?: string;
}

export const QueryHistory = ({ history, onSelect, onClear, className }: QueryHistoryProps) => {
  const formatDate = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className={cn('flex flex-col h-full', className)}>
      <div className="flex items-center justify-between px-4 py-3 border-b border-sidebar-border">
        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-sidebar-foreground/70" />
          <h2 className="text-sm font-semibold text-sidebar-foreground">History</h2>
        </div>
        {history.length > 0 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onClear}
            className="h-7 px-2 text-xs text-muted-foreground hover:text-destructive"
          >
            <Trash2 className="h-3 w-3 mr-1" />
            Clear
          </Button>
        )}
      </div>

      <ScrollArea className="flex-1">
        {history.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-32 text-center px-4">
            <MessageSquare className="h-8 w-8 text-sidebar-foreground/30 mb-2" />
            <p className="text-xs text-sidebar-foreground/50">
              Your query history will appear here
            </p>
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {history.map((item) => (
              <button
                key={item.id}
                onClick={() => onSelect(item.query)}
                className="w-full text-left p-3 rounded-lg hover:bg-sidebar-accent transition-colors group"
              >
                <p className="text-sm font-medium text-sidebar-foreground line-clamp-2 group-hover:text-sidebar-primary">
                  {item.query}
                </p>
                <p className="text-xs text-sidebar-foreground/50 line-clamp-1 mt-1">
                  {item.preview}
                </p>
                <span className="text-xs text-sidebar-foreground/40 mt-1 block">
                  {formatDate(item.timestamp)}
                </span>
              </button>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
};