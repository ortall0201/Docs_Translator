# 🐳 Docker Image Deployment Guide

## Prerequisites
1. **Docker Desktop** installed and running
2. **Docker Hub account** (free at hub.docker.com)
3. **runmydocker.com account**

## Step 1: Create Docker Hub Account
1. Go to https://hub.docker.com
2. Create free account (remember your username!)
3. Create two repositories:
   - `docs-translator-backend`
   - `docs-translator-frontend`

## Step 2: Build Docker Images Locally

### Open Command Prompt and run:

```bash
# Navigate to your project
cd "C:\Users\user\Desktop\Docs_Translator"

# Login to Docker Hub
docker login
# Enter your Docker Hub username and password

# Build Backend Image
docker build -t YOUR_DOCKERHUB_USERNAME/docs-translator-backend:latest ./backend

# Build Frontend Image  
docker build -t YOUR_DOCKERHUB_USERNAME/docs-translator-frontend:latest ./experiments/lovable_frontend

# Push Images to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/docs-translator-backend:latest
docker push YOUR_DOCKERHUB_USERNAME/docs-translator-frontend:latest
```

## Step 3: Deploy on runmydocker.com

### Backend Deployment:
- **Container Image**: `YOUR_DOCKERHUB_USERNAME/docs-translator-backend:latest`
- **Port**: `8000`
- **Environment Variables**:
  - `OPENAI_API_KEY` = your_actual_api_key

### Frontend Deployment:
- **Container Image**: `YOUR_DOCKERHUB_USERNAME/docs-translator-frontend:latest`  
- **Port**: `80`
- **Environment Variables**:
  - `VITE_API_URL` = your_backend_container_url

## Alternative: Use Pre-built Images

If Docker Desktop isn't working, I can help you use:
- **GitHub Actions** to auto-build images
- **Railway** or **Render** (easier alternatives)
- **Vercel + Railway** (frontend + backend separately)

## Quick Commands Reference

Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username:

```bash
# Check Docker is running
docker --version

# Build backend
docker build -t YOUR_DOCKERHUB_USERNAME/docs-translator-backend ./backend

# Build frontend
docker build -t YOUR_DOCKERHUB_USERNAME/docs-translator-frontend ./experiments/lovable_frontend

# Test locally (optional)
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key YOUR_DOCKERHUB_USERNAME/docs-translator-backend
```

🔐 **Security Note**: Your OpenAI API key will be secure as an environment variable!