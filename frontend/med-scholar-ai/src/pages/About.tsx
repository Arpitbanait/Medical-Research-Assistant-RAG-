import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Shield, BookOpen, AlertTriangle, Database } from 'lucide-react';
import { Link } from 'react-router-dom';

const About = () => {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card/50">
        <div className="container max-w-4xl py-4">
          <Link to="/">
            <Button variant="ghost" size="sm" className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Chat
            </Button>
          </Link>
        </div>
      </header>

      <main className="container max-w-4xl py-8 px-4">
        <div className="text-center mb-8">
          <h1 className="font-serif text-3xl font-bold text-foreground mb-2">
            Medical Research RAG System
          </h1>
          <p className="text-muted-foreground">
            AI-powered evidence retrieval for medical research
          </p>
        </div>

        {/* Disclaimer Banner */}
        <Card className="mb-8 border-warning/50 bg-warning/5">
          <CardContent className="flex items-start gap-4 p-6">
            <AlertTriangle className="h-6 w-6 text-warning shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-foreground mb-1">Important Disclaimer</h3>
              <p className="text-sm text-muted-foreground">
                This system is designed for <strong>academic, research, and educational purposes only</strong>. 
                It does not provide medical advice, diagnoses, or treatment recommendations. 
                Always consult qualified healthcare professionals for medical decisions.
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Database className="h-5 w-5 text-primary" />
                Data Sources
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <p>Our knowledge base includes:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>PubMed abstracts and papers</li>
                <li>WHO medical guidelines</li>
                <li>CDC recommendations</li>
                <li>Peer-reviewed systematic reviews</li>
                <li>Meta-analyses from major journals</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Shield className="h-5 w-5 text-primary" />
                Safety Features
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <ul className="list-disc list-inside space-y-1">
                <li>Query validation for unsafe requests</li>
                <li>Retrieval-only context (no hallucination)</li>
                <li>Confidence scoring for transparency</li>
                <li>Automatic citation enforcement</li>
                <li>"Insufficient evidence" responses when needed</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <BookOpen className="h-5 w-5 text-primary" />
                How It Works
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-sm text-muted-foreground">
              <div className="grid gap-4 md:grid-cols-4">
                <div className="text-center p-4 rounded-lg bg-secondary/50">
                  <div className="font-semibold text-foreground mb-1">1. Query</div>
                  <p className="text-xs">Your question is validated and processed</p>
                </div>
                <div className="text-center p-4 rounded-lg bg-secondary/50">
                  <div className="font-semibold text-foreground mb-1">2. Retrieve</div>
                  <p className="text-xs">Semantic search finds relevant papers</p>
                </div>
                <div className="text-center p-4 rounded-lg bg-secondary/50">
                  <div className="font-semibold text-foreground mb-1">3. Filter</div>
                  <p className="text-xs">Evidence is ranked by quality</p>
                </div>
                <div className="text-center p-4 rounded-lg bg-secondary/50">
                  <div className="font-semibold text-foreground mb-1">4. Generate</div>
                  <p className="text-xs">Answer synthesized with citations</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="mt-8 text-center text-xs text-muted-foreground">
          <p>Built with RAG (Retrieval-Augmented Generation) architecture</p>
          <p className="mt-1">Demo/Academic Project • Not for clinical use</p>
        </div>
      </main>
    </div>
  );
};

export default About;