import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.js',
  import.meta.url,
).toString();

interface PDFPreviewProps {
  fileUrl: string;
  title?: string;
}

export const PDFPreview: React.FC<PDFPreviewProps> = ({ fileUrl, title = "PDF Preview" }) => {
  console.log('[DEBUG] DEBUG: PDFPreview component initialized');
  console.log('[DEBUG] DEBUG: File URL:', fileUrl);
  console.log('[DEBUG] DEBUG: Title:', title);

  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [scale, setScale] = useState<number>(1.0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const [isHtmlContent, setIsHtmlContent] = useState<boolean>(false);
  const [htmlContent, setHtmlContent] = useState<string>('');

  // Check if this is an RTL language that serves HTML instead of PDF
  const isRTLFile = ['_he_', '_ar_', '_ru_', '_uk_'].some(lang => fileUrl.includes(lang));

  // Add debug logging for component state changes
  React.useEffect(() => {
    console.log('[DEBUG] DEBUG: Component state changed - loading:', loading, 'error:', error, 'numPages:', numPages, 'currentPage:', pageNumber, 'isHtmlContent:', isHtmlContent);
  }, [loading, error, numPages, pageNumber, isHtmlContent]);

  // Add effect to track file URL changes and load content appropriately
  React.useEffect(() => {
    console.log('[DEBUG] DEBUG: File URL changed to:', fileUrl);
    console.log('[DEBUG] DEBUG: Is RTL file:', isRTLFile);
    console.log('[DEBUG] DEBUG: Resetting viewer state');
    
    setLoading(true);
    setError('');
    setNumPages(0);
    setPageNumber(1);
    setIsHtmlContent(false);
    setHtmlContent('');
    
    if (fileUrl) {
      console.log('[DEBUG] DEBUG: Testing content type...');
      
      // First, check what content type we get
      fetch(fileUrl, { method: 'HEAD' })
      .then(response => {
        console.log('[DEBUG] DEBUG: HEAD response status:', response.status);
        console.log('[DEBUG] DEBUG: Content-Type:', response.headers.get('content-type'));
        
        const contentType = response.headers.get('content-type');
        
        if (contentType?.includes('text/html') || isRTLFile) {
          // This is HTML content (RTL languages serve HTML instead of PDF)
          console.log('[DEBUG] DEBUG: Detected HTML content, loading as HTML preview');
          setIsHtmlContent(true);
          
          // Load HTML content for preview
          fetch(fileUrl)
          .then(response => response.text())
          .then(html => {
            console.log('[DEBUG] DEBUG: HTML content loaded, length:', html.length);
            // Clean up HTML for preview (remove scripts and button)
            const cleanedHtml = html
              .replace(/<script[\s\S]*?<\/script>/gi, '') // Remove scripts
              .replace(/<button[\s\S]*?<\/button>/gi, '') // Remove buttons
              .replace(/onclick="[^"]*"/gi, ''); // Remove onclick handlers
            
            setHtmlContent(cleanedHtml);
            setLoading(false);
          })
          .catch(error => {
            console.error('[ERROR] DEBUG: Failed to load HTML content:', error);
            setError('Failed to load preview content');
            setLoading(false);
          });
        } else {
          // This should be PDF content
          console.log('[DEBUG] DEBUG: Treating as PDF content');
          setIsHtmlContent(false);
          setLoading(false); // Let the PDF component handle its own loading
        }
      })
      .catch(error => {
        console.error('[ERROR] DEBUG: Failed to check content type:', error);
        // Assume it's PDF and let the PDF component handle it
        setIsHtmlContent(false);
        setLoading(false);
      });
    }
  }, [fileUrl, isRTLFile]);

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    console.log('[DEBUG] DEBUG: PDF loaded successfully!');
    console.log('[DEBUG] DEBUG: Number of pages:', numPages);
    setNumPages(numPages);
    setLoading(false);
    setError('');
  };

  const onDocumentLoadError = (error: any) => {
    console.error('[ERROR] DEBUG: PDF loading failed!');
    console.error('[ERROR] DEBUG: Error details:', error);
    console.error('[ERROR] DEBUG: Error message:', error.message);
    console.error('[ERROR] DEBUG: Error type:', typeof error);
    console.error('[ERROR] DEBUG: Error stack:', error.stack);
    
    // Try to get more detailed error info
    if (error.name) console.error('[ERROR] DEBUG: Error name:', error.name);
    if (error.code) console.error('[ERROR] DEBUG: Error code:', error.code);
    
    setLoading(false);
    setError(`Failed to load PDF: ${error.message || error.toString() || 'Unknown error'}`);
  };

  const goToPrevPage = () => {
    setPageNumber(Math.max(1, pageNumber - 1));
  };

  const goToNextPage = () => {
    setPageNumber(Math.min(numPages, pageNumber + 1));
  };

  const zoomIn = () => {
    setScale(Math.min(2.0, scale + 0.2));
  };

  const zoomOut = () => {
    setScale(Math.max(0.5, scale - 0.2));
  };

  return (
    <Card className="w-full max-w-4xl mx-auto bg-card/50 backdrop-blur-sm border-border/50">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
          
          {/* Controls */}
          <div className="flex items-center space-x-2">
            {/* Zoom Controls */}
            <div className="flex items-center space-x-1 bg-muted/50 rounded-lg p-1">
              <Button
                variant="ghost"
                size="sm"
                onClick={zoomOut}
                disabled={scale <= 0.5}
                className="h-8 w-8 p-0"
              >
                <ZoomOut className="h-4 w-4" />
              </Button>
              <span className="text-sm text-muted-foreground min-w-[3rem] text-center">
                {Math.round(scale * 100)}%
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={zoomIn}
                disabled={scale >= 2.0}
                className="h-8 w-8 p-0"
              >
                <ZoomIn className="h-4 w-4" />
              </Button>
            </div>

            {/* Page Navigation */}
            {numPages > 1 && (
              <div className="flex items-center space-x-1 bg-muted/50 rounded-lg p-1">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={goToPrevPage}
                  disabled={pageNumber <= 1}
                  className="h-8 w-8 p-0"
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <span className="text-sm text-muted-foreground min-w-[4rem] text-center">
                  {pageNumber} / {numPages}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={goToNextPage}
                  disabled={pageNumber >= numPages}
                  className="h-8 w-8 p-0"
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Content Viewer */}
        <div className="border border-border/50 rounded-lg overflow-hidden bg-white">
          <div className="flex justify-center p-4 min-h-[600px]">
            {loading && !error && (
              <div className="flex items-center justify-center h-96">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            )}
            
            {error && (
              <div className="flex items-center justify-center h-96">
                <div className="text-center">
                  <div className="text-red-500 text-lg font-semibold mb-2">
                    ⚠️ Preview Loading Failed
                  </div>
                  <div className="text-red-400 text-sm mb-2">
                    {error}
                  </div>
                  <div className="text-muted-foreground text-xs">
                    Try using the download/print button to access the full document.
                  </div>
                </div>
              </div>
            )}
            
            {/* HTML Content Preview */}
            {!error && isHtmlContent && htmlContent && (
              <div className="w-full max-w-3xl">
                <div className="bg-gray-50 p-4 rounded-lg border-2 border-dashed border-gray-300 mb-4">
                  <div className="text-sm text-gray-600 mb-2 flex items-center">
                    <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    Document Preview - Click "Open Print/PDF Preview" for full functionality
                  </div>
                </div>
                <div 
                  className="w-full border border-gray-200 rounded-lg shadow-lg overflow-hidden"
                  style={{ 
                    height: '500px', 
                    transform: 'scale(0.8)', 
                    transformOrigin: 'top left',
                    width: '125%' // Compensate for scale
                  }}
                >
                  <iframe
                    srcDoc={htmlContent}
                    className="w-full h-full border-0"
                    title="Document Preview"
                    sandbox="allow-same-origin"
                    style={{ 
                      pointerEvents: 'none', // Make it non-interactive  
                      backgroundColor: 'white'
                    }}
                  />
                </div>
                <div className="text-center mt-4 text-sm text-gray-500">
                  This is a preview thumbnail. Click "Open Print/PDF Preview" above for the interactive version.
                </div>
              </div>
            )}
            
            {/* PDF Content */}
            {!error && !isHtmlContent && (
              <Document
                file={fileUrl}
                onLoadSuccess={onDocumentLoadSuccess}
                onLoadError={onDocumentLoadError}
                loading=""
                onLoadProgress={({ loaded, total }) => {
                  console.log('[DEBUG] DEBUG: PDF loading progress:', `${loaded}/${total} bytes (${Math.round((loaded/total)*100)}%)`);
                }}
                onSourceSuccess={() => {
                  console.log('[DEBUG] DEBUG: PDF source loaded successfully');
                }}
                onSourceError={(error) => {
                  console.error('[ERROR] DEBUG: PDF source error:', error);
                }}
              >
                <Page 
                  pageNumber={pageNumber} 
                  scale={scale}
                  renderTextLayer={false}
                  renderAnnotationLayer={false}
                  onLoadSuccess={(page) => {
                    console.log('[DEBUG] DEBUG: Page rendered successfully');
                    console.log('[DEBUG] DEBUG: Page number:', pageNumber);
                    console.log('[DEBUG] DEBUG: Page scale:', scale);
                    console.log('[DEBUG] DEBUG: Page dimensions:', page.width + 'x' + page.height);
                  }}
                  onLoadError={(error) => {
                    console.error('[ERROR] DEBUG: Page rendering failed:', error);
                    console.error('[ERROR] DEBUG: Failed page number:', pageNumber);
                  }}
                  onRenderSuccess={() => {
                    console.log('[DEBUG] DEBUG: Page render completed successfully');
                  }}
                  onRenderError={(error) => {
                    console.error('[ERROR] DEBUG: Page render error:', error);
                  }}
                />
              </Document>
            )}
          </div>
        </div>

        {/* Footer Status */}
        {isHtmlContent && htmlContent && (
          <div className="mt-4 text-sm text-muted-foreground text-center">
            ✅ HTML document preview loaded • Click button above for full interactive version
          </div>
        )}
        
        {numPages > 0 && !isHtmlContent && (
          <div className="mt-4 text-sm text-muted-foreground text-center">
            Document loaded successfully • {numPages} page{numPages > 1 ? 's' : ''}
          </div>
        )}
      </div>
    </Card>
  );
};