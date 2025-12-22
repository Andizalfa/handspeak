# api_server_fastapi.py
# Backend aplikasi - Handle auth, database, history, dan call ML service

from datetime import datetime, timedelta
from typing import List, Optional
import random
import string

import httpx
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import (
    Column, Integer, String, DateTime, Float, ForeignKey, create_engine
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

# ==========================
# 1. KONFIGURASI APLIKASI
# ==========================

# --- Konfigurasi ML Service URL ---
ML_SERVICE_URL = "http://localhost:8002"  # URL backend ML

# --- Konfigurasi JWT ---
SECRET_KEY = "ganti_dengan_string_rahasia_yang_panjang"  # GANTI di production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 hari

# --- Konfigurasi Email (Gmail SMTP) ---
# GANTI dengan credentials Gmail Anda
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "11231010@student.itk.ac.id"  # Email pengirim
SMTP_PASSWORD = "wmqx zmhj gsdb xrud"  # App Password Gmail (bukan password biasa)
SMTP_FROM_EMAIL = "HandSpeak <11231010@student.itk.ac.id>"

# --- Konfigurasi DB (MySQL) ---
# Format: mysql+pymysql://username:password@host:port/database
MYSQL_USER = "11231010_andizalfa"  # Ganti dengan username MySQL Anda
MYSQL_PASSWORD = "andizalfa05"  # Ganti dengan password MySQL Anda (kosongkan jika tidak ada password)
MYSQL_HOST = "localhost"  # atau IP server MySQL
MYSQL_PORT = "3306"  # port default MySQL
MYSQL_DATABASE = "handspeak"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# ==========================
# 2. OTP STORAGE (In-Memory)
# ==========================

# Dictionary untuk simpan OTP sementara: {email: {"otp": "123456", "expires": datetime}}
otp_storage = {}

def generate_otp(length=6):
    """Generate random OTP dengan 6 digit"""
    return ''.join(random.choices(string.digits, k=length))

async def send_email_otp(email: str, otp: str):
    """Kirim email OTP menggunakan Gmail SMTP"""
    try:
        print(f"📧 Attempting to send OTP to: {email}")
        
        # Buat pesan email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Kode Verifikasi HandSpeak"
        message["From"] = SMTP_FROM_EMAIL
        message["To"] = email
        
        # HTML body untuk email
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
              <h2 style="color: #5B8FB9; text-align: center;">HandSpeak</h2>
              <h3 style="color: #333;">Kode Verifikasi Akun Anda</h3>
              <p style="color: #666; line-height: 1.6;">
                Terima kasih telah mendaftar di HandSpeak. Gunakan kode OTP berikut untuk memverifikasi akun Anda:
              </p>
              <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                <h1 style="color: #5B8FB9; letter-spacing: 5px; margin: 0; font-size: 32px;">{otp}</h1>
              </div>
              <p style="color: #666; line-height: 1.6;">
                Kode ini akan kadaluarsa dalam <strong>5 menit</strong>.
              </p>
              <p style="color: #999; font-size: 12px; margin-top: 30px;">
                Jika Anda tidak melakukan pendaftaran ini, abaikan email ini.
              </p>
            </div>
          </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        print(f"📨 Connecting to SMTP server: {SMTP_HOST}:{SMTP_PORT}")
        
        # Kirim email
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True,
            timeout=30,  # Tambahkan timeout
        )
        
        print(f"✅ Email sent successfully to: {email}")
        return True
        
    except aiosmtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print("⚠️ Periksa SMTP_USER dan SMTP_PASSWORD di konfigurasi")
        return False
    except aiosmtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending email: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

# ==========================
# 2. SETUP DATABASE
# ==========================

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verifikasi koneksi sebelum digunakan
    pool_recycle=3600,  # Recycle koneksi setiap 1 jam
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, autoincrement=True, name="id_user")
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Simpan sebagai 'password', bukan 'hashed_password'
    created_at = Column(DateTime, default=datetime.utcnow)

    histories = relationship("SignLanguageHistory", back_populates="user")


class SignLanguageHistory(Base):
    __tablename__ = "SignLanguageHistory"

    id_history = Column(Integer, primary_key=True, autoincrement=True, name="id_history")
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False, name="id_user")
    kata_terdeteksi = Column(String(255), nullable=False, name="kata_terdeteksi")
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="histories")


# Tidak perlu create_all karena tabel sudah dibuat manual di MySQL
# Base.metadata.create_all(bind=engine)

# Dependency DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# 3. AUTH UTILS (JWT + HASH)
# ==========================

from passlib.context import CryptContext

# Ganti dari bcrypt ke pbkdf2_sha256 supaya tidak butuh modul bcrypt eksternal
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # path login


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


# ==========================
# 4. SCHEMAS (Pydantic)
# ==========================

# ----- OTP -----
class SendOTPRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

# ----- Auth -----
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    otp: str  # Tambahkan OTP untuk verifikasi


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id_user: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
        from_attributes = True  # Untuk SQLAlchemy 2.0+


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ----- Sequence Predict -----
class SequenceRequest(BaseModel):
    sequence: List[List[float]]
    fps: Optional[float] = None


class PredictionResponse(BaseModel):
    index: int              # index kelas (0..N-1)
    label: Optional[str]    # nama label dari LABELS
    max_proba: float        # probabilitas tertinggi
    probs: List[float]      # semua probabilitas (untuk debugging / grafik)

    class Config:
        orm_mode = True


# ----- History -----
class HistoryOut(BaseModel):
    id_history: int
    kata_terdeteksi: str
    confidence: float
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True  # Untuk SQLAlchemy 2.0+


# ==========================
# 5. FASTAPI APP
# ==========================

app = FastAPI(
    title="BISINDO Sign Backend",
    description="FastAPI backend dengan Auth, Prediksi LSTM, dan Riwayat",
    version="1.0.0",
)

# CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "*",  # dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"📥 {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"📤 Status: {response.status_code}")
    return response


# ==========================
# 7. DEPENDENCY: current_user
# ==========================

class TokenData(BaseModel):
    user_id: Optional[int] = None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Tidak dapat memvalidasi kredensial.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id_user == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user


# ==========================
# 8. ROUTES: HEALTH
# ==========================

@app.get("/health")
async def health_check():
    """Check backend app health and ML service connectivity"""
    try:
        async with httpx.AsyncClient() as client:
            ml_response = await client.get(f"{ML_SERVICE_URL}/health", timeout=5.0)
            ml_health = ml_response.json()
    except Exception as e:
        ml_health = {"status": "error", "message": str(e)}
    
    return {
        "status": "ok",
        "app_service": "running",
        "ml_service": ml_health,
    }


# ==========================
# 9. ROUTES: OTP
# ==========================

@app.post("/auth/send-otp")
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """
    Kirim kode OTP ke email untuk verifikasi registrasi
    """
    email = request.email
    
    print(f"\n{'='*60}")
    print(f"📥 Received OTP request for email: {email}")
    print(f"{'='*60}")
    
    # Cek apakah email sudah terdaftar
    existing_user = get_user_by_email(db, email)
    if existing_user:
        print(f"⚠️ Email already registered: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar. Silakan login."
        )
    
    # Generate OTP
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)  # OTP valid 5 menit
    
    print(f"🔑 Generated OTP: {otp} (expires at {expires_at})")
    
    # Simpan OTP ke storage
    otp_storage[email] = {
        "otp": otp,
        "expires": expires_at
    }
    
    print(f"💾 OTP stored in memory for: {email}")
    print(f"📊 Current OTP storage: {list(otp_storage.keys())}")
    
    # Kirim email
    print(f"📧 Attempting to send email to: {email}")
    email_sent = await send_email_otp(email, otp)
    
    if not email_sent:
        print(f"❌ Failed to send email to: {email}")
        # Hapus OTP dari storage karena gagal kirim
        if email in otp_storage:
            del otp_storage[email]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal mengirim email. Periksa konfigurasi SMTP atau pastikan email valid."
        )
    
    print(f"✅ OTP sent successfully to: {email}")
    print(f"{'='*60}\n")
    
    return {
        "message": "Kode OTP telah dikirim ke email Anda",
        "email": email,
        "expires_in_seconds": 300
    }


@app.post("/auth/verify-otp")
async def verify_otp(request: VerifyOTPRequest):
    """
    Verifikasi kode OTP yang diinput user
    """
    email = request.email
    otp = request.otp
    
    # Cek apakah ada OTP untuk email ini
    if email not in otp_storage:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP tidak ditemukan. Silakan kirim ulang OTP."
        )
    
    stored_data = otp_storage[email]
    
    # Cek apakah OTP sudah kadaluarsa
    if datetime.utcnow() > stored_data["expires"]:
        del otp_storage[email]  # Hapus OTP yang expired
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP telah kadaluarsa. Silakan kirim ulang OTP."
        )
    
    # Verifikasi OTP
    if stored_data["otp"] != otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP tidak valid."
        )
    
    return {
        "message": "Kode OTP berhasil diverifikasi",
        "email": email,
        "verified": True
    }


@app.post("/auth/forgot-password/send-otp")
async def forgot_password_send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """
    Kirim kode OTP ke email untuk reset password
    """
    email = request.email
    
    print(f"\n{'='*60}")
    print(f"🔐 Received forgot password OTP request for: {email}")
    print(f"{'='*60}")
    
    # Cek apakah email terdaftar
    existing_user = get_user_by_email(db, email)
    if not existing_user:
        print(f"⚠️ Email not found in database: {email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email tidak terdaftar. Silakan periksa kembali email Anda."
        )
    
    # Generate OTP
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)  # OTP valid 5 menit
    
    print(f"🔑 Generated OTP: {otp} (expires at {expires_at})")
    
    # Simpan OTP ke storage dengan prefix untuk forgot password
    forgot_password_key = f"forgot_password_{email}"
    otp_storage[forgot_password_key] = {
        "otp": otp,
        "expires": expires_at
    }
    
    print(f"💾 OTP stored for forgot password: {email}")
    
    # Kirim email
    print(f"📧 Attempting to send email to: {email}")
    email_sent = await send_email_otp(email, otp)
    
    if not email_sent:
        print(f"❌ Failed to send email to: {email}")
        # Hapus OTP dari storage karena gagal kirim
        if forgot_password_key in otp_storage:
            del otp_storage[forgot_password_key]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gagal mengirim email. Silakan coba lagi."
        )
    
    print(f"✅ Forgot password OTP sent successfully to: {email}")
    print(f"{'='*60}\n")
    
    return {
        "message": "Kode OTP untuk reset password telah dikirim ke email Anda",
        "email": email,
        "expires_in_seconds": 300
    }


@app.post("/auth/forgot-password/reset")
async def forgot_password_reset(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset password dengan verifikasi OTP
    """
    email = request.email
    otp = request.otp
    new_password = request.new_password
    
    print(f"\n{'='*60}")
    print(f"🔐 Password reset request for: {email}")
    print(f"{'='*60}")
    
    # Cek apakah email terdaftar
    user = get_user_by_email(db, email)
    if not user:
        print(f"⚠️ Email not found: {email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email tidak terdaftar."
        )
    
    # Verifikasi OTP
    forgot_password_key = f"forgot_password_{email}"
    if forgot_password_key not in otp_storage:
        print(f"⚠️ OTP not found for: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP tidak ditemukan. Silakan kirim ulang OTP."
        )
    
    stored_data = otp_storage[forgot_password_key]
    
    # Cek apakah OTP sudah kadaluarsa
    if datetime.utcnow() > stored_data["expires"]:
        del otp_storage[forgot_password_key]
        print(f"⚠️ OTP expired for: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP telah kadaluarsa. Silakan kirim ulang OTP."
        )
    
    # Verifikasi OTP
    if stored_data["otp"] != otp:
        print(f"⚠️ Invalid OTP for: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP tidak valid."
        )
    
    # Hapus OTP setelah berhasil diverifikasi
    del otp_storage[forgot_password_key]
    
    # Update password
    user.password = get_password_hash(new_password)
    db.commit()
    
    print(f"✅ Password updated successfully for: {email}")
    print(f"{'='*60}\n")
    
    return {
        "message": "Password berhasil direset. Silakan login dengan password baru Anda.",
        "email": email
    }


# ==========================
# 10. ROUTES: AUTH
# ==========================

@app.post("/auth/register", response_model=UserOut)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    Registrasi user baru dengan verifikasi OTP
    """
    # Cek apakah email sudah terdaftar
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar.",
        )
    
    # Verifikasi OTP sebelum registrasi
    email = user_in.email
    otp = user_in.otp
    
    if email not in otp_storage:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP tidak ditemukan. Silakan verifikasi email terlebih dahulu."
        )
    
    stored_data = otp_storage[email]
    
    # Cek apakah OTP sudah kadaluarsa
    if datetime.utcnow() > stored_data["expires"]:
        del otp_storage[email]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP telah kadaluarsa. Silakan kirim ulang OTP."
        )
    
    # Verifikasi OTP
    if stored_data["otp"] != otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode OTP tidak valid."
        )
    
    # Hapus OTP setelah berhasil diverifikasi
    del otp_storage[email]
    
    # Buat user baru
    user = User(
        name=user_in.name,
        email=user_in.email,
        password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_in.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email atau password salah.",
        )

    if not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email atau password salah.",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id_user)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)


@app.get("/auth/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ==========================
# 10. ROUTE: PREDICT SEQUENCE
# ==========================

@app.post("/predict_sequence_public", response_model=PredictionResponse)
async def predict_sequence_public(
    request: Request,
):
    """Endpoint tanpa autentikasi untuk testing gesture recognition"""
    # Parse body manually untuk debug
    try:
        body = await request.json()
        print(f"📦 Raw body keys: {body.keys() if isinstance(body, dict) else type(body)}")
        
        # Validasi dengan Pydantic
        req = SequenceRequest(**body)
        print(f"📥 Received sequence: {len(req.sequence)} frames")
    except Exception as e:
        print(f"❌ Error parsing request: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    
    # Forward request ke ML service
    try:
        async with httpx.AsyncClient() as client:
            ml_response = await client.post(
                f"{ML_SERVICE_URL}/predict",
                json={"sequence": req.sequence, "fps": req.fps},
                timeout=30.0
            )
            ml_response.raise_for_status()
            prediction = ml_response.json()
    except httpx.HTTPError as e:
        print(f"❌ Error calling ML service: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"ML service tidak tersedia: {str(e)}"
        )
    
    # Response ke frontend (tanpa simpan ke DB karena tidak ada user)
    return PredictionResponse(**prediction)


@app.post("/predict_sequence", response_model=PredictionResponse)
async def predict_sequence(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Parse body manually untuk debug
    try:
        body = await request.json()
        print(f"📦 Raw body keys: {body.keys() if isinstance(body, dict) else type(body)}")
        
        # Validasi dengan Pydantic
        req = SequenceRequest(**body)
        print(f"📥 Received sequence: {len(req.sequence)} frames")
    except Exception as e:
        print(f"❌ Error parsing request: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    
    # Forward request ke ML service
    try:
        async with httpx.AsyncClient() as client:
            ml_response = await client.post(
                f"{ML_SERVICE_URL}/predict",
                json={"sequence": req.sequence, "fps": req.fps},
                timeout=30.0
            )
            ml_response.raise_for_status()
            prediction = ml_response.json()
    except httpx.HTTPError as e:
        print(f"❌ Error calling ML service: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"ML service tidak tersedia: {str(e)}"
        )
    
    # Simpan ke riwayat di database
    label = prediction.get("label") or str(prediction.get("index"))
    history = SignLanguageHistory(
        id_user=current_user.id_user,
        kata_terdeteksi=label,
        confidence=prediction.get("max_proba"),
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    # Response ke frontend
    return PredictionResponse(**prediction)


# ==========================
# 11. ROUTE: HISTORY
# ==========================

@app.get("/history", response_model=List[HistoryOut])
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    histories = (
        db.query(SignLanguageHistory)
        .filter(SignLanguageHistory.id_user == current_user.id_user)
        .order_by(SignLanguageHistory.created_at.desc())
        .all()
    )
    return histories


@app.delete("/history")
def delete_all_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Hapus semua riwayat penerjemahan user yang sedang login
    """
    deleted_count = (
        db.query(SignLanguageHistory)
        .filter(SignLanguageHistory.id_user == current_user.id_user)
        .delete()
    )
    db.commit()
    
    return {
        "message": f"Berhasil menghapus {deleted_count} riwayat",
        "deleted_count": deleted_count
    }


# ==========================
# 12. ENTRY POINT
# ==========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_server_fastapi:app", host="0.0.0.0", port=8001, reload=False)
