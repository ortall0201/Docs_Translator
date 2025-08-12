import { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { LanguageSelector } from '@/components/LanguageSelector';
import { TranslationProgress } from '@/components/TranslationProgress';
import { StepIndicator } from '@/components/StepIndicator';
import { TranslateButton } from '@/components/TranslateButton';
import { PDFPreview } from '@/components/PDFPreview';
import heroImage from '@/assets/hero-illustration.jpg';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { X, Check, Crown, Zap } from 'lucide-react';
import { API_BASE_URL } from '@/config/api';

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState('pl');
  const [isTranslating, setIsTranslating] = useState(false);
  const [translatedFile, setTranslatedFile] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const { toast } = useToast();

  const getCurrentStep = () => {
    if (translatedFile) return 3;
    if (isTranslating) return 2;
    if (selectedFile && selectedLanguage) return 1;
    if (selectedFile) return 1;
    return 0;
  };

  const handleFileSelect = (file: File | null) => {
    setSelectedFile(file);
    setTranslatedFile(null);
    if (file) {
      setCurrentStep(1);
    } else {
      setCurrentStep(0);
    }
  };

  const handleLanguageChange = (language: string) => {
    setSelectedLanguage(language);
  };

  const handleTranslate = async () => {
    if (!selectedFile || !selectedLanguage) return;
    
    console.log('[DEBUG] DEBUG: Starting translation process');
    console.log('[DEBUG] DEBUG: Selected file:', selectedFile.name, 'Size:', selectedFile.size, 'Type:', selectedFile.type);
    console.log('[DEBUG] DEBUG: Target language:', selectedLanguage);
    
    setIsTranslating(true);
    setCurrentStep(2);
    
    try {
      // Step 1: Upload the file to FastAPI
      const uploadFormData = new FormData();
      uploadFormData.append('file', selectedFile);
      
      console.log('[DEBUG] DEBUG: Uploading file to backend...');
      const uploadResponse = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: uploadFormData,
      });
      
      console.log('[DEBUG] DEBUG: Upload response status:', uploadResponse.status);
      console.log('[DEBUG] DEBUG: Upload response headers:', Object.fromEntries(uploadResponse.headers.entries()));
      
      if (!uploadResponse.ok) {
        const errorText = await uploadResponse.text();
        console.error('[ERROR] DEBUG: Upload failed with response:', errorText);
        throw new Error('Upload failed');
      }
      
      const uploadResult = await uploadResponse.json();
      const filename = uploadResult.filename;
      console.log('[DEBUG] DEBUG: File uploaded successfully, filename:', filename);
      
      // Step 2: Translate the uploaded file
      const translateFormData = new FormData();
      translateFormData.append('filename', filename);
      translateFormData.append('lang', selectedLanguage);
      
      console.log('[DEBUG] DEBUG: Starting translation request...');
      const translateResponse = await fetch(`${API_BASE_URL}/translate`, {
        method: 'POST',
        body: translateFormData,
        // Increase timeout for large documents (5 minutes)
        signal: AbortSignal.timeout(300000),
      });
      
      console.log('[DEBUG] DEBUG: Translation response status:', translateResponse.status);
      console.log('[DEBUG] DEBUG: Translation response headers:', Object.fromEntries(translateResponse.headers.entries()));
      
      if (!translateResponse.ok) {
        const errorText = await translateResponse.text();
        console.error('[ERROR] DEBUG: Translation failed with response:', errorText);
        throw new Error('Translation failed');
      }
      
      const translateResult = await translateResponse.json();
      console.log('[DEBUG] DEBUG: Translation completed, result:', translateResult);
      console.log('[DEBUG] DEBUG: Extracted translated_file:', translateResult.translated_file);
      setTranslatedFile(translateResult.translated_file);
      console.log('[DEBUG] DEBUG: Set translatedFile state to:', translateResult.translated_file);
      setCurrentStep(3);
      
      // Immediately test if the translated file is accessible
      const testFileUrl = `${API_BASE_URL}/preview/${translateResult.translated_file}`;
      console.log('[DEBUG] DEBUG: Testing translated file accessibility at:', testFileUrl);
      
      fetch(testFileUrl, { method: 'HEAD' })
      .then(response => {
        console.log('[DEBUG] DEBUG: Translated file test - Status:', response.status);
        console.log('[DEBUG] DEBUG: Translated file test - Content-Type:', response.headers.get('content-type'));
        console.log('[DEBUG] DEBUG: Translated file test - Content-Length:', response.headers.get('content-length'));
      })
      .catch(error => {
        console.error('[ERROR] DEBUG: Translated file test failed:', error);
      });
      
      toast({
        title: "Translation completed!",
        description: "Your document has been successfully translated.",
      });
    } catch (error) {
      console.error('[ERROR] DEBUG: Translation process failed:', error);
      console.error('[ERROR] DEBUG: Error details:', {
        message: error.message,
        stack: error.stack,
        name: error.name
      });
      toast({
        title: "Translation failed",
        description: "There was an error translating your document. Please try again.",
        variant: "destructive",
      });
    } finally {
      console.log('[DEBUG] DEBUG: Translation process finished, isTranslating set to false');
      setIsTranslating(false);
    }
  };

  const handleDownload = () => {
    if (translatedFile) {
      console.log('[DEBUG] DEBUG: Starting download for file:', translatedFile);
      
      // Check if this is a Hebrew/RTL language that has HTML preview with working print-to-PDF
      const hasHtmlPreview = ['_he_', '_ar_', '_ru_', '_uk_'].some(lang => translatedFile.includes(lang));
      
      if (hasHtmlPreview) {
        console.log('[DEBUG] DEBUG: RTL language detected, opening HTML preview with print functionality');
        const previewUrl = `${API_BASE_URL}/preview/${translatedFile}`;
        console.log('[DEBUG] DEBUG: Opening HTML preview URL:', previewUrl);
        
        // Open HTML preview in new tab (it has the working print-to-PDF button)
        window.open(previewUrl, '_blank');
        
        toast({
          title: "Preview opened",
          description: "Use the 'Print/Save as PDF' button in the preview to download your document.",
          duration: 5000,
        });
        
        return;
      }
      
      // For regular languages, use direct download
      console.log('[DEBUG] DEBUG: Regular language, using direct download');
      const downloadUrl = `${API_BASE_URL}/download/${translatedFile}`;
      console.log('[DEBUG] DEBUG: Download URL:', downloadUrl);
      
      // Test the download URL before creating the link
      fetch(downloadUrl, { method: 'HEAD' })
      .then(response => {
        console.log('[DEBUG] DEBUG: Download URL test - Status:', response.status);
        console.log('[DEBUG] DEBUG: Download URL test - Content-Type:', response.headers.get('content-type'));
        console.log('[DEBUG] DEBUG: Download URL test - Content-Length:', response.headers.get('content-length'));
        
        if (response.ok) {
          console.log('[DEBUG] DEBUG: Creating download link...');
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.download = translatedFile;
          link.target = '_blank';
          document.body.appendChild(link);
          
          console.log('[DEBUG] DEBUG: Triggering download click...');
          link.click();
          document.body.removeChild(link);
          console.log('[DEBUG] DEBUG: Download link removed from DOM');
          
          toast({
            title: "Download started",
            description: "Your translated document is being downloaded.",
          });
        } else {
          console.error('[ERROR] DEBUG: Download URL test failed, status:', response.status);
          toast({
            title: "Download failed",
            description: "The translated file is not accessible for download.",
            variant: "destructive",
          });
        }
      })
      .catch(error => {
        console.error('[ERROR] DEBUG: Download URL test error:', error);
        toast({
          title: "Download failed",
          description: "Unable to access the translated file.",
          variant: "destructive",
        });
      });
    } else {
      console.warn('[WARN] DEBUG: Download attempted but no translated file available');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-secondary">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center">
              <span className="text-2xl">📄</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Docs Translator</h1>
              <p className="text-sm text-muted-foreground">Professional document translation made simple</p>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-16 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="space-y-4">
                <h2 className="text-4xl lg:text-5xl font-bold text-foreground leading-tight">
                  Translate Documents
                  <span className="block text-transparent bg-gradient-primary bg-clip-text">
                    Instantly & Accurately
                  </span>
                </h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  Upload your PDF documents and get professional translations in multiple languages. 
                  Powered by advanced AI technology while preserving your document's original formatting.
                </p>
              </div>
              
              <div className="flex flex-wrap gap-4 text-sm">
                <div className="flex items-center space-x-2 bg-card/50 backdrop-blur-sm px-3 py-2 rounded-lg border border-border/50">
                  <div className="w-2 h-2 bg-success rounded-full"></div>
                  <span className="text-foreground">Secure & Private</span>
                </div>
                <div className="flex items-center space-x-2 bg-card/50 backdrop-blur-sm px-3 py-2 rounded-lg border border-border/50">
                  <div className="w-2 h-2 bg-tech-blue rounded-full"></div>
                  <span className="text-foreground">Format Preserved</span>
                </div>
                <div className="flex items-center space-x-2 bg-card/50 backdrop-blur-sm px-3 py-2 rounded-lg border border-border/50">
                  <div className="w-2 h-2 bg-warning rounded-full"></div>
                  <span className="text-foreground">Lightning Fast</span>
                </div>
              </div>
            </div>
            
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-primary opacity-20 rounded-2xl blur-3xl"></div>
              <img 
                src={heroImage} 
                alt="Document translation illustration" 
                className="relative w-full h-auto rounded-2xl shadow-strong floating-animation"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-12">
        <StepIndicator currentStep={getCurrentStep()} />
        
        <div className="space-y-8">
          {/* Step 1: File Upload */}
          <FileUpload 
            onFileSelect={handleFileSelect}
            selectedFile={selectedFile}
            isProcessing={isTranslating}
          />
          
          {/* Step 2: Language Selection */}
          {selectedFile && (
            <LanguageSelector
              selectedLanguage={selectedLanguage}
              onLanguageChange={handleLanguageChange}
              disabled={isTranslating}
            />
          )}
          
          {/* Step 3: Translate Button */}
          {selectedFile && selectedLanguage && (
            <TranslateButton
              onTranslate={handleTranslate}
              disabled={!selectedFile || !selectedLanguage}
              isTranslating={isTranslating}
            />
          )}
          
          {/* Step 4: Translation Progress & Download */}
          <TranslationProgress
            isTranslating={isTranslating}
            translatedFile={translatedFile}
            onDownload={handleDownload}
            fileName={selectedFile?.name || ''}
          />

          {/* Step 5: PDF Preview */}
          {translatedFile && (
            <div className="mt-8">
              <PDFPreview 
                fileUrl={`${API_BASE_URL}/preview/${translatedFile}`}
                title="📄 Translated Document Preview"
              />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/30 backdrop-blur-sm mt-20">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="grid md:grid-cols-3 gap-8 text-sm">
            {/* About */}
            <div>
              <h3 className="font-semibold text-foreground mb-3">About Docs Translator</h3>
              <p className="text-muted-foreground leading-relaxed">
                Professional document translation powered by advanced AI. 
                Preserving formatting while delivering accurate translations.
              </p>
            </div>
            
            {/* Contact */}
            <div>
              <h3 className="font-semibold text-foreground mb-3">Contact</h3>
              <div className="space-y-2 text-muted-foreground">
                <p className="flex items-start">
                  <span className="mr-2 mt-0.5">👤</span>
                  <div>
                    <div className="font-medium text-foreground">Ortal Lasry</div>
                    <div className="text-sm">Founder & AI Engineer</div>
                  </div>
                </p>
                <p className="flex items-center">
                  <span className="mr-2">📧</span>
                  <a href="mailto:ortalgr@gmail.com" className="hover:text-primary transition-colors">
                    ortalgr@gmail.com
                  </a>
                </p>
                <p className="flex items-center">
                  <span className="mr-2">🌐</span>
                  <span>Professional AI Translation Services</span>
                </p>
              </div>
            </div>
            
            {/* Premium */}
            <div>
              <h3 className="font-semibold text-foreground mb-3">Premium Features</h3>
              <p className="text-muted-foreground mb-3">
                Unlock advanced features with our premium plans
              </p>
              <button 
                onClick={() => setShowPaymentModal(true)}
                className="bg-gradient-primary text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity text-sm font-medium"
              >
                View Plans
              </button>
            </div>
          </div>
          
          <div className="mt-8 pt-4 border-t border-border/50 text-center text-muted-foreground">
            <p>&copy; 2024 Docs Translator. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Payment Modal */}
      {showPaymentModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-4xl bg-card border-border/50 max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              {/* Modal Header */}
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-foreground mb-2">Choose Your Plan</h2>
                  <p className="text-muted-foreground">Unlock premium features for professional document translation</p>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setShowPaymentModal(false)}
                  className="h-8 w-8 p-0"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>

              {/* Pricing Cards */}
              <div className="grid md:grid-cols-3 gap-6 mb-8">
                {/* Free Plan */}
                <div className="border border-border/50 rounded-lg p-6 bg-card/50">
                  <div className="text-center mb-6">
                    <h3 className="text-lg font-semibold mb-2">Free</h3>
                    <div className="text-3xl font-bold mb-2">$0</div>
                    <p className="text-muted-foreground text-sm">Perfect for testing</p>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>5 documents per month</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>Basic language support</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>Standard PDF quality</span>
                    </li>
                  </ul>
                  <Button className="w-full" variant="outline" disabled>
                    Current Plan
                  </Button>
                </div>

                {/* Pro Plan */}
                <div className="border-2 border-primary rounded-lg p-6 bg-card/50 relative">
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <span className="bg-primary text-primary-foreground px-3 py-1 rounded-full text-xs font-medium">
                      Most Popular
                    </span>
                  </div>
                  <div className="text-center mb-6">
                    <h3 className="text-lg font-semibold mb-2 flex items-center justify-center">
                      <Zap className="h-5 w-5 text-primary mr-2" />
                      Pro
                    </h3>
                    <div className="text-3xl font-bold mb-2">$9.99</div>
                    <p className="text-muted-foreground text-sm">per month</p>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>100 documents per month</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>All languages supported</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>High-quality PDF output</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>Priority support</span>
                    </li>
                  </ul>
                  <Button 
                    className="w-full bg-gradient-primary hover:opacity-90"
                    onClick={() => {
                      toast({
                        title: "Coming Soon!",
                        description: "Payment system will be available soon. Contact Ortal Lasry at ortalgr@gmail.com for early access.",
                        duration: 5000,
                      });
                    }}
                  >
                    Coming Soon
                  </Button>
                </div>

                {/* Enterprise Plan */}
                <div className="border border-border/50 rounded-lg p-6 bg-card/50">
                  <div className="text-center mb-6">
                    <h3 className="text-lg font-semibold mb-2 flex items-center justify-center">
                      <Crown className="h-5 w-5 text-yellow-500 mr-2" />
                      Enterprise
                    </h3>
                    <div className="text-3xl font-bold mb-2">$29.99</div>
                    <p className="text-muted-foreground text-sm">per month</p>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>Unlimited documents</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>All languages + dialects</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>Premium PDF quality</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>24/7 priority support</span>
                    </li>
                    <li className="flex items-center text-sm">
                      <Check className="h-4 w-4 text-green-500 mr-2" />
                      <span>Custom integrations</span>
                    </li>
                  </ul>
                  <Button 
                    className="w-full"
                    variant="outline"
                    onClick={() => {
                      toast({
                        title: "Coming Soon!",
                        description: "Enterprise features will be available soon. Contact ortalgr@gmail.com for more information.",
                        duration: 5000,
                      });
                    }}
                  >
                    Coming Soon
                  </Button>
                </div>
              </div>

              {/* Contact Info */}
              <div className="bg-muted/30 rounded-lg p-4 text-center">
                <p className="text-sm text-muted-foreground mb-2">
                  Questions about our plans?
                </p>
                <p className="text-sm mb-1">
                  <span className="font-medium text-foreground">Ortal Lasry</span>
                  <span className="text-muted-foreground"> • Founder & AI Engineer</span>
                </p>
                <p className="text-sm">
                  <a 
                    href="mailto:ortalgr@gmail.com" 
                    className="text-primary hover:underline font-medium"
                  >
                    ortalgr@gmail.com
                  </a>
                </p>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

export default Index;
