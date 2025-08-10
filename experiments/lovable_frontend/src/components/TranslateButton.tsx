import { Zap, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface TranslateButtonProps {
  onTranslate: () => void;
  disabled: boolean;
  isTranslating: boolean;
}

export const TranslateButton = ({ onTranslate, disabled, isTranslating }: TranslateButtonProps) => {
  if (disabled || isTranslating) {
    return null;
  }

  return (
    <div className="step-card fade-in">
      <div className="text-center space-y-6">
        <div className="space-y-2">
          <h3 className="text-lg font-semibold text-foreground">
            Ready to Translate
          </h3>
          <p className="text-muted-foreground">
            Your document and target language are set. Click below to start the translation process.
          </p>
        </div>

        <Button
          onClick={onTranslate}
          size="lg"
          className="w-full h-14 bg-gradient-primary hover:opacity-90 transition-all duration-300 text-lg font-semibold group"
        >
          <Zap className="w-6 h-6 mr-3 group-hover:scale-110 transition-transform" />
          Start Translation
          <ArrowRight className="w-5 h-5 ml-3 group-hover:translate-x-1 transition-transform" />
        </Button>

        <div className="flex items-center justify-center space-x-4 text-xs text-muted-foreground">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-success rounded-full"></div>
            <span>Secure Processing</span>
          </div>
          <span>•</span>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-tech-blue rounded-full"></div>
            <span>AI Powered</span>
          </div>
          <span>•</span>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-warning rounded-full"></div>
            <span>Format Preserved</span>
          </div>
        </div>
      </div>
    </div>
  );
};