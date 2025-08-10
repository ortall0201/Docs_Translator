# Deployment Guide for Docs Translator

## 🚀 Deployment with runmydocker.com

### Prerequisites
1. Docker Desktop installed and running locally (for testing)
2. Account on runmydocker.com
3. Git repository with your code

### 🔐 Environment Variables Setup

**CRITICAL: Your OpenAI API key will be stored securely as environment variables**

#### Backend Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

#### Frontend Environment Variables
```bash
VITE_API_URL=https://your-backend-container.runmydocker.com
```

### 📦 Container Setup

#### Backend Container
- **Dockerfile**: `backend/Dockerfile`
- **Port**: 8000
- **Environment**: Add `OPENAI_API_KEY` in runmydocker.com dashboard
- **Build Context**: `./backend`

#### Frontend Container  
- **Dockerfile**: `experiments/lovable_frontend/Dockerfile`
- **Port**: 80
- **Environment**: Add `VITE_API_URL` pointing to backend container
- **Build Context**: `./experiments/lovable_frontend`

### 🔗 Container Communication

1. **Deploy Backend First**
   - Upload backend folder to runmydocker.com
   - Set `OPENAI_API_KEY` environment variable
   - Get the backend URL (e.g., `https://abc123.runmydocker.com`)

2. **Deploy Frontend Second**
   - Upload frontend folder to runmydocker.com
   - Set `VITE_API_URL` to your backend URL
   - Frontend will connect to backend automatically

### 🧪 Local Testing (Optional)

```bash
# Build and test locally first
cd "C:\Users\user\Desktop\Docs_Translator"

# Start Docker Desktop, then:
docker build -t docs-translator-backend ./backend
docker build -t docs-translator-frontend ./experiments/lovable_frontend

# Test with docker-compose
docker-compose up
```

### ✅ Deployment Checklist

- [ ] Backend deployed on runmydocker.com
- [ ] `OPENAI_API_KEY` set as environment variable (secure)
- [ ] Backend URL obtained
- [ ] Frontend deployed on runmydocker.com  
- [ ] `VITE_API_URL` set to backend URL
- [ ] Test upload/translation functionality
- [ ] Test contact form and payment modal

### 🔒 Security Notes

✅ **Safe**: API key stored as environment variable on runmydocker.com
✅ **Safe**: .dockerignore excludes .env files
✅ **Safe**: No API keys in source code or Docker images
❌ **Never**: Commit .env files to Git
❌ **Never**: Hardcode API keys in Dockerfiles

Your OpenAI API key will be completely secure and only accessible to your backend container!