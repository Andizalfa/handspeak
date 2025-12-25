<template>
  <section id="camera-section" class="py-16 sm:py-20 px-4 sm:px-6 bg-gradient-to-br from-[#E8F4F8] to-[#D4EBF3]">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-8 sm:mb-10">
        <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-800 mb-3 sm:mb-4">
          Coba Sekarang
        </h2>
        <p class="text-base sm:text-lg text-gray-600">
          Mulai terjemahkan bahasa isyarat BISINDO secara real-time
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-6 lg:gap-8 items-start">
        
        <!-- Camera Preview -->
        <div class="flex flex-col h-full w-full">
          <div class="bg-white rounded-2xl shadow-xl p-4 sm:p-5 flex flex-col h-full border-2 border-white/50 backdrop-blur-sm">
            
            <div class="flex flex-col gap-2 mb-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-gradient-to-br from-[#64CCC5] to-[#4FB8B0]">
                    <Camera class="w-4 h-4 text-white" />
                  </div>
                  <h2 class="text-gray-800 font-bold text-base sm:text-lg">Preview Kamera</h2>
                </div>

                <div class="flex items-center gap-2">
                  <div
                    v-if="isDetecting && sequenceBuffer.length >= SEQUENCE_LENGTH"
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-100 border border-amber-200"
                  >
                    <div class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
                    <span class="text-xs font-semibold text-amber-800 whitespace-nowrap">
                      Mendeteksi...
                    </span>
                  </div>

                  <button
                    @click="toggleDetection"
                    class="py-2 px-4 sm:px-5 text-white rounded-lg shadow-md hover:shadow-lg transition-all duration-200 hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2 text-sm font-semibold min-w-[100px]"
                    :class="isDetecting ? 'bg-gradient-to-r from-red-500 to-red-600' : 'bg-gradient-to-r from-[#5B8FB9] to-[#4A7BA7]'"
                  >
                    <component :is="isDetecting ? Square : Play" class="w-4 h-4 fill-current" />
                    {{ isDetecting ? "Hentikan" : "Mulai" }}
                  </button>
                </div>
              </div>

              <div class="sm:hidden flex items-start gap-2 p-2.5 rounded-lg bg-amber-50 border border-amber-100">
                <AlertCircle class="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
                <p class="text-gray-700 text-xs leading-snug">
                  Pastikan pencahayaan cukup terang dan tangan Anda berada di dalam frame kamera untuk hasil deteksi yang optimal.
                </p>
              </div>
            </div>

            <div class="relative bg-slate-900 rounded-xl overflow-hidden shadow-inner w-full aspect-[4/3] sm:aspect-video lg:h-[400px] xl:h-[480px]">
              
              <div
                v-if="!isDetecting"
                class="absolute inset-0 flex flex-col items-center justify-center text-white z-10 bg-slate-900/90"
              >
                <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full flex items-center justify-center mb-4 bg-white/10 backdrop-blur-sm animate-pulse">
                  <Camera class="w-8 h-8 sm:w-10 sm:h-10 text-white/50" />
                </div>
                <p class="text-base sm:text-lg font-medium mb-1">Kamera Belum Aktif</p>
                <p class="text-xs sm:text-sm text-slate-400">
                  Klik tombol "Mulai" untuk mengaktifkan
                </p>
              </div>

              <video
                ref="videoRef"
                autoplay
                playsinline
                muted
                class="w-full h-full object-cover scale-x-[-1]"
              ></video>

              <canvas
                ref="canvasRef"
                class="absolute inset-0 w-full h-full pointer-events-none object-cover scale-x-[-1]"
              ></canvas>
            </div>

            <div class="mt-4 hidden sm:flex items-start gap-3 p-3 rounded-lg bg-amber-50 border border-amber-100">
              <AlertCircle class="w-5 h-5 text-amber-500 flex-shrink-0" />
              <p class="text-gray-700 text-xs sm:text-sm leading-snug">
                Pastikan pencahayaan cukup terang dan tangan Anda berada di dalam frame kamera untuk hasil deteksi yang optimal.
              </p>
            </div>
          </div>
        </div>

        <!-- Translation Result -->
        <div class="flex flex-col h-full w-full">
          <div class="bg-white rounded-2xl shadow-xl p-4 sm:p-5 flex flex-col h-[400px] lg:h-full border-2 border-white/50 backdrop-blur-sm">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-gradient-to-br from-[#FFD95A] to-[#FFC830]">
                <Sparkles class="w-4 h-4 text-gray-800" />
              </div>
              <h2 class="text-gray-800 font-bold text-base sm:text-lg">Hasil Terjemahan</h2>
            </div>

            <div class="flex-1 p-4 rounded-xl overflow-y-auto shadow-inner bg-slate-50 border-2 border-[#64CCC5]/30 relative transition-all">
              <div v-if="accumulatedText">
                <p class="text-gray-800 text-base sm:text-lg leading-relaxed whitespace-pre-wrap font-medium">
                  {{ accumulatedText }}
                </p>
              </div>
              
              <div
                v-else
                class="flex flex-col items-center justify-center h-full text-center px-4"
              >
                <div class="w-16 h-16 rounded-full flex items-center justify-center mb-4 bg-slate-100">
                  <Sparkles class="w-8 h-8 text-slate-300" />
                </div>
                <p class="text-gray-500 text-sm sm:text-base font-medium mb-1">
                  Hasil terjemahan muncul di sini
                </p>
                <p class="text-gray-400 text-xs">
                  {{ !isDetecting ? 'Menunggu kamera aktif...' : 'Menunggu gerakan tangan...' }}
                </p>
              </div>
            </div>

            <div class="mt-4 flex items-center justify-between px-3 py-2 rounded-lg bg-blue-50/50 border border-blue-100">
              <div class="flex items-center gap-2">
                <Activity class="w-4 h-4 text-[#5B8FB9]" />
                <span class="text-xs sm:text-sm font-semibold text-gray-700">
                  {{ accumulatedText ? accumulatedText.split(" ").length : 0 }} kata
                </span>
              </div>
              <span class="text-[10px] sm:text-xs text-gray-500 font-medium truncate max-w-[150px]">
                {{ lastPrediction ? "Terdeteksi: " + (lastPrediction.prediction_label || 'Unknown') : "Standby" }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onUnmounted, nextTick, watch } from "vue";
import { Camera, Play, Square, AlertCircle, Sparkles, Activity } from "lucide-vue-next";
import { Hands, HAND_CONNECTIONS } from "@mediapipe/hands";
import { Camera as MediaPipeCamera } from "@mediapipe/camera_utils";
import { drawConnectors, drawLandmarks } from "@mediapipe/drawing_utils";
import { useBisindoPredictor } from "@/composables/useBisindoPredictor";

// Internal state
const isDetecting = ref(false);
const videoRef = ref(null);
const canvasRef = ref(null);
const accumulatedText = ref("");

// MediaPipe instances
let hands = null;
let mpCamera = null;

// from composable
const {
  SEQUENCE_LENGTH,
  NUM_FEATURES,
  sequenceBuffer,
  lastPrediction,
  errorMessage,
  pushFrame,
  onNoHandDetected,
  resetBuffer,
} = useBisindoPredictor();

// --------- Normalisasi & fitur -----------
function normalizeHand(coords63) {
  if (!coords63 || coords63.length !== 63) return new Array(63).fill(0);
  
  const sum = coords63.reduce((a, b) => a + Math.abs(b), 0);
  if (sum === 0) return new Array(63).fill(0);
  
  const hand = [];
  for (let i = 0; i < 63; i += 3) {
    hand.push([coords63[i], coords63[i + 1], coords63[i + 2] ?? 0]);
  }
  
  const wrist = hand[0];
  const normalized = [];
  for (const [x, y, z] of hand) {
    normalized.push([x - wrist[0], y - wrist[1], z - wrist[2]]);
  }
  
  let maxDist = 0;
  for (const [x, y, z] of normalized) {
    const dist = Math.sqrt(x * x + y * y + z * z);
    if (dist > maxDist) maxDist = dist;
  }
  
  const result = [];
  if (maxDist > 1e-6) {
    for (const [x, y, z] of normalized) {
      result.push(x / maxDist, y / maxDist, z / maxDist);
    }
  } else {
    for (const [x, y, z] of normalized) {
      result.push(x, y, z);
    }
  }
  
  return result;
}

function flattenLandmarksToFeatures(results) {
  let leftRaw = new Array(63).fill(0);
  let rightRaw = new Array(63).fill(0);

  const multiHandLandmarks = results.multiHandLandmarks || [];
  const multiHandedness = results.multiHandedness || [];

  for (let i = 0; i < multiHandLandmarks.length; i++) {
    const landmarks = multiHandLandmarks[i];
    const handedInfo = multiHandedness[i];
    const handed = handedInfo?.label || handedInfo?.categoryName || "Right";
    
    const coords = [];
    for (const lm of landmarks) {
      coords.push(lm.x, lm.y, lm.z ?? 0);
    }

    if (handed === "Left") leftRaw = coords;
    else rightRaw = coords;
  }

  const leftNorm = normalizeHand(leftRaw);
  const rightNorm = normalizeHand(rightRaw);
  
  const features = [...rightNorm, ...leftNorm];
  const rightSum = rightNorm.reduce((a, b) => a + Math.abs(b), 0);
  const leftSum = leftNorm.reduce((a, b) => a + Math.abs(b), 0);
  
  return {
    features,
    handMetadata: {
      hasRight: rightSum > 0,
      hasLeft: leftSum > 0
    }
  };
}

// --------- Callback hasil MediaPipe -----------
function onResults(results) {
  const videoEl = videoRef.value;
  const canvasEl = canvasRef.value;
  if (!videoEl || !canvasEl) return;

  const handsDetected = results.multiHandLandmarks?.length || 0;
  if (handsDetected === 0) {
    onNoHandDetected();
  }

  const ctx = canvasEl.getContext("2d");
  
  const w = videoEl.videoWidth || 640;
  const h = videoEl.videoHeight || 480;
  
  canvasEl.width = w;
  canvasEl.height = h;

  ctx.save();
  ctx.clearRect(0, 0, w, h);

  if (results.multiHandLandmarks) {
    for (const landmarks of results.multiHandLandmarks) {
      drawConnectors(ctx, landmarks, HAND_CONNECTIONS, {
        lineWidth: 3,
        color: '#64CCC5'
      });
      drawLandmarks(ctx, landmarks, { 
        radius: 4,
        color: '#FFD95A',
        lineWidth: 1
      });
    }
  }
  ctx.restore();

  if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
    const { features, handMetadata } = flattenLandmarksToFeatures(results);
    pushFrame(features, handMetadata);
  }
}

// Update teks akumulasi setiap ada prediksi baru
watch(lastPrediction, (res) => {
  if (!res) return;
  
  const label = res.prediction_label ?? `Kelas ${res.prediction_index}`;
  
  if (label === "none") return;
  
  if (!accumulatedText.value) {
    accumulatedText.value = label;
  } else if (!accumulatedText.value.endsWith(label)) {
    accumulatedText.value += " " + label;
  }
});

// --------- Start / Stop detection -----------
async function startDetection() {
  if (isDetecting.value) return;

  await nextTick();
  const videoEl = videoRef.value;
  const canvasEl = canvasRef.value;
  
  if (!videoEl || !canvasEl) return;

  const ctx = canvasEl.getContext("2d");
  ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);

  hands = new Hands({
    locateFile: (file) =>
      `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
  });
  hands.setOptions({
    maxNumHands: 2,
    modelComplexity: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
  });
  hands.onResults(onResults);

  await hands.initialize();

  mpCamera = new MediaPipeCamera(videoEl, {
    onFrame: async () => {
      if (!hands) return;
      await hands.send({ image: videoEl });
    },
    width: 640,
    height: 480,
  });

  await mpCamera.start();
  isDetecting.value = true;
  accumulatedText.value = "";
}

async function stopDetection() {
  if (!isDetecting.value) return;
  
  isDetecting.value = false;
  
  resetBuffer();
  
  if (mpCamera) {
    mpCamera.stop();
    mpCamera = null;
  }
  
  if (hands) {
    await hands.close();
    hands = null;
  }
  
  if (videoRef.value && videoRef.value.srcObject) {
    const tracks = videoRef.value.srcObject.getTracks();
    tracks.forEach((t) => t.stop());
    videoRef.value.srcObject = null;
  }
  
  const canvasEl = canvasRef.value;
  if (canvasEl) {
    const ctx = canvasEl.getContext("2d");
    ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
  }
}

function toggleDetection() {
  if (isDetecting.value) {
    stopDetection();
  } else {
    startDetection();
  }
}

// Cleanup on unmount
onUnmounted(() => {
  stopDetection();
});

// Expose method untuk dipanggil dari parent jika perlu
defineExpose({
  stopDetection
});
</script>
