# 📄 Form Translator App

A clean, AI-powered tool that allows users to upload foreign-language forms, get an annotated translation, fill them out in their native language, and receive a finalized document ready for submission — all without human translation.

## 🚀 Features

- Upload and translate official documents (PDFs or text)
- Annotated guidance for common bureaucratic terms
- Fill forms in your own language, then auto-translate responses
- Secure, private, no document storage
- Free to use (MVP phase)

## 🧠 Tech Stack

- **Frontend:** React + Tailwind CSS
- **Backend:** FastAPI + CrewAI agents (LLM-powered)
- **Translation:** OpenAI GPT (via API)
- **Deployment:** Local or Cloud (Hugging Face / GCP)

## 📁 Project Structure

```
form-translator-app/
├── backend/              # FastAPI backend + CrewAI agents
├── frontend/             # React frontend
├── .gitignore            # Clean repo, no secrets
├── LICENSE.txt           # Proprietary license
├── README.md             # You're here
```

## ⚙️ Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI key
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 🛡️ Disclaimer
This app is provided as a free tool. No responsibility is assumed for translation accuracy or legal use. Users are responsible for verifying results. We do not store your files or data.

## 📬 Contact
Built with 💙 by Ortal Y. — for questions or collaborations, reach out via LinkedIn.

---
*This project is proprietary. All rights reserved.*
