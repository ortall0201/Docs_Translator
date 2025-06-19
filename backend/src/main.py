# src/main.py - FastAPI backend for doc translator with CrewAI integration

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import fitz  # PyMuPDF
from src.crew import run_crew

# Initialize app
app = FastAPI()

# Health check route
@app.get("/")
async def root():
    return {"message": "Docs Translator backend is running 🚀"}

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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

@app.post("/translate")
async def translate_form(filename: str = Form(...), lang: str = Form(...)):
    input_path = UPLOAD_DIR / filename
    output_path = OUTPUT_DIR / f"translated_{lang}_{filename}"

    try:
        # Extract text from PDF
        doc = fitz.open(input_path)
        content = ""
        for page in doc:
            content += page.get_text()
        doc.close()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"PDF parsing failed: {str(e)}"})

    try:
        # Run translation crew
        result = run_crew(
            mode="translate",
            text=content,
            source_lang="auto",
            target_lang=lang
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        return {"translated_file": output_path.name}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Translation failed: {str(e)}"})

@app.post("/fill")
async def fill_form(filename: str = Form(...), user_inputs: str = Form(...), lang: str = Form(...)):
    input_path = OUTPUT_DIR / filename
    filled_output = OUTPUT_DIR / f"final_{lang}_{filename}"

    try:
        result = run_crew(
            mode="fill",
            text=user_inputs,
            source_lang=lang,
            target_lang="auto"
        )
        with open(filled_output, "w", encoding="utf-8") as f:
            f.write(result)
        return {"filled_file": filled_output.name}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/download/{filename}")
async def download(filename: str):
    file_path = OUTPUT_DIR / filename
    if file_path.exists():
        return FileResponse(path=file_path, filename=filename)
    return JSONResponse(status_code=404, content={"error": "File not found"})
