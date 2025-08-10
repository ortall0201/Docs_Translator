import { Upload, Languages, Zap, Download, CheckCircle } from 'lucide-react';

interface StepIndicatorProps {
  currentStep: number;
}

const steps = [
  { icon: Upload, label: 'Upload', description: 'Upload PDF document' },
  { icon: Languages, label: 'Language', description: 'Select target language' },
  { icon: Zap, label: 'Translate', description: 'Process translation' },
  { icon: Download, label: 'Download', description: 'Get translated file' },
];

export const StepIndicator = ({ currentStep }: StepIndicatorProps) => {
  return (
    <div className="w-full max-w-4xl mx-auto mb-8">
      <div className="flex items-center justify-between relative">
        {/* Progress line */}
        <div className="absolute top-6 left-0 w-full h-0.5 bg-border -z-10">
          <div 
            className="h-full bg-gradient-primary transition-all duration-500 ease-out"
            style={{ width: `${(currentStep / (steps.length - 1)) * 100}%` }}
          />
        </div>

        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index <= currentStep;
          const isCurrent = index === currentStep;
          
          return (
            <div key={index} className="flex flex-col items-center space-y-2 relative">
              <div 
                className={`
                  w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300
                  ${isActive 
                    ? 'bg-gradient-primary text-primary-foreground shadow-medium' 
                    : 'bg-muted text-muted-foreground'
                  }
                  ${isCurrent ? 'scale-110 shadow-strong' : ''}
                `}
              >
                {isActive && index < currentStep ? (
                  <CheckCircle className="w-6 h-6" />
                ) : (
                  <Icon className="w-6 h-6" />
                )}
              </div>
              
              <div className="text-center">
                <p className={`text-sm font-medium ${isActive ? 'text-foreground' : 'text-muted-foreground'}`}>
                  {step.label}
                </p>
                <p className="text-xs text-muted-foreground hidden sm:block">
                  {step.description}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};