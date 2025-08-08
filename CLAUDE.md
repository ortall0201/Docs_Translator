# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Document Translator App that uses AI to translate foreign-language forms and documents. Users upload PDFs, get AI-powered translations with annotations for bureaucratic terms, and can download the translated results.

**Tech Stack:**
- Frontend: React with axios for API communication
- Backend: FastAPI with CrewAI agents for AI-powered translation
- AI: OpenAI GPT-4 via CrewAI framework
- PDF Processing: PyMuPDF (fitz) for text extraction

## Architecture

### Backend (FastAPI + CrewAI)
The backend uses a multi-agent AI system with two specialized agents:

1. **FormTranslatorAgent**: Translates documents and provides annotations for unclear bureaucratic terms
2. **ResponseBackTranslatorAgent**: Translates user responses back to official language

**Key Files:**
- `backend/src/main.py`: FastAPI server with 4 endpoints (/upload, /translate, /fill, /download)
- `backend/src/crew.py`: CrewAI agent definitions and orchestration
- `backend/src/tools/`: Custom CrewAI tools (TranslationTool, AnnotationTool)

**File Flow:**
- Uploads saved to `backend/uploads/`
- Translated outputs saved to `backend/outputs/`
- PDF text extraction happens in `/translate` endpoint before CrewAI processing

### Frontend (React)
React app with component-based architecture:

- `App.js`: Main orchestration, manages state flow between upload → translate → download
- `UploadForm.js`: File upload handling with FormData
- `TranslateForm.js`: Language selection and translation requests
- `PDFViewer.js`: PDF display component (uses react-pdf)

**API Communication:**
All requests use axios to communicate with backend at `http://127.0.0.1:8000`

## Development Commands

### Backend Setup and Running
```bash
cd backend

# Install dependencies (requires Python 3.13+)
pip install -r requirements.txt

# Start development server
python -m uvicorn src.main:app --reload
# Server runs at http://localhost:8000

# Test specific functionality
python src/test_run.py
```

### Frontend Setup and Running
```bash
cd frontend

# Install dependencies
npm install

# Start development server  
npm start
# App runs at http://localhost:3000

# Run tests
npm test

# Build for production
npm run build
```

## Environment Setup

**Required:**
- OpenAI API key in `backend/.env`:
  ```
  OPENAI_API_KEY=your_key_here
  ```

**Backend Dependencies:**
- fastapi, uvicorn (web server)
- crewai, openai (AI agents)
- PyMuPDF (imported as `fitz` for PDF processing) 
- python-dotenv (environment variables)

**Frontend Dependencies:**
- React 19.1.0, react-dom
- axios (API requests)
- react-pdf, pdfjs-dist (PDF viewing)

## Key Implementation Details

### CrewAI Integration
- Uses GPT-4 model (`gpt-4o`) with temperature=0 for consistent translations
- Two custom tools: TranslationTool (basic mock) and AnnotationTool (static glossary)
- Crew runs in two modes: "translate" and "fill" based on endpoint called
- All AI processing is orchestrated through `run_crew()` function

### PDF Processing
- Uses PyMuPDF (`fitz`) to extract text from uploaded PDFs
- Text extraction happens in main.py before sending to CrewAI
- No OCR - only extracts selectable text from PDFs

### API Endpoints
- `POST /upload`: Saves file to uploads/ directory
- `POST /translate`: Extracts PDF text, runs CrewAI translation, saves to outputs/
- `POST /fill`: Processes user form responses (back-translation)
- `GET /download/{filename}`: Serves files from outputs/ directory

### State Management
React uses simple state lifting - App.js manages filename and translatedFile state, passing callbacks to child components. No external state management library used.

## Testing and Validation

The app includes a test file (`backend/src/test_run.py`) for backend functionality testing. Frontend uses standard React testing setup with @testing-library.

**API Testing:**
Test backend endpoints directly at http://localhost:8000/docs (FastAPI auto-generated docs)