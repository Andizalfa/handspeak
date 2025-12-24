# 🔧 Panduan Memperbaiki Error CORS di Deployment

## 📋 Masalah yang Ditemukan

Error yang muncul:
```
Access to fetch at 'https://handspeak-production.up.railway.app/history' 
from origin 'https://handspeak-one.vercel.app' has been blocked by CORS policy
```

## ✅ Solusi yang Sudah Diterapkan

### 1. Backend (Railway) - CORS Configuration
File `backend/api_server_fastapi.py` sudah diupdate dengan konfigurasi CORS yang benar:

```python
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "https://handspeak-one.vercel.app",  # Frontend Vercel
    "https://handspeak-production.up.railway.app",  # Backend Railway
    "https://backendml-production-326a.up.railway.app",  # Backend ML Railway
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # Penting untuk expose headers
)
```

## 🚀 Langkah-langkah yang Harus Dilakukan

### 1. Deploy Backend yang Sudah Diupdate ke Railway

```bash
cd backend
git add api_server_fastapi.py
git commit -m "fix: update CORS configuration for production"
git push origin main
```

Railway akan otomatis deploy ulang backend Anda.

### 2. Set Environment Variable di Vercel

Masuk ke dashboard Vercel Anda dan set environment variable:

**Cara:**
1. Buka project `handspeak-one` di dashboard Vercel
2. Pergi ke **Settings** → **Environment Variables**
3. Tambahkan variable berikut:

| Name | Value |
|------|-------|
| `VITE_API_BASE` | `https://handspeak-production.up.railway.app` |
| `VITE_ML_API_BASE` | `https://backendml-production-326a.up.railway.app` |

**Penting:** 
- Pastikan URL **TIDAK** ada trailing slash di akhir
- URL Railway harus sesuai dengan URL deployment Anda

### 3. Redeploy Frontend di Vercel

Setelah environment variable diset, Anda perlu redeploy:

**Option A: Melalui Dashboard Vercel**
1. Pergi ke **Deployments**
2. Klik tiga titik pada deployment terakhir
3. Pilih **Redeploy**

**Option B: Melalui Git Push**
```bash
cd frontend
git commit --allow-empty -m "trigger redeploy"
git push origin main
```

### 4. Verifikasi Environment Variable di Frontend (Opsional)

Jika ingin memastikan environment variable terbaca dengan baik, buat file `.env.production` di folder frontend:

```bash
# frontend/.env.production
VITE_API_BASE=https://handspeak-production.up.railway.app
VITE_ML_API_BASE=https://backendml-production-326a.up.railway.app
```

**JANGAN COMMIT FILE INI!** Tambahkan ke `.gitignore`:
```bash
echo ".env.production" >> .gitignore
```

## 🔍 Cara Mengecek Apakah Sudah Berfungsi

1. **Cek Backend Railway:**
   ```bash
   curl -X GET https://handspeak-production.up.railway.app/docs
   ```
   Seharusnya muncul halaman dokumentasi Swagger UI.

2. **Cek CORS Header:**
   ```bash
   curl -X OPTIONS https://handspeak-production.up.railway.app/history \
     -H "Origin: https://handspeak-one.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -i
   ```
   
   Response seharusnya mengandung:
   ```
   Access-Control-Allow-Origin: https://handspeak-one.vercel.app
   Access-Control-Allow-Methods: *
   Access-Control-Allow-Headers: *
   ```

3. **Test di Browser:**
   - Buka https://handspeak-one.vercel.app
   - Buka Developer Console (F12)
   - Login ke aplikasi
   - Coba akses halaman History
   - Seharusnya tidak ada error CORS lagi

## 🐛 Troubleshooting

### Jika masih ada error CORS:

1. **Pastikan Railway sudah deploy ulang:**
   - Cek di Railway dashboard apakah deployment baru sudah selesai
   - Cek logs Railway untuk memastikan tidak ada error

2. **Pastikan environment variable di Vercel sudah benar:**
   - Cek di Vercel Settings → Environment Variables
   - Pastikan URL Railway tidak ada typo
   - Pastikan tidak ada spasi di awal atau akhir URL

3. **Clear cache browser:**
   - Hard refresh dengan Ctrl+Shift+R (Windows) atau Cmd+Shift+R (Mac)
   - Atau buka di Incognito/Private mode

4. **Cek Network Tab di Browser:**
   - Buka Developer Tools → Network
   - Filter untuk request ke `/history`
   - Lihat Request Headers dan Response Headers
   - Pastikan Authorization header terkirim

### Jika Frontend tidak menggunakan URL yang benar:

Kemungkinan environment variable tidak terbaca. Solusi:
1. Pastikan variable dimulai dengan `VITE_` (bukan hanya `API_BASE`)
2. Redeploy ulang frontend setelah set environment variable
3. Cek build logs di Vercel untuk memastikan tidak ada error

## 📝 Catatan Penting

1. **Environment Variable di Vercel:**
   - Harus diawali dengan `VITE_` agar terbaca oleh Vite
   - Harus di-set sebelum build
   - Perlu redeploy setelah mengubah nilai

2. **CORS di Production:**
   - Jangan gunakan `"*"` untuk allow_origins di production
   - Explicit list domain yang diizinkan lebih aman
   - Pastikan domain frontend dan backend sesuai

3. **Railway Auto-Deploy:**
   - Railway akan otomatis deploy saat ada push ke branch yang dikonfigurasi
   - Cek logs untuk memastikan deployment sukses

## 🎯 Checklist

- [ ] Backend CORS config sudah diupdate
- [ ] Backend sudah di-push ke Railway
- [ ] Railway deployment sudah selesai
- [ ] Environment variable `VITE_API_BASE` sudah diset di Vercel
- [ ] Frontend sudah di-redeploy
- [ ] Test di browser, tidak ada error CORS
- [ ] Test login berhasil
- [ ] Test akses halaman history berhasil

---

**Setelah semua langkah dilakukan, aplikasi Anda seharusnya sudah berfungsi dengan baik!** 🎉
