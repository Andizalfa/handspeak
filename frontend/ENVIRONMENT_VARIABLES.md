# 🔧 Environment Variables - Frontend

## 📋 File Environment

Frontend menggunakan **Vite** yang mendukung environment variables dengan prefix `VITE_`.

### File yang tersedia:

1. **`.env`** - Development (local)
2. **`.env.production`** - Production (Vercel/deploy)
3. **`.env.example`** - Template

---

## 🌍 Environment Variables

### `VITE_API_BASE`

URL backend API untuk fetch data.

**Development:**
```env
VITE_API_BASE=http://localhost:8001
```

**Production (Railway):**
```env
VITE_API_BASE=https://handspeak-api.up.railway.app
```

---

## 📝 Cara Menggunakan

### 1. Development (Local)

File: `.env`
```env
VITE_API_BASE=http://localhost:8001
```

Jalankan dev server:
```bash
npm run dev
```

### 2. Production (Vercel)

#### Option A: File `.env.production`

File: `.env.production`
```env
VITE_API_BASE=https://handspeak-api.up.railway.app
```

Build untuk production:
```bash
npm run build
```

#### Option B: Environment Variables di Vercel Dashboard

1. Buka Vercel Dashboard → Project → **Settings** → **Environment Variables**
2. Tambahkan:
   - **Key**: `VITE_API_BASE`
   - **Value**: `https://handspeak-api.up.railway.app`
   - **Environment**: Production, Preview, Development (pilih sesuai kebutuhan)
3. Redeploy

---

## 📄 File yang Menggunakan Environment Variable

### 1. `src/api/apiClient.js`
```javascript
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8001";
```

### 2. `src/pages/HistoryPage.vue`
```javascript
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8001";
```

### 3. `src/pages/LoginPage.vue`
```javascript
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8001";
```

### 4. `src/pages/RegisterPage.vue`
```javascript
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8001";
```

---

## 🔄 Update URL Backend Setelah Deploy

### Langkah-langkah:

1. **Deploy Backend di Railway** → Dapat URL: `https://handspeak-api.up.railway.app`

2. **Update `.env.production`**:
   ```env
   VITE_API_BASE=https://handspeak-api.up.railway.app
   ```

3. **Commit & Push**:
   ```bash
   git add .
   git commit -m "Update production API URL"
   git push
   ```

4. **Vercel akan auto-redeploy** dengan environment variable baru

**ATAU** update langsung di Vercel Dashboard (Settings → Environment Variables)

---

## 🧪 Testing

### Test Local:
```bash
# Check environment variable di browser console
console.log(import.meta.env.VITE_API_BASE)
# Output: http://localhost:8001
```

### Test Production:
```bash
# Build production
npm run build

# Preview
npm run preview

# Check di browser console
console.log(import.meta.env.VITE_API_BASE)
# Output: https://handspeak-api.up.railway.app
```

---

## ⚠️ Important Notes

1. **Prefix `VITE_` wajib** untuk Vite expose variable ke client
2. **Restart dev server** setelah ubah `.env`
3. **File `.env` jangan di-commit** (sudah ada di `.gitignore`)
4. **`.env.production` boleh di-commit** (untuk production build)
5. **Fallback value** (`|| "http://localhost:8001"`) untuk dev tanpa `.env`

---

## 🎯 Deploy Checklist

- [ ] Backend deployed di Railway → dapat URL
- [ ] Update `VITE_API_BASE` di `.env.production`
- [ ] Commit & push ke GitHub
- [ ] Deploy frontend di Vercel
- [ ] Verify environment variable di Vercel dashboard
- [ ] Test API calls dari frontend production
- [ ] Update CORS di backend (tambahkan frontend URL)

---

## 🐛 Troubleshooting

### ❌ Environment variable tidak terdeteksi

**Problem**: `import.meta.env.VITE_API_BASE` undefined

**Solution**:
1. Pastikan prefix `VITE_` ada
2. Restart dev server (`Ctrl+C` lalu `npm run dev`)
3. Clear cache browser
4. Check typo di nama variable

### ❌ Production masih pakai localhost

**Problem**: Production API call ke localhost

**Solution**:
1. Cek `.env.production` ada dan terisi
2. Build ulang: `npm run build`
3. Atau set di Vercel environment variables
4. Clear build cache di Vercel

### ❌ CORS error di production

**Problem**: Backend block request dari frontend

**Solution**:
1. Update CORS di backend `api_server_fastapi.py`:
   ```python
   origins = [
       "https://handspeak.vercel.app",  # Frontend URL
       "http://localhost:5173",
   ]
   ```
2. Redeploy backend

---

**Ready untuk production deployment! 🚀**
