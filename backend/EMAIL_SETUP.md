# 📧 Konfigurasi Email untuk OTP

## Setup Gmail SMTP

Untuk mengirim email OTP, Anda perlu mengkonfigurasi Gmail SMTP dengan App Password.

### Langkah 1: Buat App Password Gmail

1. **Login ke Gmail** Anda
2. Buka **Google Account Settings**: https://myaccount.google.com/
3. Pilih **Security** di menu kiri
4. Aktifkan **2-Step Verification** (jika belum aktif)
5. Setelah 2FA aktif, cari **App passwords**
6. Pilih **Mail** sebagai app dan **Other (Custom name)** sebagai device
7. Masukkan nama: `HandSpeak Backend`
8. Klik **Generate**
9. **Salin 16-digit app password** yang muncul

### Langkah 2: Update Konfigurasi Backend

Edit file `api_server_fastapi.py` pada bagian konfigurasi email (baris ~40-45):

```python
# --- Konfigurasi Email (Gmail SMTP) ---
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@gmail.com"  # 👈 GANTI dengan email Anda
SMTP_PASSWORD = "your_app_password"  # 👈 GANTI dengan App Password (16 digit)
SMTP_FROM_EMAIL = "HandSpeak <your_email@gmail.com>"  # 👈 GANTI
```

**Contoh:**
```python
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "handspeak.app@gmail.com"
SMTP_PASSWORD = "abcd efgh ijkl mnop"  # App Password dari Google
SMTP_FROM_EMAIL = "HandSpeak <handspeak.app@gmail.com>"
```

### Langkah 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Langkah 4: Test Kirim Email

Jalankan backend dan test endpoint:

```bash
python api_server_fastapi.py
```

Buka browser atau Postman dan test:
```
POST http://localhost:8001/auth/send-otp
Content-Type: application/json

{
  "email": "test@example.com"
}
```

## Alternatif: Menggunakan SendGrid atau Mailgun

Jika tidak ingin menggunakan Gmail, Anda bisa gunakan layanan email lain:

### SendGrid
1. Daftar di https://sendgrid.com/
2. Dapatkan API Key
3. Update konfigurasi untuk gunakan SendGrid API

### Mailgun
1. Daftar di https://www.mailgun.com/
2. Dapatkan SMTP credentials
3. Update SMTP_HOST, SMTP_USER, SMTP_PASSWORD

## Troubleshooting

### Error: "Username and Password not accepted"
- ✅ Pastikan 2-Step Verification aktif
- ✅ Gunakan App Password, bukan password Gmail biasa
- ✅ Hapus spasi dari App Password (16 karakter tanpa spasi)

### Error: "Connection refused"
- ✅ Cek firewall/antivirus yang mungkin blok port 587
- ✅ Pastikan koneksi internet stabil

### Email tidak diterima
- ✅ Cek folder Spam
- ✅ Tunggu beberapa menit (kadang delay)
- ✅ Verifikasi email pengirim valid di Gmail settings

## Flow Registrasi dengan OTP

1. **Step 1**: User input email → Backend kirim OTP via email
2. **Step 2**: User input OTP 6 digit → Backend verifikasi
3. **Step 3**: User lengkapi data (nama, password) → Registrasi selesai

## Keamanan

- ✅ OTP expired setelah 5 menit
- ✅ OTP hanya bisa digunakan 1 kali
- ✅ Password di-hash menggunakan PBKDF2-SHA256
- ✅ Email verifikasi mencegah spam registration

## Notes

⚠️ **PENTING**: Jangan commit App Password ke Git! 
Gunakan environment variables untuk production:

```python
import os

SMTP_USER = os.getenv("SMTP_USER", "your_email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_app_password")
```
