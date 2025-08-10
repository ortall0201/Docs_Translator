import { useState, useEffect } from 'react';
import { Loader2, FileText, Download, CheckCircle, ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { API_BASE_URL } from '@/config/api';

interface TranslationProgressProps {
  isTranslating: boolean;
  translatedFile: string | null;
  onDownload: () => void;
  fileName: string;
}

export const TranslationProgress = ({ 
  isTranslating, 
  translatedFile, 
  onDownload, 
  fileName 
}: TranslationProgressProps) => {
  // Check if this is a Hebrew/RTL language file
  const isRTLLanguage = translatedFile && ['_he_', '_ar_', '_ru_', '_uk_'].some(lang => translatedFile.includes(lang));
  console.log('[DEBUG] DEBUG: TranslationProgress render - isTranslating:', isTranslating, 'translatedFile:', translatedFile);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');

  const steps = [
    'Analyzing document structure...',
    'Extracting text content...',
    'Processing translation...',
    'Optimizing layout...',
    'Finalizing document...',
  ];

  useEffect(() => {
    if (isTranslating) {
      setProgress(0);
      setCurrentStep(steps[0]);
      
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          
          const newProgress = prev + Math.random() * 15;
          const stepIndex = Math.floor((newProgress / 100) * steps.length);
          setCurrentStep(steps[Math.min(stepIndex, steps.length - 1)]);
          
          return Math.min(newProgress, 100);
        });
      }, 800);

      return () => clearInterval(interval);
    } else {
      setProgress(0);
      setCurrentStep('');
    }
  }, [isTranslating]);

  if (translatedFile) {
    return (
      <div className="step-card fade-in">
        <div className="text-center space-y-6">
          <div className="w-16 h-16 mx-auto bg-success/10 rounded-xl flex items-center justify-center">
            <CheckCircle className="w-8 h-8 text-success" />
          </div>
          
          <div className="space-y-2">
            <h3 className="text-xl font-semibold text-foreground">
              Translation Complete!
            </h3>
            <p className="text-muted-foreground">
              Your document has been successfully translated and is ready for download.
            </p>
          </div>

          <div className="p-4 bg-muted/50 rounded-lg border border-border/50">
            <div className="flex items-center justify-center space-x-3">
              <FileText className="w-5 h-5 text-primary" />
              <span className="font-medium text-foreground">
                {fileName.replace('.pdf', '_translated.pdf')}
              </span>
            </div>
          </div>

          <div className="space-y-3">
            <Button 
              onClick={() => {
                const viewUrl = `${API_BASE_URL}/preview/${translatedFile}`;
                console.log('[DEBUG] DEBUG: Opening view URL:', viewUrl);
                window.open(viewUrl, '_blank');
              }}
              variant="outline"
              className="w-full h-12 border-2 hover:bg-muted/50 transition-colors"
              size="lg"
            >
              <ExternalLink className="w-5 h-5 mr-2" />
              View Translated File
            </Button>

            <Button 
              onClick={onDownload} 
              className="w-full h-12 bg-gradient-primary hover:opacity-90 transition-opacity"
              size="lg"
            >
              {isRTLLanguage ? (
                <>
                  <ExternalLink className="w-5 h-5 mr-2" />
                  Open Print/PDF Preview
                </>
              ) : (
                <>
                  <Download className="w-5 h-5 mr-2" />
                  Download Translated Document
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (isTranslating) {
    return (
      <div className="step-card fade-in">
        <div className="space-y-6">
          <div className="text-center space-y-4">
            <div className="w-16 h-16 mx-auto bg-primary/10 rounded-xl flex items-center justify-center">
              <Loader2 className="w-8 h-8 text-primary animate-spin" />
            </div>
            
            <div className="space-y-2">
              <h3 className="text-lg font-semibold text-foreground">
                Translating Document
              </h3>
              <p className="text-sm text-muted-foreground">
                {currentStep}
              </p>
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Progress</span>
              <span className="text-foreground font-medium">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          <div className="flex items-center justify-center text-xs text-muted-foreground">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
              <span>This may take a few moments depending on document size</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};