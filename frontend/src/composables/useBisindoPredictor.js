// src/composables/useBisindoPredictor.js
import { ref } from "vue";
import { predictSequence as apiPredictSequence, predictSequenceWithAuth } from "@/api/apiClient";
// Hapus import isLoggedIn, kita cek manual tokennya biar pasti

// [PERBAIKAN] Tingkatkan sequence length untuk gerakan yang lebih lengkap
const SEQUENCE_LENGTH = 45;  // Dari 30 ke 45 frames (1.5x lebih lama)
const NUM_FEATURES = 126;

// [PERBAIKAN] Turunkan threshold agar tidak terlalu strict
const MIN_CONFIDENCE = 0.70;  // Dari 0.75 ke 0.70

// [PERBAIKAN BARU] Tambahkan min frames untuk mulai prediksi
const MIN_FRAMES_FOR_PREDICTION = 40;  // Minimal 40 frames sebelum prediksi

// [PERBAIKAN BARU] Deteksi gerakan selesai dengan stabilitas hand position
const MOTION_STABILITY_FRAMES = 5;  // Cek 5 frame terakhir untuk stabilitas
const MOTION_THRESHOLD = 0.02;  // Threshold untuk mendeteksi gerakan berhenti 

const sequenceBuffer = ref([]);      
const handMetadataBuffer = ref([]);  
const lastPrediction = ref(null);    
const isPredicting = ref(false);
const errorMessage = ref("");

// Timer untuk auto-reset buffer jika tidak ada tangan
let resetTimer = null;
const IDLE_TIMEOUT = 2000; 

// [PERBAIKAN] Tingkatkan delay antar prediksi untuk stabilitas
let lastPredictionTime = 0;
const PREDICTION_COOLDOWN = 2500;  // Dari 1500ms ke 2500ms (2.5 detik) 

function resetBuffer() {
  if (sequenceBuffer.value.length > 0) {
    console.log('🧹 Buffer di-reset karena tidak ada gerakan tangan.');
    sequenceBuffer.value = [];
    handMetadataBuffer.value = [];
  }
}

function cancelBufferReset() {
  if (resetTimer) {
    clearTimeout(resetTimer);
    resetTimer = null;
  }
}

function scheduleBufferReset() {
  cancelBufferReset();
  resetTimer = setTimeout(() => {
    resetBuffer();
  }, IDLE_TIMEOUT);
}

// [FUNGSI BARU] Deteksi apakah gerakan sudah stabil (berhenti)
function isMotionStable(buffer) {
  if (buffer.length < MOTION_STABILITY_FRAMES + 1) return false;
  
  // Ambil N frame terakhir
  const recentFrames = buffer.slice(-MOTION_STABILITY_FRAMES - 1);
  
  // Hitung rata-rata perubahan posisi antar frame
  let totalMotion = 0;
  for (let i = 1; i < recentFrames.length; i++) {
    const prevFrame = recentFrames[i - 1];
    const currFrame = recentFrames[i];
    
    // Hitung euclidean distance antar frame
    let frameDiff = 0;
    for (let j = 0; j < Math.min(prevFrame.length, currFrame.length); j++) {
      frameDiff += Math.abs(currFrame[j] - prevFrame[j]);
    }
    totalMotion += frameDiff;
  }
  
  const avgMotion = totalMotion / (recentFrames.length - 1);
  
  // Jika rata-rata pergerakan kecil = gerakan stabil
  return avgMotion < MOTION_THRESHOLD;
}

async function pushFrame(frameFeatures, handMetadata = { hasRight: false, hasLeft: false }) {
  if (!Array.isArray(frameFeatures)) return;
  if (frameFeatures.length !== NUM_FEATURES) return;

  cancelBufferReset();

  if (isPredicting.value) return;

  const now = Date.now();
  const timeSinceLastPrediction = now - lastPredictionTime;
  if (timeSinceLastPrediction < PREDICTION_COOLDOWN && lastPredictionTime > 0) {
    return;
  }

  sequenceBuffer.value.push(frameFeatures);
  handMetadataBuffer.value.push(handMetadata);

  // Logging progress buffer setiap 15 frame
  if (sequenceBuffer.value.length % 15 === 0) {
    console.log(`📊 Buffer: ${sequenceBuffer.value.length}/${SEQUENCE_LENGTH} frames`);
  }

  // [PERBAIKAN] Tunggu minimal frames dan gerakan stabil sebelum prediksi
  if (sequenceBuffer.value.length < MIN_FRAMES_FOR_PREDICTION) return;
  
  // Cek apakah gerakan sudah stabil
  const isStable = isMotionStable(sequenceBuffer.value);
  if (!isStable) {
    console.log('⏳ Menunggu gerakan selesai...');
    // Jika sudah mencapai max length tapi belum stabil, tetap lanjut prediksi
    if (sequenceBuffer.value.length < SEQUENCE_LENGTH) return;
  }
  
  // Jika buffer overflow
  if (sequenceBuffer.value.length > SEQUENCE_LENGTH) {
    sequenceBuffer.value = [];
    handMetadataBuffer.value = [];
    return;
  }

  // Cek konsistensi tangan
  const handConsistency = checkHandConsistency(handMetadataBuffer.value);
  if (!handConsistency.isConsistent) {
    console.log('⚠️ Inkonsistensi tangan - Skip prediksi');
    sequenceBuffer.value = [];
    handMetadataBuffer.value = [];
    return;
  }

  try {
    isPredicting.value = true;
    errorMessage.value = "";

    const seqToSend = [...sequenceBuffer.value];
    
    // [PERBAIKAN 2] Cek token langsung dari localStorage
    // Ini memastikan kita benar-benar tahu ada token atau tidak saat request dikirim
    const token = localStorage.getItem("access_token");
    let raw;

    try {
      if (token) {
        console.log('🔐 Token ditemukan, mengirim dengan Auth...');
        // Pastikan fungsi ini di apiClient.js benar-benar memasang header Authorization!
        raw = await predictSequenceWithAuth(seqToSend);
      } else {
        console.log('👤 Token tidak ada, mengirim sebagai Guest...');
        raw = await apiPredictSequence(seqToSend);
      }
    } catch (authError) {
      console.warn('⚠️ Gagal request, mencoba fallback...', authError);
      raw = await apiPredictSequence(seqToSend);
    }

    const data = raw?.data ?? raw;
    if (!data) throw new Error("Response kosong.");

    const confidence = Number(data.max_proba ?? NaN);
    const predictedLabel = data.label;
    
    // [PERBAIKAN 3] Logika Confidence
    if (confidence < MIN_CONFIDENCE) {
      console.log(`⚠️ Terdeteksi "${predictedLabel}" tapi confidence rendah (${(confidence * 100).toFixed(0)}%)`);
      
      // Tetap tampilkan feedback ke user tapi labelnya "none" atau beri tanda tanya
      lastPrediction.value = {
        prediction_label: "none", // Frontend akan mengabaikan ini
        confidence: confidence,
        reason: "Confidence rendah"
      };
    } else {
      // Prediksi Valid
      lastPrediction.value = {
        prediction_index: data.index ?? null,
        prediction_label: predictedLabel,
        confidence: confidence,
        probabilities: data.probs ?? [],
      };
      
      console.log(`✅ HASIL: ${predictedLabel} (${(confidence * 100).toFixed(0)}%)`);
      
      // Jika user login, seharusnya Backend SUDAH menyimpannya saat request predictSequenceWithAuth di atas.
      if (token) {
          console.log("💾 Data seharusnya tersimpan di History Database.");
      }
    }
    
    lastPredictionTime = Date.now();
    sequenceBuffer.value = [];
    handMetadataBuffer.value = [];

  } catch (err) {
    console.error("❌ Error Prediksi:", err);
    errorMessage.value = "Gagal memproses prediksi.";
    sequenceBuffer.value = [];
    handMetadataBuffer.value = [];
  } finally {
    isPredicting.value = false;
  }
}

function checkHandConsistency(handMetadata) {
  if (handMetadata.length === 0) return { isConsistent: false };

  const patterns = {};
  handMetadata.forEach(meta => {
    const pattern = `${meta.hasRight ? 'R' : ''}${meta.hasLeft ? 'L' : ''}`;
    patterns[pattern] = (patterns[pattern] || 0) + 1;
  });

  const dominantPattern = Object.keys(patterns).reduce((a, b) => 
    patterns[a] > patterns[b] ? a : b
  );
  const consistencyRatio = patterns[dominantPattern] / handMetadata.length;

  // Turunkan sedikit threshold konsistensi jika perlu (0.7)
  return {
    isConsistent: consistencyRatio >= 0.7, 
    dominantHand: dominantPattern
  };
}

function onNoHandDetected() {
  scheduleBufferReset();
}

export function useBisindoPredictor() {
  return {
    SEQUENCE_LENGTH,
    NUM_FEATURES,
    sequenceBuffer,
    lastPrediction,
    isPredicting,
    errorMessage,
    pushFrame,
    onNoHandDetected,
    resetBuffer,
  };
}