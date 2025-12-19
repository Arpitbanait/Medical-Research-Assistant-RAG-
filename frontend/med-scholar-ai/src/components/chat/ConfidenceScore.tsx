import { cn } from '@/lib/utils';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';

interface ConfidenceScoreProps {
  score: number;
  className?: string;
}

export const ConfidenceScore = ({ score, className }: ConfidenceScoreProps) => {
  const percentage = Math.round(score * 100);
  
  const getLevel = () => {
    if (score >= 0.8) return { label: 'High', color: 'text-success', bg: 'bg-success', Icon: CheckCircle };
    if (score >= 0.5) return { label: 'Medium', color: 'text-warning', bg: 'bg-warning', Icon: AlertCircle };
    return { label: 'Low', color: 'text-destructive', bg: 'bg-destructive', Icon: XCircle };
  };

  const { label, color, bg, Icon } = getLevel();

  return (
    <div className={cn('flex items-center gap-3', className)}>
      <div className="flex items-center gap-1.5">
        <Icon className={cn('h-4 w-4', color)} />
        <span className={cn('text-sm font-medium', color)}>
          {label} Confidence
        </span>
      </div>
      <div className="flex items-center gap-2">
        <div className="h-2 w-24 rounded-full bg-muted overflow-hidden">
          <div 
            className={cn('h-full rounded-full transition-all duration-500', bg)}
            style={{ width: `${percentage}%` }}
          />
        </div>
        <span className="text-xs text-muted-foreground font-mono">
          {percentage}%
        </span>
      </div>
    </div>
  );
};