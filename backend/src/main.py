# src/main.py - FastAPI backend for doc translator with CrewAI integration

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import fitz  # PyMuPDF
import openai
import os
from dotenv import load_dotenv

# GCP Translator disabled for production deployment
GCP_AVAILABLE = False
print("[DEBUG] DEBUG: GCP Translator disabled for production")

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize app
app = FastAPI()

# Health check route
@app.get("/")
async def root():
    return {"message": "Docs Translator backend is running!"}

# Allow frontend - specific origins to avoid runmydocker CORS conflicts
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://translate-doc.runmydocker-app.com",
        "https://transladoc.runmydocker-app.com",
        "https://docs-translator-frontend.runmydocker-app.com",
        "https://docs-translator-frontend-v3.runmydocker-app.com",
        "http://localhost:3000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "File uploaded successfully", "filename": file.filename}

def sanitize_filename(filename):
    """Remove or replace problematic characters in filenames"""
    import re
    import unicodedata
    
    # Normalize unicode characters first
    filename = unicodedata.normalize('NFKD', filename)
    
    # Replace any non-ASCII, non-alphanumeric characters (except . and _)
    filename = re.sub(r'[^\w\._-]', '_', filename, flags=re.UNICODE)
    
    # Replace multiple underscores/spaces with single underscore
    filename = re.sub(r'[_\s]+', '_', filename)
    
    # Clean up edges
    filename = filename.strip('_')
    
    return filename

async def create_html_translation(translated_text: str, lang: str, output_path: Path, original_text: str = "") -> dict:
    """Create HTML file for languages with font display issues"""
    try:
        print(f"[DEBUG] DEBUG: Creating HTML translation for language: {lang}")
        
        # Language direction and fonts
        direction = "rtl" if lang in ['he', 'ar'] else "ltr"
        font_family = {
            'he': "Arial, 'Times New Roman', serif",
            'ar': "Arial, 'Times New Roman', serif", 
            'ru': "Arial, 'Times New Roman', serif",
            'uk': "Arial, 'Times New Roman', serif"
        }.get(lang, "Arial, sans-serif")
        
        # Process text to preserve structure
        paragraphs = translated_text.split('\n\n')
        if len(paragraphs) < 2:
            # Try splitting by single line breaks if no double breaks
            paragraphs = translated_text.split('\n')
        
        print(f"[DEBUG] DEBUG: Split text into {len(paragraphs)} paragraphs")
        
        # HTML template with proper Hebrew support
        html_content = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Translated Document ({lang.upper()})</title>
    <style>
        body {{
            font-family: {font_family};
            font-size: 16px;
            line-height: 1.6;
            margin: 40px;
            background-color: #ffffff;
            color: #333333;
            direction: {direction};
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #007acc;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #007acc;
            margin-bottom: 10px;
        }}
        .content {{
            padding: 30px;
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: 0 auto;
        }}
        .paragraph {{
            margin-bottom: 15px;
            line-height: 1.8;
            text-align: justify;
        }}
        .paragraph:last-child {{
            margin-bottom: 0;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 12px;
            color: #666666;
            border-top: 1px solid #e0e0e0;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">📄 Translated Document ({lang.upper()})</div>
        <div>Professional AI Translation</div>
    </div>
    
    <div class="content">"""
        
        # Add paragraphs with proper structure
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():  # Only add non-empty paragraphs
                html_content += f'        <div class="paragraph">{paragraph.strip()}</div>\n'
        
        html_content += """    </div>
    
    <!-- Download PDF Button -->
    <div style="text-align: center; margin: 30px 0; padding: 20px; border-top: 2px solid #e0e0e0;">
        <button onclick="downloadAsPDF()" style="
            background: linear-gradient(135deg, #007acc, #0056b3);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.3)';" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)';">
            🖨️ Print/Save as PDF
        </button>
        <p style="margin-top: 15px; font-size: 12px; color: #666;">
            Opens print dialog - select "Save as PDF" to download this document
        </p>
    </div>
    
    <div class="footer">
        Generated by Docs Translator • Powered by OpenAI
    </div>
    
    <script>
        function downloadAsPDF() {
            // Show loading indicator
            const button = document.querySelector('button');
            const originalText = button.innerHTML;
            button.innerHTML = '⏳ Preparing PDF...';
            button.disabled = true;
            
            try {
                // Use browser's print functionality to generate PDF
                // Create a clean version for PDF generation
                const printContent = document.cloneNode(true);
                
                // Remove the button from the print version
                const printButton = printContent.querySelector('button');
                if (printButton) {
                    printButton.remove();
                }
                
                // Create temporary window for printing
                const printWindow = window.open('', '_blank');
                printWindow.document.write(printContent.documentElement.outerHTML);
                printWindow.document.close();
                
                // Add print styles to ensure proper formatting
                const printStyle = printWindow.document.createElement('style');
                printStyle.textContent = `
                    @media print {
                        body { margin: 0.5in; }
                        .footer { page-break-inside: avoid; }
                        button { display: none !important; }
                    }
                    @page {
                        size: A4;
                        margin: 0.5in;
                    }
                `;
                printWindow.document.head.appendChild(printStyle);
                
                // Trigger print dialog
                setTimeout(() => {
                    printWindow.print();
                    
                    // Close print window after printing
                    setTimeout(() => {
                        printWindow.close();
                    }, 500);
                }, 100);
                
            } catch (error) {
                console.error('PDF generation error:', error);
                alert('PDF generation failed. Please use your browser\\'s print function (Ctrl+P) and select "Save as PDF".');
            } finally {
                // Restore button
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.disabled = false;
                }, 1000);
            }
        }
    </script>
</body>
</html>"""

        # Change extension to .html
        html_output_path = output_path.with_suffix('.html')
        print(f"[DEBUG] DEBUG: Saving HTML to: {html_output_path}")
        
        # Write HTML file
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"[DEBUG] DEBUG: HTML file created successfully, size: {len(html_content)} characters")
        
        return {"translated_file": html_output_path.name, "html_file": html_output_path.name}
        
    except Exception as e:
        print(f"[ERROR] DEBUG: HTML creation failed: {e}")
        raise e

async def create_hebrew_pdf(translated_text: str, lang: str, output_path: Path) -> dict:
    """Create PDF with better Hebrew font support"""
    try:
        print(f"[DEBUG] DEBUG: Creating Hebrew-compatible PDF for language: {lang}")
        print(f"[DEBUG] DEBUG: Input text length: {len(translated_text)}")
        print(f"[DEBUG] DEBUG: Text preview: Hebrew text handling...")
        
        # Create new PDF
        new_doc = fitz.open()
        page = new_doc.new_page(width=595, height=842)  # A4
        
        current_y = 50
        line_height = 20
        
        # Add English title since Hebrew title might not render properly
        title = f"Translated Document ({lang.upper()})"
        try:
            page.insert_text(fitz.Point(50, current_y), title, fontsize=16, 
                           color=(0, 0, 1), fontname="helv")
            print(f"[DEBUG] DEBUG: Title added successfully")
        except Exception as title_error:
            print(f"[ERROR] DEBUG: Title insertion failed: {title_error}")
            page.insert_text(fitz.Point(50, current_y), "Translated Document", fontsize=16, color=(0, 0, 1))
        
        current_y += 40
        
        # For Hebrew text, we need to handle it differently
        # Try to convert Hebrew characters to be compatible with PDF generation
        import unicodedata
        
        # Normalize the text first
        normalized_text = unicodedata.normalize('NFKC', translated_text)
        print(f"[DEBUG] DEBUG: Normalized text length: {len(normalized_text)}")
        
        # Try to create PDF with the actual Hebrew text
        # Split into manageable chunks
        lines = []
        words = normalized_text.split()
        current_line = ""
        max_chars = 50  # Conservative limit for Hebrew
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) < max_chars:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        print(f"[DEBUG] DEBUG: Split Hebrew text into {len(lines)} lines for PDF")
        
        # Insert text lines with better error handling
        lines_inserted = 0
        for line_num, line in enumerate(lines):
            if current_y > 780:  # Prevent overflow
                break
                
            try:
                # Method 1: Try with built-in font
                try:
                    result = page.insert_text(fitz.Point(50, current_y), line, 
                                           fontsize=12, fontname="helv")
                    if result > 0:  # Check if text was actually inserted
                        lines_inserted += 1
                        print(f"[DEBUG] DEBUG: Line {line_num + 1} inserted successfully with helv font")
                    else:
                        raise Exception("No text inserted")
                except:
                    # Method 2: Try with default font
                    try:
                        result = page.insert_text(fitz.Point(50, current_y), line, fontsize=12)
                        if result > 0:
                            lines_inserted += 1
                            print(f"[DEBUG] DEBUG: Line {line_num + 1} inserted with default font")
                        else:
                            # Method 3: Insert fallback text indicating Hebrew content
                            fallback_text = f"[Hebrew Text - Line {line_num + 1}]"
                            page.insert_text(fitz.Point(50, current_y), fallback_text, fontsize=12)
                            lines_inserted += 1
                            print(f"[DEBUG] DEBUG: Line {line_num + 1} inserted as fallback")
                    except Exception as e2:
                        print(f"[ERROR] DEBUG: All insertion methods failed for line {line_num + 1}: {e2}")
                        # Insert error indicator
                        error_text = f"[Translation Error - Line {line_num + 1}]"
                        try:
                            page.insert_text(fitz.Point(50, current_y), error_text, fontsize=12)
                            lines_inserted += 1
                        except:
                            print(f"[ERROR] DEBUG: Even error text insertion failed for line {line_num + 1}")
                
                current_y += line_height
                
            except Exception as line_error:
                print(f"[ERROR] DEBUG: Complete line processing failed for line {line_num + 1}: {line_error}")
                current_y += line_height
        
        print(f"[DEBUG] DEBUG: Total lines inserted: {lines_inserted}")
        
        # Add a note about Hebrew text limitations
        note_y = current_y + 30
        note_text = "Note: For best Hebrew text display, please use the preview function."
        try:
            page.insert_text(fitz.Point(50, note_y), note_text, fontsize=10, color=(0.5, 0.5, 0.5))
            print(f"[DEBUG] DEBUG: Hebrew note added successfully")
        except:
            print(f"[DEBUG] DEBUG: Could not add Hebrew note")
        
        # Save PDF with compression
        pdf_output_path = output_path.with_suffix('.pdf')
        print(f"[DEBUG] DEBUG: Saving PDF to: {pdf_output_path}")
        
        try:
            new_doc.save(pdf_output_path, garbage=4, deflate=True, clean=True)
            new_doc.close()
            
            # Verify the file was created and check size
            import os
            if pdf_output_path.exists():
                file_size = os.path.getsize(pdf_output_path)
                print(f"[DEBUG] DEBUG: Hebrew PDF saved successfully, size: {file_size} bytes")
                
                # Quick validation
                test_doc = fitz.open(pdf_output_path)
                pages = len(test_doc)
                test_doc.close()
                print(f"[DEBUG] DEBUG: PDF validation: {pages} pages")
                
                return {"translated_file": pdf_output_path.name, "pdf_file": pdf_output_path.name}
            else:
                raise Exception("PDF file was not created")
                
        except Exception as save_error:
            print(f"[ERROR] DEBUG: PDF save failed: {save_error}")
            if 'new_doc' in locals():
                new_doc.close()
            raise save_error
        
    except Exception as e:
        print(f"[ERROR] DEBUG: Hebrew PDF creation completely failed: {e}")
        import traceback
        traceback.print_exc()
        raise e

async def create_readable_hebrew_pdf(translated_text: str, lang: str, output_path: Path) -> dict:
    """Create PDF with English description of Hebrew content since Hebrew fonts aren't working"""
    try:
        print(f"[DEBUG] DEBUG: Creating readable Hebrew PDF with English explanation")
        
        # Get English description from OpenAI
        from openai import OpenAI
        client = OpenAI()
        
        print(f"[DEBUG] DEBUG: Requesting English description of Hebrew content...")
        
        description_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a document description expert. Provide a clear English description of Hebrew text content, explaining what the Hebrew text says and means. Make it professional and informative."},
                {"role": "user", "content": f"Please provide a clear English description of what this Hebrew text contains: {translated_text}"}
            ],
            temperature=0
        )
        
        english_description = description_response.choices[0].message.content
        print(f"[DEBUG] DEBUG: English description length: {len(english_description)}")
        
        # Create new PDF
        new_doc = fitz.open()
        page = new_doc.new_page(width=595, height=842)  # A4
        
        current_y = 50
        line_height = 16
        
        # Add title
        title = f"Hebrew Document Translation - Content Description"
        page.insert_text(fitz.Point(50, current_y), title, fontsize=16, 
                       color=(0, 0, 1), fontname="helv")
        current_y += 30
        
        # Add explanation
        explanation = "Note: Hebrew text cannot display properly in PDF format."
        page.insert_text(fitz.Point(50, current_y), explanation, fontsize=11, 
                       color=(0.7, 0, 0), fontname="helv")
        current_y += 20
        
        explanation2 = "Below is an English description of the Hebrew content:"
        page.insert_text(fitz.Point(50, current_y), explanation2, fontsize=11, 
                       color=(0.3, 0.3, 0.3), fontname="helv")
        current_y += 30
        
        # Process the English description
        words = english_description.split()
        lines = []
        current_line = ""
        max_chars = 75
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) <= max_chars:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        print(f"[DEBUG] DEBUG: Split description into {len(lines)} lines")
        
        # Insert description lines
        for line in lines:
            if current_y > 750:  # Prevent overflow
                break
                
            page.insert_text(fitz.Point(50, current_y), line, 
                           fontsize=12, fontname="helv")
            current_y += line_height
        
        # Add footer note
        current_y += 30
        footer_text1 = "For proper Hebrew text display with correct fonts and formatting,"
        page.insert_text(fitz.Point(50, current_y), footer_text1, fontsize=10, 
                       color=(0.4, 0.4, 0.4), fontname="helv")
        current_y += 15
        
        footer_text2 = "please use the 'View Translated File' button in the web interface."
        page.insert_text(fitz.Point(50, current_y), footer_text2, fontsize=10, 
                       color=(0.4, 0.4, 0.4), fontname="helv")
        
        # Save PDF
        pdf_output_path = output_path.with_suffix('.pdf')
        print(f"[DEBUG] DEBUG: Saving readable PDF to: {pdf_output_path}")
        
        new_doc.save(pdf_output_path, garbage=4, deflate=True, clean=True)
        new_doc.close()
        
        # Verify file creation
        import os
        if pdf_output_path.exists():
            file_size = os.path.getsize(pdf_output_path)
            print(f"[DEBUG] DEBUG: Readable Hebrew PDF saved successfully, size: {file_size} bytes")
            
            # Validate
            test_doc = fitz.open(pdf_output_path)
            pages = len(test_doc)
            test_doc.close()
            print(f"[DEBUG] DEBUG: Readable PDF validation: {pages} pages")
            
            return {"translated_file": pdf_output_path.name, "pdf_file": pdf_output_path.name}
        else:
            raise Exception("Readable PDF file was not created")
            
    except Exception as e:
        print(f"[ERROR] DEBUG: Readable Hebrew PDF creation failed: {e}")
        import traceback
        traceback.print_exc()
        raise e

# HTML-to-PDF conversion now handled by browser's print functionality

async def translate_text_with_openai(text: str, target_lang: str) -> str:
    """Translate text using OpenAI GPT directly"""
    try:
        language_map = {
            "pl": "Polish",
            "he": "Hebrew", 
            "en": "English",
            "uk": "Ukrainian",
            "ru": "Russian"
        }
        
        target_language = language_map.get(target_lang, target_lang)
        
        from openai import OpenAI
        client = OpenAI()
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a professional document translator. Translate the following text to {target_language}. Maintain the original formatting and structure. For bureaucratic or technical terms, provide clear translations but preserve important official terminology."},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Translation error: {e}")
        return f"[Translation to {target_language}]\n\n{text}\n\n[Note: This is a fallback - AI translation failed]"

@app.post("/translate")
async def translate_form(filename: str = Form(...), lang: str = Form(...)):
    print(f"[DEBUG] DEBUG: Starting translation process")
    print(f"[DEBUG] DEBUG: Input filename: {filename}")
    print(f"[DEBUG] DEBUG: Target language: {lang}")
    
    input_path = UPLOAD_DIR / filename
    print(f"[DEBUG] DEBUG: Input path: {input_path}")
    print(f"[DEBUG] DEBUG: Input file exists: {input_path.exists()}")
    
    if input_path.exists():
        import os
        file_size = os.path.getsize(input_path)
        print(f"[DEBUG] DEBUG: Input file size: {file_size} bytes")
    
    # Sanitize the output filename
    safe_filename = sanitize_filename(filename)
    print(f"[DEBUG] DEBUG: Original filename: {filename}")
    print(f"[DEBUG] DEBUG: Sanitized filename: {safe_filename}")
    
    output_path = OUTPUT_DIR / f"translated_{lang}_{safe_filename}"
    print(f"[DEBUG] DEBUG: Output path: {output_path}")

    try:
        print(f"[DEBUG] DEBUG: Starting PDF text extraction...")
        # Extract text from PDF
        doc = fitz.open(input_path)
        print(f"[DEBUG] DEBUG: PDF opened successfully, pages: {len(doc)}")
        
        content = ""
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            content += page_text
            print(f"[DEBUG] DEBUG: Page {page_num + 1} text length: {len(page_text)}")
            
        doc.close()
        print(f"[DEBUG] DEBUG: Total extracted text length: {len(content)}")
        print("[DEBUG] DEBUG: Text preview skipped due to Unicode encoding issues on Windows")
        
    except Exception as e:
        print(f"[ERROR] DEBUG: PDF parsing error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": f"PDF parsing failed: {str(e)}"})

    try:
        # Use OpenAI for translation (GCP disabled for production)
        print(f"[DEBUG] DEBUG: Starting OpenAI translation...")
        translated_text = await translate_text_with_openai(content, lang)
        print(f"[DEBUG] DEBUG: Translation completed, length: {len(translated_text) if translated_text else 'None'}")
        print("[DEBUG] DEBUG: Translation preview skipped due to Unicode encoding issues on Windows")
        
        print(f"[DEBUG] DEBUG: Starting PDF creation...")
        # Create a new PDF with the translated text using a more robust method
        new_doc = fitz.open()
        print(f"[DEBUG] DEBUG: New PDF document created")
        
        # Create a standard A4 page
        page = new_doc.new_page(width=595, height=842)  # Standard A4 in points
        print(f"[DEBUG] DEBUG: A4 page created (595x842)")
        
        # Clean the text for PDF insertion while preserving Hebrew and other languages
        import re
        print(f"[DEBUG] DEBUG: Starting text cleaning...")
        original_length = len(translated_text)
        
        # For Hebrew and other non-Latin scripts, we need to be more careful
        # Just normalize whitespace and keep all characters
        clean_text = re.sub(r'\s+', ' ', translated_text)
        clean_text = clean_text.strip()
        
        # For languages with font issues in PDF, create both HTML (for preview) and PDF (for download)
        if lang in ['he', 'ar', 'ru', 'uk']:  # Languages that have font display issues in PDF
            print(f"[DEBUG] DEBUG: Detected RTL language: {lang}, creating both HTML and PDF")
            try:
                # Create HTML for preview
                html_result = await create_html_translation(translated_text, lang, output_path, content)
                print(f"[DEBUG] DEBUG: HTML creation successful")
                
                # Create readable PDF as backup (browser handles PDF generation from HTML)
                readable_pdf_result = await create_readable_hebrew_pdf(translated_text, lang, output_path)
                print(f"[DEBUG] DEBUG: Readable PDF creation successful")
                
                # Return PDF filename for download, but HTML will be available for preview
                response_data = {"translated_file": readable_pdf_result["pdf_file"], "html_preview": html_result["html_file"]}
                print(f"[DEBUG] DEBUG: Returning JSON response: {response_data}")
                return JSONResponse(content=response_data)
                
            except Exception as hybrid_error:
                print(f"[ERROR] DEBUG: Hybrid creation failed: {hybrid_error}")
                print(f"[DEBUG] DEBUG: Falling back to standard PDF creation")
                # Continue with PDF creation as fallback
        
        print(f"[DEBUG] DEBUG: Text cleaning complete - Original: {original_length}, Clean: {len(clean_text)}")
        print("[DEBUG] DEBUG: Clean text preview skipped due to Unicode encoding issues on Windows")
        
        # Add title with better font support
        title = f"Translated Document ({lang.upper()})"
        title_point = fitz.Point(50, 50)
        print(f"[DEBUG] DEBUG: Adding title: '{title}' at point (50, 50)")
        
        try:
            # Use a font that supports Unicode better
            title_result = page.insert_text(title_point, title, fontsize=16, color=(0, 0, 1), fontname="helv")
            print(f"[DEBUG] DEBUG: Title insertion result: {title_result}")
        except Exception as title_error:
            print(f"[ERROR] DEBUG: Title insertion failed: {title_error}")
            # Try without specifying font
            try:
                title_result = page.insert_text(title_point, title, fontsize=16, color=(0, 0, 1))
                print(f"[DEBUG] DEBUG: Title insertion with default font: {title_result}")
            except:
                print(f"[ERROR] DEBUG: Title insertion completely failed")
        
        # Split text into lines that fit the page
        max_chars_per_line = 80
        lines = []
        words = clean_text.split()
        current_line = ""
        
        print(f"[DEBUG] DEBUG: Splitting text into lines (max {max_chars_per_line} chars per line)")
        print(f"[DEBUG] DEBUG: Total words to process: {len(words)}")
        
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        print(f"[DEBUG] DEBUG: Text split into {len(lines)} lines")
        
        # Insert text line by line
        y_position = 80
        lines_inserted = 0
        print(f"[DEBUG] DEBUG: Starting text insertion at y={y_position}")
        
        for line_num, line in enumerate(lines[:40]):  # Limit to 40 lines to fit on page
            if y_position > 780:  # Don't go off the page
                print(f"[DEBUG] DEBUG: Reached page bottom at y={y_position}, stopping insertion")
                break
                
            point = fitz.Point(50, y_position)
            try:
                # Try with better Unicode support - use built-in font that supports Hebrew
                result = page.insert_text(point, line, fontsize=11, color=(0, 0, 0), fontname="helv")
                lines_inserted += 1
                if line_num < 3:  # Only log first few lines to avoid spam
                    print(f"[DEBUG] DEBUG: Line {line_num + 1} inserted at y={y_position}, result: {result}")
            except Exception as line_error:
                print(f"[ERROR] DEBUG: Line {line_num + 1} insertion failed with Unicode encoding: {line_error}")
                # Fallback to default
                try:
                    result = page.insert_text(point, line, fontsize=11, color=(0, 0, 0))
                    lines_inserted += 1
                    if line_num < 3:
                        print(f"[DEBUG] DEBUG: Line {line_num + 1} inserted with fallback at y={y_position}")
                except Exception as fallback_error:
                    print(f"[ERROR] DEBUG: Line {line_num + 1} completely failed: {fallback_error}")
                    print("[ERROR] DEBUG: Failed line content preview skipped due to Unicode")
                
            y_position += 15
        
        print(f"[DEBUG] DEBUG: Text insertion complete - {lines_inserted} lines inserted")
        
        # Save the PDF with error checking
        print(f"[DEBUG] DEBUG: Starting PDF save to: {output_path}")
        try:
            save_result = new_doc.save(output_path, garbage=4, deflate=True)
            print(f"[DEBUG] DEBUG: PDF save result: {save_result}")
            new_doc.close()
            print(f"[DEBUG] DEBUG: PDF document closed")
            
            # Check file was created and get size
            if output_path.exists():
                import os
                output_size = os.path.getsize(output_path)
                print(f"[DEBUG] DEBUG: Output file created successfully, size: {output_size} bytes")
            else:
                print(f"[ERROR] DEBUG: Output file was NOT created!")
                raise Exception("PDF file was not created")
            
            # Verify the saved PDF is valid
            print(f"[DEBUG] DEBUG: Validating saved PDF...")
            test_doc = fitz.open(output_path)
            test_pages = len(test_doc)
            test_doc.close()
            print(f"[DEBUG] DEBUG: PDF validation successful - {test_pages} pages")
            
        except Exception as save_error:
            print(f"[ERROR] DEBUG: PDF save error: {save_error}")
            import traceback
            traceback.print_exc()
            if 'new_doc' in locals():
                new_doc.close()
            raise save_error
        
        response_data = {"translated_file": output_path.name}
        print(f"[DEBUG] DEBUG: Returning JSON response: {response_data}")
        return JSONResponse(content=response_data)
    except Exception as e:
        print(f"Translation processing error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": f"Translation failed: {str(e)}"})

@app.post("/fill")
async def fill_form(filename: str = Form(...), user_inputs: str = Form(...), lang: str = Form(...)):
    input_path = OUTPUT_DIR / filename
    filled_output = OUTPUT_DIR / f"final_{lang}_{filename}"

    try:
        # Temporary mock for testing
        result = f"MOCK FILLED FORM: {user_inputs}"
        with open(filled_output, "w", encoding="utf-8") as f:
            f.write(result)
        return {"filled_file": filled_output.name}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/preview/{filename}")
@app.head("/preview/{filename}")
async def preview_file(filename: str):
    """Serve file for preview (same as download but with different headers)"""
    print(f"[DEBUG] DEBUG: Preview request for file: {filename}")
    
    # For languages with font issues, check if HTML version exists and use that for preview
    if any(lang in filename for lang in ['_he_', '_ar_', '_ru_', '_uk_']) and filename.endswith('.pdf'):
        html_filename = filename.replace('.pdf', '.html')
        html_path = OUTPUT_DIR / html_filename
        if html_path.exists():
            print(f"[DEBUG] DEBUG: Found HTML version for RTL language, using: {html_filename}")
            file_path = html_path
            filename = html_filename
        else:
            file_path = OUTPUT_DIR / filename
    else:
        file_path = OUTPUT_DIR / filename
    
    print(f"[DEBUG] DEBUG: Preview file path: {file_path}")
    print(f"[DEBUG] DEBUG: Preview file exists: {file_path.exists()}")
    
    if file_path.exists():
        import os
        file_size = os.path.getsize(file_path)
        print(f"[DEBUG] DEBUG: Preview file size: {file_size} bytes")
        
        # Validate file before serving (PDF or HTML)
        if file_path.suffix.lower() == '.pdf':
            try:
                import fitz
                test_doc = fitz.open(file_path)
                pages = len(test_doc)
                test_doc.close()
                print(f"[DEBUG] DEBUG: Preview PDF validation successful - {pages} pages")
            except Exception as validation_error:
                print(f"[ERROR] DEBUG: Preview PDF validation failed: {validation_error}")
                return JSONResponse(status_code=500, content={"error": f"PDF file is corrupted: {validation_error}"})
        elif file_path.suffix.lower() == '.html':
            print(f"[DEBUG] DEBUG: Preview HTML file detected - serving directly")
        
        print(f"[DEBUG] DEBUG: Serving preview file with inline headers")
        return FileResponse(
            path=file_path, 
            filename=filename,
            headers={
                "Content-Disposition": "inline",  # Display in browser instead of download
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "*"
            }
        )
    
    print(f"[ERROR] DEBUG: Preview file not found: {file_path}")
    return JSONResponse(status_code=404, content={"error": "File not found"})

@app.get("/health")
async def health_check():
    """Health check endpoint for container monitoring"""
    return {"status": "healthy", "message": "Docs Translator API is running"}

@app.get("/download/{filename}")
@app.head("/download/{filename}")
async def download(filename: str):
    print(f"[DEBUG] DEBUG: Download request for file: {filename}")
    file_path = OUTPUT_DIR / filename
    print(f"[DEBUG] DEBUG: Download file path: {file_path}")
    print(f"[DEBUG] DEBUG: Download file exists: {file_path.exists()}")
    
    if file_path.exists():
        import os
        file_size = os.path.getsize(file_path)
        print(f"[DEBUG] DEBUG: Download file size: {file_size} bytes")
        
        # Validate file before serving (PDF or HTML)
        if file_path.suffix.lower() == '.pdf':
            try:
                import fitz
                test_doc = fitz.open(file_path)
                pages = len(test_doc)
                test_doc.close()
                print(f"[DEBUG] DEBUG: Download PDF validation successful - {pages} pages")
            except Exception as validation_error:
                print(f"[ERROR] DEBUG: Download PDF validation failed: {validation_error}")
                return JSONResponse(status_code=500, content={"error": f"PDF file is corrupted: {validation_error}"})
        elif file_path.suffix.lower() == '.html':
            print(f"[DEBUG] DEBUG: Download HTML file detected - serving directly")
            
        print(f"[DEBUG] DEBUG: Serving download file")
        return FileResponse(path=file_path, filename=filename)
    
    print(f"[ERROR] DEBUG: Download file not found: {file_path}")
    return JSONResponse(status_code=404, content={"error": "File not found"})

# Browser-based PDF generation - no server endpoint needed
