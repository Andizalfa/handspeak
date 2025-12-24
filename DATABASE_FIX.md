# 🗄️ Database Setup untuk Railway MySQL

## ✅ Masalah yang Sudah Diperbaiki

Error sebelumnya:
```
Table 'railway.SignLanguageHistory' doesn't exist
```

**Root Cause:** Database MySQL di Railway belum memiliki tabel-tabel yang dibutuhkan.

**Solusi:** Backend sudah diupdate untuk **auto-create tables** saat startup.

## 🚀 Deployment Sequence

### 1. Backend Auto-Deploy
Railway akan otomatis deploy backend setelah git push. Proses:

1. ✅ Push ke GitHub sudah selesai
2. ⏳ Railway akan otomatis pull changes
3. ⏳ Rebuild backend container
4. ⏳ Saat startup, backend akan create tables otomatis
5. ✅ Tables created: `users` dan `SignLanguageHistory`

**Timeline:** 2-3 menit

### 2. Verifikasi Deployment

**Cek Railway Logs:**
1. Buka Railway Dashboard → Backend service
2. Pergi ke tab **Logs**
3. Cari message: `✅ Database tables created/verified successfully`
4. Jika muncul, artinya tables sudah dibuat ✅

**Jika ada error:**
```
⚠️ Warning: Could not create tables: [error message]
```
Screenshot dan share error message-nya.

### 3. Test Aplikasi

Setelah Railway deployment selesai (cek status di Railway dashboard):

1. Buka https://handspeak-one.vercel.app
2. Login dengan akun yang sudah ada
3. Akses halaman **History**
4. ✅ Seharusnya tidak ada error lagi!

## 📋 Database Schema

Tables yang dibuat otomatis:

### Table: `users`
```sql
CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Table: `SignLanguageHistory`
```sql
CREATE TABLE SignLanguageHistory (
    id_history INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    kata_terdeteksi VARCHAR(255) NOT NULL,
    confidence FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);
```

## 🔍 Troubleshooting

### Jika masih error "Table doesn't exist":

**1. Cek Railway MySQL Environment Variables**

Pastikan environment variables ini ada di Railway backend:
```
MYSQL_HOST=${{MySQL.MYSQLHOST}}
MYSQL_PORT=${{MySQL.MYSQLPORT}}
MYSQL_USER=${{MySQL.MYSQLUSER}}
MYSQL_PASSWORD=${{MySQL.MYSQLPASSWORD}}
MYSQL_DATABASE=${{MySQL.MYSQLDATABASE}}
```

**Format:** Harus menggunakan `${{MySQL.XXX}}` untuk reference service MySQL Railway.

**2. Cek MySQL Service Status**

Di Railway dashboard:
- Pastikan MySQL service sudah running
- Cek apakah backend ter-link dengan MySQL service

**3. Manual Create Tables (Jika Auto-Create Gagal)**

Jika auto-create gagal, bisa manual create via Railway MySQL CLI:

1. Railway Dashboard → MySQL service
2. Klik **Connect**
3. Copy connection string
4. Run SQL commands untuk create tables (schema di atas)

### Error Lain yang Mungkin Muncul:

**Error: "Access denied for user"**
- MySQL credentials salah
- Cek environment variables di Railway

**Error: "Can't connect to MySQL server"**
- MySQL service belum running
- Network issue antara backend dan MySQL service
- Cek Railway service links

**Error: "Unknown database"**
- Database name salah di environment variable
- Pastikan `MYSQL_DATABASE` sesuai dengan yang di-create Railway

## ⏱️ Timeline Fix

- [x] Update backend code untuk auto-create tables
- [x] Commit dan push ke GitHub
- [ ] Railway auto-deploy (2-3 menit) - **SEDANG PROSES**
- [ ] Verify tables created di logs
- [ ] Test aplikasi

## 📸 Verification Checklist

Setelah Railway deployment selesai:

- [ ] Railway backend deployment status: **Ready** ✅
- [ ] Railway logs menunjukkan: `✅ Database tables created/verified successfully`
- [ ] Test endpoint `/history` return status 200 (bukan 500)
- [ ] Frontend bisa load history page tanpa error
- [ ] Bisa create new history entry (test deteksi gesture)

---

## 🎯 Next Steps

**Tunggu 2-3 menit untuk Railway deployment, lalu:**

1. Refresh halaman https://handspeak-one.vercel.app
2. Login
3. Test halaman History
4. ✅ Should work now!

**Jika masih error, share:**
- Railway backend logs (screenshot)
- Error message dari browser console
- Network tab screenshot

---

**Backend sudah di-push dan Railway sedang auto-deploy!** ⏳
