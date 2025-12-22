<template>
  <div
    class="min-h-screen bg-gradient-to-b from-slate-50 to-slate-200 flex items-center justify-center px-4 py-8 sm:py-12"
  >
    <div class="w-full max-w-sm sm:max-w-md transition-all duration-300">
      
      <div class="text-center mb-6 sm:mb-8">
        <div
          class="inline-flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 rounded-2xl mb-4 shadow-lg shadow-[#80A1BA]/30 bg-[#80A1BA]"
        >
          <UserPlus class="w-7 h-7 sm:w-8 sm:h-8 text-white" />
        </div>
        
        <h1 class="text-gray-800 text-2xl sm:text-3xl font-bold mb-2 tracking-tight">
          Daftar Akun HandSpeak
        </h1>
        <p class="text-gray-500 text-sm sm:text-base px-2">
          {{ stepDescription }}
        </p>
      </div>

      <div class="bg-white rounded-2xl sm:rounded-3xl shadow-xl shadow-slate-200/60 p-6 sm:p-8">
        
        <!-- Progress Steps -->
        <div class="flex items-center justify-center mb-6 sm:mb-8">
          <div class="flex items-center gap-2">
            <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all', currentStep >= 1 ? 'bg-[#5B8FB9] text-white' : 'bg-gray-200 text-gray-400']">
              1
            </div>
            <div :class="['h-1 w-8 sm:w-12 transition-all', currentStep >= 2 ? 'bg-[#5B8FB9]' : 'bg-gray-200']"></div>
            <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all', currentStep >= 2 ? 'bg-[#5B8FB9] text-white' : 'bg-gray-200 text-gray-400']">
              2
            </div>
            <div :class="['h-1 w-8 sm:w-12 transition-all', currentStep >= 3 ? 'bg-[#5B8FB9]' : 'bg-gray-200']"></div>
            <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all', currentStep >= 3 ? 'bg-[#5B8FB9] text-white' : 'bg-gray-200 text-gray-400']">
              3
            </div>
          </div>
        </div>

        <div
          v-if="errorMessage"
          class="mb-6 p-3 rounded-xl bg-red-50 border border-red-100 flex items-center justify-center gap-2 animate-pulse"
        >
          <span class="text-sm text-red-600 font-medium text-center">
            {{ errorMessage }}
          </span>
        </div>

        <div
          v-if="successMessage"
          class="mb-6 p-3 rounded-xl bg-green-50 border border-green-100 flex items-center justify-center gap-2"
        >
          <CheckCircle class="w-5 h-5 text-green-600" />
          <span class="text-sm text-green-600 font-medium text-center">
            {{ successMessage }}
          </span>
        </div>

        <!-- Step 1: Input Email -->
        <form v-if="currentStep === 1" @submit.prevent="handleSendOTP" class="space-y-4 sm:space-y-5">
          
          <!-- Warning Box -->
          <div class="flex items-start gap-3 p-4 rounded-xl bg-amber-50 border-2 border-amber-200">
            <AlertTriangle class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p class="text-amber-900 font-semibold text-sm mb-1">Penting!</p>
              <p class="text-amber-800 text-xs sm:text-sm leading-relaxed">
                Gunakan email <strong>AKTIF dan TERDAFTAR</strong> (Gmail/Yahoo/Outlook). 
                OTP hanya dikirim ke email yang valid dan dapat menerima pesan.
              </p>
            </div>
          </div>

          <div class="group">
            <label for="email" class="block text-gray-700 mb-2 text-sm font-medium ml-1">
              Email
            </label>
            <div class="relative transition-all duration-200 focus-within:scale-[1.01]">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Mail class="w-5 h-5 text-gray-400 group-focus-within:text-[#5B8FB9] transition-colors" />
              </div>
              <input
                type="email"
                id="email"
                v-model="formData.email"
                class="w-full pl-11 pr-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:bg-white focus:border-[#80A1BA] focus:ring-4 focus:ring-[#80A1BA]/10 transition-all"
                placeholder="nama@email.com"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3.5 px-6 text-white rounded-xl shadow-lg shadow-[#5B8FB9]/30 hover:shadow-xl hover:shadow-[#5B8FB9]/40 transition-all duration-300 hover:-translate-y-0.5 active:scale-[0.98] mt-6 text-center disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none text-sm sm:text-base font-semibold bg-gradient-to-r from-[#5B8FB9] to-[#4A7BA7]"
          >
            <div class="flex items-center justify-center gap-2">
              <span v-if="!loading">Kirim Kode OTP</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Mengirim...
              </span>
            </div>
          </button>
        </form>

        <!-- Step 2: Input OTP -->
        <form v-if="currentStep === 2" @submit.prevent="handleVerifyOTP" class="space-y-4 sm:space-y-5">
          <div class="text-center mb-4">
            <p class="text-gray-600 text-sm">
              Kode OTP telah dikirim ke
            </p>
            <p class="text-[#5B8FB9] font-semibold">{{ formData.email }}</p>
          </div>

          <div class="group">
            <label for="otp" class="block text-gray-700 mb-2 text-sm font-medium ml-1">
              Kode OTP
            </label>
            <div class="relative transition-all duration-200 focus-within:scale-[1.01]">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Shield class="w-5 h-5 text-gray-400 group-focus-within:text-[#5B8FB9] transition-colors" />
              </div>
              <input
                type="text"
                id="otp"
                v-model="formData.otp"
                maxlength="6"
                class="w-full pl-11 pr-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:bg-white focus:border-[#80A1BA] focus:ring-4 focus:ring-[#80A1BA]/10 transition-all text-center tracking-widest font-bold text-2xl"
                placeholder="000000"
                required
                @input="formatOTPInput"
              />
            </div>
          </div>

          <div class="text-center">
            <p class="text-gray-500 text-sm mb-2">
              Kode akan kadaluarsa dalam <span class="font-bold text-red-500">{{ formatTime(timeRemaining) }}</span>
            </p>
            <button
              v-if="timeRemaining === 0"
              @click="handleSendOTP"
              type="button"
              class="text-[#5B8FB9] hover:text-[#4A7BA7] font-semibold text-sm underline"
            >
              Kirim Ulang Kode OTP
            </button>
          </div>

          <div class="flex gap-3">
            <button
              type="button"
              @click="currentStep = 1"
              class="flex-1 py-3 px-4 border-2 border-gray-300 rounded-xl text-gray-700 font-medium hover:bg-gray-50 transition-colors"
            >
              Kembali
            </button>
            <button
              type="submit"
              :disabled="loading || formData.otp.length !== 6"
              class="flex-1 py-3 px-4 text-white rounded-xl shadow-lg shadow-[#5B8FB9]/30 hover:shadow-xl hover:shadow-[#5B8FB9]/40 transition-all duration-300 hover:-translate-y-0.5 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none text-sm font-semibold bg-gradient-to-r from-[#5B8FB9] to-[#4A7BA7]"
            >
              <span v-if="!loading">Verifikasi</span>
              <span v-else>Memverifikasi...</span>
            </button>
          </div>
        </form>

        <!-- Step 3: Complete Registration -->
        <form v-if="currentStep === 3" @submit.prevent="handleRegister" class="space-y-4 sm:space-y-5">
          <div class="group">
            <label for="fullName" class="block text-gray-700 mb-2 text-sm font-medium ml-1">
              Nama Lengkap
            </label>
            <div class="relative transition-all duration-200 focus-within:scale-[1.01]">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <User class="w-5 h-5 text-gray-400 group-focus-within:text-[#5B8FB9] transition-colors" />
              </div>
              <input
                type="text"
                id="fullName"
                v-model="formData.fullName"
                class="w-full pl-11 pr-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:bg-white focus:border-[#80A1BA] focus:ring-4 focus:ring-[#80A1BA]/10 transition-all"
                placeholder="Masukkan nama lengkap"
                required
              />
            </div>
          </div>

          <div class="group">
            <label for="password" class="block text-gray-700 mb-2 text-sm font-medium ml-1">
              Password
            </label>
            <div class="relative transition-all duration-200 focus-within:scale-[1.01]">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Lock class="w-5 h-5 text-gray-400 group-focus-within:text-[#5B8FB9] transition-colors" />
              </div>
              <input
                type="password"
                id="password"
                v-model="formData.password"
                class="w-full pl-11 pr-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:bg-white focus:border-[#80A1BA] focus:ring-4 focus:ring-[#80A1BA]/10 transition-all"
                placeholder="Minimal 6 karakter"
                required
                minlength="6"
              />
            </div>
          </div>

          <div class="group">
            <label for="confirmPassword" class="block text-gray-700 mb-2 text-sm font-medium ml-1">
              Konfirmasi Password
            </label>
            <div class="relative transition-all duration-200 focus-within:scale-[1.01]">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Lock class="w-5 h-5 text-gray-400 group-focus-within:text-[#5B8FB9] transition-colors" />
              </div>
              <input
                type="password"
                id="confirmPassword"
                v-model="formData.confirmPassword"
                class="w-full pl-11 pr-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:bg-white focus:border-[#80A1BA] focus:ring-4 focus:ring-[#80A1BA]/10 transition-all"
                placeholder="Ulangi password Anda"
                required
                minlength="6"
              />
            </div>
          </div>

          <div class="flex gap-3">
            <button
              type="button"
              @click="currentStep = 2"
              class="flex-1 py-3 px-4 border-2 border-gray-300 rounded-xl text-gray-700 font-medium hover:bg-gray-50 transition-colors"
            >
              Kembali
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 py-3 px-4 text-white rounded-xl shadow-lg shadow-[#5B8FB9]/30 hover:shadow-xl hover:shadow-[#5B8FB9]/40 transition-all duration-300 hover:-translate-y-0.5 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none text-sm font-semibold bg-gradient-to-r from-[#5B8FB9] to-[#4A7BA7]"
            >
              <div class="flex items-center justify-center gap-2">
                <span v-if="!loading">Daftar Sekarang</span>
                <span v-else class="flex items-center gap-2">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Memproses...
                </span>
              </div>
            </button>
          </div>
        </form>

        <div class="mt-8 text-center">
          <p class="text-gray-500 text-sm sm:text-base">
            Sudah punya akun?
            <RouterLink
              to="/login"
              class="font-semibold transition-colors hover:underline decoration-2 decoration-[#5B8FB9]/50 hover:text-[#4A7BA7] text-[#5B8FB9]"
            >
              Masuk di sini
            </RouterLink>
          </p>
        </div>
      </div>

      <div class="text-center mt-8">
        <p class="text-slate-400 text-xs sm:text-sm">
          © 2025 HandSpeak. Memudahkan komunikasi untuk semua.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { UserPlus, Mail, Lock, User, Shield, CheckCircle, AlertTriangle } from "lucide-vue-next";

const router = useRouter();

const currentStep = ref(1); // 1: Email, 2: OTP, 3: Complete Registration
const formData = ref({
  email: "",
  otp: "",
  fullName: "",
  password: "",
  confirmPassword: "",
});

const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const timeRemaining = ref(300); // 5 minutes in seconds
let countdownInterval = null;

const API_BASE = "http://127.0.0.1:8001";

const stepDescription = computed(() => {
  switch (currentStep.value) {
    case 1:
      return "Masukkan email Anda untuk verifikasi";
    case 2:
      return "Masukkan kode OTP yang dikirim ke email";
    case 3:
      return "Lengkapi data untuk menyelesaikan pendaftaran";
    default:
      return "";
  }
});

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function startCountdown() {
  // Reset countdown
  timeRemaining.value = 300; // 5 minutes
  
  // Clear existing interval
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
  
  // Start new countdown
  countdownInterval = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--;
    } else {
      clearInterval(countdownInterval);
    }
  }, 1000);
}

function formatOTPInput(event) {
  // Only allow numbers
  formData.value.otp = event.target.value.replace(/[^0-9]/g, '');
}

async function handleSendOTP() {
  if (!formData.value.email) {
    errorMessage.value = "Email harus diisi.";
    return;
  }

  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    console.log('🔄 Sending OTP request to:', formData.value.email);
    
    const res = await fetch(`${API_BASE}/auth/send-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: formData.value.email,
      }),
    });

    console.log('📥 Response status:', res.status);
    const data = await res.json();
    console.log('📦 Response data:', data);

    if (!res.ok) {
      throw new Error(data.detail || "Gagal mengirim OTP");
    }

    successMessage.value = "Kode OTP telah dikirim ke email Anda! Cek inbox atau folder spam.";
    currentStep.value = 2;
    formData.value.otp = ""; // Reset OTP
    
    // Start countdown timer
    startCountdown();
    
    console.log('✅ OTP sent successfully');
    
  } catch (err) {
    console.error('❌ Error sending OTP:', err);
    errorMessage.value = err.message || "Terjadi kesalahan saat mengirim OTP. Pastikan email valid dan coba lagi.";
  } finally {
    loading.value = false;
  }
}

async function handleVerifyOTP() {
  if (formData.value.otp.length !== 6) {
    errorMessage.value = "Kode OTP harus 6 digit.";
    return;
  }

  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    const res = await fetch(`${API_BASE}/auth/verify-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: formData.value.email,
        otp: formData.value.otp,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Kode OTP tidak valid");
    }

    successMessage.value = "Email berhasil diverifikasi!";
    currentStep.value = 3;
    
    // Stop countdown
    if (countdownInterval) {
      clearInterval(countdownInterval);
    }
    
  } catch (err) {
    errorMessage.value = err.message || "Terjadi kesalahan.";
  } finally {
    loading.value = false;
  }
}

async function handleRegister() {
  // Validasi password
  if (formData.value.password !== formData.value.confirmPassword) {
    errorMessage.value = "Password dan konfirmasi password tidak cocok.";
    return;
  }

  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: formData.value.fullName,
        email: formData.value.email,
        password: formData.value.password,
        otp: formData.value.otp,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Registrasi gagal");
    }

    // Berhasil registrasi, redirect ke login
    successMessage.value = "Registrasi berhasil! Mengalihkan ke halaman login...";
    
    setTimeout(() => {
      router.push("/login");
    }, 1500);
    
  } catch (err) {
    errorMessage.value = err.message || "Terjadi kesalahan.";
  } finally {
    loading.value = false;
  }
}

// Cleanup on unmount
onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
});
</script>