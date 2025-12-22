# 🐳 Docker Deployment Guide - Railway

Panduan deployment HandSpeak menggunakan Docker di Railway.

---

## 📋 Pre-requisites

- ✅ Account Railway (https://railway.app)
- ✅ Account GitHub (untuk push code)
- ✅ Model sudah di-upload ke Hugging Face: `Andizalfa05/handspeak`
- ✅ MySQL Database sudah setup di Railway

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Railway Platform                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────────┐    ┌──────────────────┐   │
│  │  Backend ML     │    │  Backend App     │   │
│  │  (Port 8002)    │◄───┤  (Port 8001)     │   │
│  │  - TensorFlow   │    │  - FastAPI       │   │
│  │  - Hugging Face │    │  - MySQL         │   │
│  │  - Docker       │    │  - JWT Auth      │   │
│  └─────────────────┘    │  - OTP Email     │   │
│          ▲              │  - Docker        │   │
│          │              └──────────────────┘   │
│          │                       │              │
│  ┌───────┴────────┐    ┌─────────▼──────────┐ │
│  │  Hugging Face  │    │  Railway MySQL     │ │
│  │  Model Storage │    │  Database          │ │
│  └────────────────┘    └────────────────────┘ │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 📦 Step 1: Test Docker Locally

### Backend ML

```bash
cd backend_ml

# Build image
docker build -t handspeak-ml .

# Run container (test)
docker run -p 8002:8002 \
  -e HF_REPO_ID=Andizalfa05/handspeak \
  handspeak-ml

# Test endpoint
curl http://localhost:8002/health
```

### Backend App

```bash
cd backend

# Build image
docker build -t handspeak-api .

# Run container (test) - perlu database connection
docker run -p 8001:8001 \
  -e DB_HOST=your-db-host \
  -e DB_PORT=3306 \
  -e DB_USER=root \
  -e DB_PASSWORD=your-password \
  -e DB_NAME=railway \
  -e ML_SERVICE_URL=http://localhost:8002 \
  handspeak-api

# Test endpoint
curl http://localhost:8001/health
```

---

## 🚀 Step 2: Deploy Backend ML ke Railway

### 2.1 Push ke GitHub

```bash
cd backend_ml

# Init git (jika belum)
git init

# Add files
git add .
git commit -m "Add Backend ML with Docker"

# Push ke GitHub
git remote add origin https://github.com/USERNAME/handspeak-backend-ml.git
git branch -M main
git push -u origin main
```

### 2.2 Deploy di Railway

1. **Buka Railway**: https://railway.app/new
2. **Deploy from GitHub repo**:
   - Pilih repository: `handspeak-backend-ml`
   - Railway akan auto-detect Dockerfile
3. **Set Environment Variables**:
   ```
   HF_REPO_ID=Andizalfa05/handspeak
   PORT=8002
   ```
4. **Generate Domain**:
   - Settings → Networking → Generate Domain
   - Contoh: `handspeak-ml.up.railway.app`
5. **Wait for deployment** (~5-10 menit, download model dari HF)

### 2.3 Verify Deployment

```bash
# Health check
curl https://handspeak-ml.up.railway.app/health

# Expected response:
{
  "status": "ok",
  "model_loaded": true,
  "sequence_length": 45,
  "num_labels": 50
}
```

---

## 🚀 Step 3: Deploy Backend App ke Railway

### 3.1 Push ke GitHub

```bash
cd backend

# Init git
git init
git add .
git commit -m "Add Backend App with Docker"

# Push
git remote add origin https://github.com/USERNAME/handspeak-backend-app.git
git branch -M main
git push -u origin main
```

### 3.2 Deploy di Railway

1. **Deploy from GitHub**:
   - Pilih repository: `handspeak-backend-app`
2. **Set Environment Variables**:
   ```env
   # Database (dari Railway MySQL yang sudah ada)
   DB_HOST=containers-us-west-xxx.railway.app
   DB_PORT=6789
   DB_USER=root
   DB_PASSWORD=xxx
   DB_NAME=railway
   
   # ML Service (dari Backend ML yang sudah deploy)
   ML_SERVICE_URL=https://handspeak-ml.up.railway.app
   
   # SMTP (Gmail)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   
   # JWT
   SECRET_KEY=your-super-secret-key-change-this
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   
   # Port
   PORT=8001
   ```
3. **Generate Domain**:
   - Contoh: `handspeak-api.up.railway.app`
4. **Deploy**

### 3.3 Verify Deployment

```bash
# Health check
curl https://handspeak-api.up.railway.app/health

# Expected response:
{
  "status": "ok",
  "app_service": "running",
  "ml_service": {
    "status": "ok",
    "model_loaded": true
  }
}
```

---

## 🎯 Step 4: Deploy Frontend ke Vercel

### 4.1 Update API URLs

File: `frontend/src/api/apiClient.js`

```javascript
const API_BASE = import.meta.env.VITE_API_BASE || "https://handspeak-api.up.railway.app";
```

File: `frontend/.env.production`

```env
VITE_API_BASE=https://handspeak-api.up.railway.app
```

### 4.2 Deploy ke Vercel

1. **Push ke GitHub**:
   ```bash
   cd frontend
   git init
   git add .
   git commit -m "Frontend with production config"
   git push
   ```

2. **Import di Vercel**:
   - Framework: **Vite**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Environment Variables**:
   ```env
   VITE_API_BASE=https://handspeak-api.up.railway.app
   ```

4. **Deploy**

### 4.3 Update CORS

Setelah dapat domain Vercel, update environment variable di **Backend App**:

```env
FRONTEND_URL=https://handspeak.vercel.app
```

Dan update code di `backend/api_server_fastapi.py`:

```python
origins = [
    "https://handspeak.vercel.app",
    "http://localhost:5173",
]
```

Commit dan push lagi, Railway akan auto-redeploy.

---

## 🔍 Monitoring & Logs

### Railway Logs

```bash
# Via Railway CLI (opsional)
npm i -g @railway/cli
railway login
railway logs
```

### Via Dashboard
- Railway → Service → **Logs** tab
- Real-time logs
- Filter by level (info, error, warning)

### Health Checks

```bash
# Backend ML
curl https://handspeak-ml.up.railway.app/health

# Backend App
curl https://handspeak-api.up.railway.app/health

# Frontend
curl https://handspeak.vercel.app
```

---

## 🐛 Troubleshooting

### ❌ Build Failed

**Problem**: Docker build gagal

**Solution**:
1. Cek Dockerfile syntax
2. Cek requirements.txt valid
3. Lihat Railway build logs untuk error spesifik

### ❌ Model Download Failed

**Problem**: Tidak bisa download dari Hugging Face

**Solution**:
1. Cek `HF_REPO_ID` benar
2. Repository harus public
3. Cek Railway logs untuk error detail
4. Pastikan file `bisindo_best.h5` dan `labels.json` ada di repo HF

### ❌ Database Connection Failed

**Problem**: Backend tidak bisa connect ke MySQL

**Solution**:
1. Cek environment variables database
2. Railway MySQL harus running
3. Test connection dari Railway shell:
   ```bash
   railway run python -c "import pymysql; print('OK')"
   ```

### ❌ CORS Error

**Problem**: Frontend tidak bisa call backend

**Solution**:
1. Update `FRONTEND_URL` di backend env vars
2. Redeploy backend
3. Clear browser cache

---

## 📊 Resource Usage (Estimasi)

| Service | Memory | CPU | Disk |
|---------|--------|-----|------|
| Backend ML | ~800MB | 0.5 CPU | ~500MB |
| Backend App | ~200MB | 0.2 CPU | ~100MB |
| MySQL | ~150MB | 0.1 CPU | ~200MB |

**Railway Hobby Plan**: $5/month + usage
- ~$15-20/month untuk 3 services

---

## 🎉 Success Checklist

- [ ] Backend ML deployed dan health check OK
- [ ] Backend App deployed dan health check OK
- [ ] Database tables created
- [ ] Frontend deployed di Vercel
- [ ] CORS configured properly
- [ ] Test registration flow (OTP email)
- [ ] Test login
- [ ] Test camera prediction
- [ ] Test history page
- [ ] All services reachable via HTTPS

---

## 🔐 Security Notes

- ✅ Semua service menggunakan HTTPS
- ✅ Environment variables di Railway (tidak di-commit)
- ✅ JWT untuk authentication
- ✅ OTP untuk email verification
- ✅ Database password strong
- ✅ CORS restricted ke frontend domain saja

---

## 📚 Useful Commands

```bash
# Build & test locally
docker build -t my-service .
docker run -p 8001:8001 my-service

# Check container logs
docker logs <container-id>

# Access container shell
docker exec -it <container-id> bash

# Clean up
docker system prune -a
```

---

**Ready to deploy! 🚀**
