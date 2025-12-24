# ⚙️ Vercel Environment Variables Setup

## 🎯 Environment Variables yang Harus Diset

Untuk frontend yang di-deploy di Vercel, Anda **HARUS** menset environment variables berikut:

### Variables:

```
VITE_API_BASE=https://handspeak-production.up.railway.app
VITE_ML_API_BASE=https://backendml-production-326a.up.railway.app
```

## 📝 Cara Setting di Vercel Dashboard

1. **Login ke Vercel**
   - Buka https://vercel.com/dashboard
   - Pilih project **handspeak-one**

2. **Masuk ke Settings**
   - Klik tab **Settings** di menu atas
   - Pilih **Environment Variables** di sidebar kiri

3. **Tambahkan Variable**
   
   **Variable 1: Backend API**
   - **Name:** `VITE_API_BASE`
   - **Value:** `https://handspeak-production.up.railway.app`
   - **Environment:** Pilih semua (Production, Preview, Development)
   - Klik **Save**
   
   **Variable 2: Backend ML**
   - **Name:** `VITE_ML_API_BASE`
   - **Value:** `https://backendml-production-326a.up.railway.app`
   - **Environment:** Pilih semua (Production, Preview, Development)
   - Klik **Save**

4. **Redeploy**
   - Pergi ke tab **Deployments**
   - Klik **⋮** (tiga titik) pada deployment paling atas
   - Pilih **Redeploy**
   - Tunggu hingga deployment selesai (biasanya 1-2 menit)

## ⚠️ PENTING!

- ✅ **Pastikan URL TIDAK ada trailing slash** (`/`) di akhir
  - ✅ Benar: `https://handspeak-production.up.railway.app`
  - ❌ Salah: `https://handspeak-production.up.railway.app/`

- ✅ **Variable harus diawali dengan `VITE_`**
  - Vite hanya membaca environment variable yang dimulai dengan `VITE_`
  - `API_BASE` tidak akan terbaca, harus `VITE_API_BASE`

- ✅ **Redeploy setelah menambah/mengubah variable**
  - Environment variable hanya dibaca saat build time
  - Perubahan variable tidak otomatis apply ke deployment yang sudah ada

## 🔍 Cara Verifikasi

### 1. Cek di Browser Console
Setelah deployment selesai, buka frontend Anda dan ketik di console:
```javascript
console.log(import.meta.env.VITE_API_BASE)
```

Seharusnya output: `https://handspeak-production.up.railway.app`

### 2. Cek Network Request
1. Buka Developer Tools (F12)
2. Pergi ke tab **Network**
3. Login ke aplikasi
4. Cek request ke API
5. URL request harus mengarah ke Railway, bukan localhost

### 3. Test Functionality
- Login ke aplikasi
- Coba akses halaman History
- Tidak ada error CORS di console
- Data history berhasil dimuat

## 🔄 Alternative: Deploy via CLI

Jika lebih suka menggunakan Vercel CLI:

```bash
# Install Vercel CLI (jika belum)
npm i -g vercel

# Set environment variables
vercel env add VITE_API_BASE production
# Masukkan: https://handspeak-production.up.railway.app

vercel env add VITE_ML_API_BASE production
# Masukkan: https://backendml-production-326a.up.railway.app

# Redeploy
vercel --prod
```

## 📸 Screenshot Panduan

### Dashboard Vercel → Settings → Environment Variables
```
┌─────────────────────────────────────────────────────────┐
│ Name              │ Value                                │
├─────────────────────────────────────────────────────────┤
│ VITE_API_BASE     │ https://handspeak-production.up...  │
│ VITE_ML_API_BASE  │ https://backendml-production-32...  │
└─────────────────────────────────────────────────────────┘
```

## ❓ Troubleshooting

**Q: Variable sudah diset tapi frontend masih request ke localhost**
- A: Pastikan sudah redeploy setelah set variable
- A: Clear browser cache dan refresh halaman

**Q: Error "import.meta.env.VITE_API_BASE is undefined"**
- A: Pastikan nama variable benar (harus diawali `VITE_`)
- A: Pastikan environment dipilih (Production/Preview/Development)
- A: Redeploy ulang

**Q: Railway URL berubah, apa yang harus dilakukan?**
- A: Update nilai variable di Vercel
- A: Redeploy frontend
- A: Update juga CORS origins di backend jika URL Railway berubah

---

**Setelah langkah ini, frontend Anda seharusnya sudah connect dengan backend Railway!** ✅
