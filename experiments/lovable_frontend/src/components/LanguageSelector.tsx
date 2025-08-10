import { Languages } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface LanguageSelectorProps {
  selectedLanguage: string;
  onLanguageChange: (language: string) => void;
  disabled?: boolean;
}

const languages = [
  { code: 'pl', name: 'Polish', flag: '🇵🇱' },
  { code: 'he', name: 'Hebrew', flag: '🇮🇱' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'uk', name: 'Ukrainian', flag: '🇺🇦' },
  { code: 'ru', name: 'Russian', flag: '🇷🇺' },
];

export const LanguageSelector = ({ selectedLanguage, onLanguageChange, disabled }: LanguageSelectorProps) => {
  return (
    <div className="step-card fade-in">
      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-tech-blue/10 rounded-lg flex items-center justify-center">
            <Languages className="w-6 h-6 text-tech-blue" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-foreground">
              Select Target Language
            </h3>
            <p className="text-sm text-muted-foreground">
              Choose the language to translate your document to
            </p>
          </div>
        </div>

        <Select value={selectedLanguage} onValueChange={onLanguageChange} disabled={disabled}>
          <SelectTrigger className="w-full h-12 bg-background border-border hover:border-primary/50 transition-colors">
            <SelectValue placeholder="Select target language" />
          </SelectTrigger>
          <SelectContent>
            {languages.map((language) => (
              <SelectItem key={language.code} value={language.code}>
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{language.flag}</span>
                  <span>{language.name}</span>
                </div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
};