import { Source } from '@/data/mockData';
import { Card, CardContent } from '@/components/ui/card';
import { ExternalLink, BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SourceCardProps {
  source: Source;
  index: number;
  className?: string;
}

export const SourceCard = ({ source, index, className }: SourceCardProps) => {
  return (
    <Card className={cn(
      'group cursor-pointer transition-all duration-200 hover:shadow-md hover:border-primary/30',
      className
    )}>
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary font-semibold text-sm">
            [{index + 1}]
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="font-medium text-sm text-foreground line-clamp-2 group-hover:text-primary transition-colors">
              {source.title}
            </h4>
            <p className="text-xs text-muted-foreground mt-1 line-clamp-1">
              {source.authors.join(', ')}
            </p>
            <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
              <BookOpen className="h-3 w-3" />
              <span className="truncate">{source.journal}</span>
              <span>•</span>
              <span>{source.year}</span>
            </div>
          </div>
          <a 
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="shrink-0 p-2 rounded-md hover:bg-muted transition-colors"
            onClick={(e) => e.stopPropagation()}
          >
            <ExternalLink className="h-4 w-4 text-muted-foreground group-hover:text-primary" />
          </a>
        </div>
        <div className="mt-2 pt-2 border-t border-border/50">
          <span className="text-xs font-mono text-muted-foreground">
            PubMed ID: {source.pubmedId}
          </span>
        </div>
      </CardContent>
    </Card>
  );
};