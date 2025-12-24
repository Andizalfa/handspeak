# backend_ml/main.py
# Service khusus untuk ML model inference

from typing import List, Optional
import json
import os
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from huggingface_hub import hf_hub_download

# ==========================
# 1. KONFIGURASI ML MODEL
# ==========================

# Hugging Face Configuration
# GANTI dengan repository Anda sendiri!
HF_REPO_ID = os.getenv("HF_REPO_ID", "Andizalfa05/handspeak")  # Format: username/repo-name
HF_MODEL_FILE = "bisindo_best.h5"
HF_LABELS_FILE = "labels.json"

# Force download from HuggingFace even if local files exist
# Set to True to always download fresh model from HF
FORCE_DOWNLOAD_FROM_HF = os.getenv("FORCE_DOWNLOAD_FROM_HF", "False").lower() == "true"

# Local paths (akan di-download ke sini)
LOCAL_MODEL_DIR = "models"
MODEL_PATH = os.path.join(LOCAL_MODEL_DIR, HF_MODEL_FILE)
LABELS_PATH = os.path.join(LOCAL_MODEL_DIR, HF_LABELS_FILE)

SEQUENCE_LENGTH = 45      # Tingkatkan dari 30 ke 45 untuk gerakan lebih lengkap
NUM_FEATURES = 126        # 21 landmarks * 2 hands * 3 coords (x,y,z)

# Toleransi untuk sequence length (model di-train dengan 30, tapi bisa handle lebih)
MIN_SEQUENCE_LENGTH = 30  # Minimal yang diterima
MAX_SEQUENCE_LENGTH = 60  # Maksimal yang diterima

# ==========================
# 2. SCHEMAS (Pydantic)
# ==========================

class SequenceRequest(BaseModel):
    sequence: List[List[float]]
    fps: Optional[float] = None


class PredictionResponse(BaseModel):
    index: int              # index kelas (0..N-1)
    label: Optional[str] = None       # nama label dari LABELS
    max_proba: float        # probabilitas tertinggi
    probs: List[float]      # semua probabilitas


# ==========================
# 3. DOWNLOAD MODEL FROM HUGGING FACE
# ==========================

def download_model_from_huggingface():
    """
    Download model dan labels dari Hugging Face jika belum ada di lokal
    atau jika FORCE_DOWNLOAD_FROM_HF = True
    """
    print("\n" + "="*60)
    print("🤗 Checking Hugging Face models...")
    print(f"   Repository: {HF_REPO_ID}")
    print(f"   Force download: {FORCE_DOWNLOAD_FROM_HF}")
    print("="*60)
    
    # Create models directory if not exists
    os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)
    
    try:
        # Download model file
        if not os.path.exists(MODEL_PATH) or FORCE_DOWNLOAD_FROM_HF:
            if FORCE_DOWNLOAD_FROM_HF and os.path.exists(MODEL_PATH):
                print(f"🔄 Force downloading model (overwriting local file)...")
            else:
                print(f"📥 Downloading model from Hugging Face: {HF_REPO_ID}/{HF_MODEL_FILE}")
            
            model_path = hf_hub_download(
                repo_id=HF_REPO_ID,
                filename=HF_MODEL_FILE,
                cache_dir="./cache",
                local_dir=LOCAL_MODEL_DIR,
                local_dir_use_symlinks=False,
                force_download=FORCE_DOWNLOAD_FROM_HF
            )
            print(f"✅ Model downloaded to: {model_path}")
        else:
            print(f"✅ Model already exists locally: {MODEL_PATH}")
            print(f"   💡 Set FORCE_DOWNLOAD_FROM_HF=true to re-download from HuggingFace")
        
        # Download labels file (optional - fallback ke lokal jika tidak ada)
        if not os.path.exists(LABELS_PATH) or FORCE_DOWNLOAD_FROM_HF:
            try:
                if FORCE_DOWNLOAD_FROM_HF and os.path.exists(LABELS_PATH):
                    print(f"🔄 Force downloading labels (overwriting local file)...")
                else:
                    print(f"📥 Downloading labels from Hugging Face: {HF_REPO_ID}/{HF_LABELS_FILE}")
                
                labels_path = hf_hub_download(
                    repo_id=HF_REPO_ID,
                    filename=HF_LABELS_FILE,
                    cache_dir="./cache",
                    local_dir=LOCAL_MODEL_DIR,
                    local_dir_use_symlinks=False,
                    force_download=FORCE_DOWNLOAD_FROM_HF
                )
                print(f"✅ Labels downloaded to: {labels_path}")
            except Exception as label_error:
                print(f"⚠️ Labels not found in HF repository: {label_error}")
                print(f"💡 Will try to use local labels.json if available")
        else:
            print(f"✅ Labels already exists locally: {LABELS_PATH}")
        
        print("="*60)
        return True
        
    except Exception as e:
        print(f"❌ Error downloading from Hugging Face: {e}")
        print("⚠️  Make sure:")
        print("   1. HF_REPO_ID is correct (format: username/repo-name)")
        print("   2. Repository is public or you have access")
        print("   3. Files exist in the repository")
        print("="*60)
        return False


# ==========================
# 4. FASTAPI APP
# ==========================

app = FastAPI(
    title="BISINDO ML Service",
    description="Service khusus untuk ML model inference",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8001",  # Backend aplikasi
    "http://127.0.0.1:5500",
    "https://handspeak-one.vercel.app",
    "*",  # dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ==========================
# 5. LOAD MODEL & LABELS
# ==========================

# Download model from Hugging Face if needed
download_success = download_model_from_huggingface()

if not download_success:
    print("⚠️  Continuing with local files (if available)...")

print("\n🔁 Loading BISINDO LSTM model...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"✅ Model loaded successfully from: {MODEL_PATH}")
    print(f"   Model input shape: {model.input_shape}")
    print(f"   Model output shape: {model.output_shape}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

try:
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        LABELS = json.load(f)
    print(f"✅ Loaded {len(LABELS)} labels from: {LABELS_PATH}")
except FileNotFoundError:
    LABELS = []
    print("⚠️ labels.json tidak ditemukan, label hanya index.")

print("="*60 + "\n")


# ==========================
# 6. ROUTES
# ==========================

@app.get("/")
def root():
    return {
        "service": "BISINDO ML Service",
        "status": "running",
        "model_loaded": model is not None,
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "sequence_length": SEQUENCE_LENGTH,
        "min_sequence_length": MIN_SEQUENCE_LENGTH,
        "max_sequence_length": MAX_SEQUENCE_LENGTH,
        "num_features": NUM_FEATURES,
        "labels_available": len(LABELS) > 0,
        "num_labels": len(LABELS),
        "labels": LABELS,
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(req: SequenceRequest):
    """
    Endpoint untuk prediksi sequence dengan support dynamic sequence length
    """
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model belum dimuat dengan benar."
        )
    
    # Konversi ke numpy
    seq = np.array(req.sequence, dtype=np.float32)
    
    # Validasi bentuk data: (timesteps, features)
    if seq.ndim != 2:
        raise HTTPException(
            status_code=400,
            detail=f"Sequence harus 2D (timesteps, features), tetapi dapat shape {seq.shape}",
        )
    
    timesteps, features = seq.shape
    
    # [PERBAIKAN] Validasi dengan toleransi
    if timesteps < MIN_SEQUENCE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Sequence terlalu pendek. Minimal {MIN_SEQUENCE_LENGTH} frames, diterima {timesteps}"
        )
    
    if timesteps > MAX_SEQUENCE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Sequence terlalu panjang. Maksimal {MAX_SEQUENCE_LENGTH} frames, diterima {timesteps}"
        )
    
    # [PERBAIKAN] Resample atau pad ke 30 frames (sesuai training)
    if timesteps != 30:
        print(f"🔄 Original sequence: {timesteps} frames")
        if timesteps > 30:
            # Resample: ambil 30 frame yang merata
            indices = np.linspace(0, timesteps - 1, 30).astype(int)
            seq = seq[indices]
            print(f"📉 Resampled to 30 frames")
        else:
            # Padding dengan frame terakhir
            last_frame = seq[-1:]
            padding_needed = 30 - timesteps
            seq = np.vstack([seq, np.repeat(last_frame, padding_needed, axis=0)])
            print(f"📈 Padded to 30 frames")
    
    # DEBUG: Cek statistik data yang masuk
    print(f"🔍 Final sequence shape: {seq.shape}")
    if seq.shape[1] == 126:
        # Ambil frame pertama untuk analisis
        first_frame = seq[0]
        right_hand = first_frame[:63]
        left_hand = first_frame[63:]
        right_sum = np.sum(np.abs(right_hand))
        left_sum = np.sum(np.abs(left_hand))
        print(f"🔍 First frame - Right hand sum: {right_sum:.2f}, Left hand sum: {left_sum:.2f}")
        print(f"🔍 Data range - Min: {seq.min():.4f}, Max: {seq.max():.4f}, Mean: {seq.mean():.4f}")
    
    # Validasi final shape setelah resample
    timesteps, features = seq.shape
    if timesteps != 30:
        raise HTTPException(
            status_code=400,
            detail=f"Sequence length harus 30 setelah resample, tetapi dapat {timesteps}",
        )
    if features != NUM_FEATURES:
        raise HTTPException(
            status_code=400,
            detail=f"Jumlah fitur harus {NUM_FEATURES}, tetapi dapat {features}",
        )
    
    # Tambahkan dimensi batch: (1, T, F)
    seq_batch = np.expand_dims(seq, axis=0)
    
    # Prediksi
    probs = model.predict(seq_batch, verbose=0)[0]   # shape: (num_classes,)
    pred_idx = int(np.argmax(probs))                 # index kelas
    max_proba = float(probs[pred_idx])               # probabilitas tertinggi
    
    # Get label
    label = None
    if LABELS and 0 <= pred_idx < len(LABELS):
        label = LABELS[pred_idx]
    
    print(f"✅ Prediction: {label} (index={pred_idx}, confidence={max_proba:.4f})")
    
    # Response
    return PredictionResponse(
        index=pred_idx,
        label=label,
        max_proba=max_proba,
        probs=[float(p) for p in probs],
    )


# ==========================
# 7. ENTRY POINT
# ==========================

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Gunakan PORT dari env Railway, default ke 8000 atau port lain jika lokal
    port = int(os.getenv("PORT", 8080)) 
    
    uvicorn.run(app, host="0.0.0.0", port=port)