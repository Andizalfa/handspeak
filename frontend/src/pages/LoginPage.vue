<template>
  <div
    class="min-h-screen bg-gradient-to-b from-slate-50 to-slate-200 flex items-center justify-center px-4 py-8 sm:py-12"
  >
    <div class="w-full max-w-sm sm:max-w-md transition-all duration-300">
      
      <div class="text-center mb-6 sm:mb-8">
        <div
          class="inline-flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 rounded-2xl mb-4 shadow-lg shadow-[#91C4C3]/30 bg-[#91C4C3]"
        >
          <LogIn class="w-7 h-7 sm:w-8 sm:h-8 text-white" />
        </div>
        
        <h1 class="text-gray-800 text-2xl sm:text-3xl font-bold mb-2 tracking-tight">
          Masuk ke HandSpeak
        </h1>
        <p class="text-gray-500 text-sm sm:text-base px-2">
          Selamat datang kembali! Masuk untuk melanjutkan
        </p>
      </div>

      <div class="bg-white rounded-2xl sm:rounded-3xl shadow-xl shadow-slate-200/60 p-6 sm:p-8">
        
        <div
          v-if="errorMessage"
          class="mb-6 p-3 rounded-xl bg-red-50 border border-red-100 flex items-center justify-center gap-2 animate-pulse"
        >
          <span class="text-sm text-red-600 font-medium text-center">
            {{ errorMessage }}
          </span>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5 sm:space-y-6">
          <div class="group">
            <label
              for="email"
              class="block text-gray-700 mb-2 text-sm font-medium ml-1"
            >
              Email
            </label>
            <div class="relative transition-all duration-200 focus-within:scale-[1.01]">
              <div
                class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none"
              >
                <Mail class="w-5 h-5 text-gray-400 group-focus-within:text-[#64CCC5] transition-colors" />
              </div>
              <input
                type="email"
                id="email"
                v-model="formData.email"
                class="w-full pl-11 pr-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:bg-white focus:border-[#91C4C3] focus:ring-4 focus:ring-[#91C4C3]/10 transition-all"
                placeholder="nama@email.com"
                required
              />
            </div>
          </div>

          <div class="group">
            <label
              for="password"
              class="block text-gray-700 mb-2 text-sm font-medium ml-1"
            >
              Password
            </label>
            <div class="relative transition-all duration-200 focus-within:scale-[1.01]">
              <div
                class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none"
              >
                <Lock class="w-5 h-5 text-gray-400 group-focus-within:text-[#64CCC5] transition-colors" />
              </div>
              <input
                type="password"
                id="password"
                v-model="formData.password"
                class="w-full pl-11 pr-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:bg-white focus:border-[#91C4C3] focus:ring-4 focus:ring-[#91C4C3]/10 transition-all"
                placeholder="Masukkan password Anda"
                required
              />
            </div>
          </div>

          <div class="text-right mt-2">
            <button
              type="button"
              @click="showForgotPassword = true"
              class="text-sm text-[#64CCC5] hover:text-[#4FB8B0] hover:underline transition-colors"
            >
              Lupa Password?
            </button>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3.5 px-6 text-white rounded-xl shadow-lg shadow-[#64CCC5]/30 hover:shadow-xl hover:shadow-[#64CCC5]/40 transition-all duration-300 hover:-translate-y-0.5 active:scale-[0.98] mt-4 text-center disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none text-sm sm:text-base font-semibold bg-gradient-to-r from-[#64CCC5] to-[#4FB8B0]"
          >
            <div class="flex items-center justify-center gap-2">
                <span v-if="!loading">Masuk Sekarang</span>
                <span v-else class="flex items-center gap-2">
                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Memproses...
                </span>
            </div>
          </button>
        </form>

        <div class="mt-8 text-center">
          <p class="text-gray-500 text-sm sm:text-base">
            Belum punya akun?
            <RouterLink
              to="/register"
              class="font-semibold transition-colors hover:underline decoration-2 decoration-[#64CCC5]/50 hover:text-[#4FB8B0] text-[#64CCC5]"
            >
              Daftar di sini
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

    <!-- Modal Lupa Password -->
    <div
      v-if="showForgotPassword"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center px-4 z-50 animate-fadeIn"
      @click.self="closeForgotPasswordModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-6 sm:p-8 w-full max-w-md animate-slideUp">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl sm:text-2xl font-bold text-gray-800 flex items-center gap-2">
            <Shield class="w-6 h-6 text-[#64CCC5]" />
            Reset Password
          </h2>
          <button
            @click="closeForgotPasswordModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Progress Steps -->
        <div class="flex items-center justify-center mb-8">
          <div class="flex items-center gap-2">
            <!-- Step 1 -->
            <div class="flex flex-col items-center">
              <div
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all',
                  forgotPasswordStep >= 1
                    ? 'bg-[#64CCC5] text-white'
                    : 'bg-gray-200 text-gray-400',
                ]"
              >
                <Mail class="w-5 h-5" />
              </div>
              <span class="text-xs mt-1 text-gray-500">Email</span>
            </div>

            <!-- Separator -->
            <div
              :class="[
                'w-12 h-1 rounded transition-all',
                forgotPasswordStep >= 2 ? 'bg-[#64CCC5]' : 'bg-gray-200',
              ]"
            ></div>

            <!-- Step 2 -->
            <div class="flex flex-col items-center">
              <div
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all',
                  forgotPasswordStep >= 2
                    ? 'bg-[#64CCC5] text-white'
                    : 'bg-gray-200 text-gray-400',
                ]"
              >
                <Shield class="w-5 h-5" />
              </div>
              <span class="text-xs mt-1 text-gray-500">OTP</span>
            </div>

            <!-- Separator -->
            <div
              :class="[
                'w-12 h-1 rounded transition-all',
                forgotPasswordStep >= 3 ? 'bg-[#64CCC5]' : 'bg-gray-200',
              ]"
            ></div>

            <!-- Step 3 -->
            <div class="flex flex-col items-center">
              <div
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all',
                  forgotPasswordStep >= 3
                    ? 'bg-[#64CCC5] text-white'
                    : 'bg-gray-200 text-gray-400',
                ]"
              >
                <Lock class="w-5 h-5" />
              </div>
              <span class="text-xs mt-1 text-gray-500">Password</span>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div
          v-if="forgotPasswordError"
          class="mb-4 p-3 rounded-xl bg-red-50 border border-red-100 flex items-center gap-2"
        >
          <span class="text-sm text-red-600">{{ forgotPasswordError }}</span>
        </div>

        <!-- Step 1: Email -->
        <div v-if="forgotPasswordStep === 1" class="space-y-4">
          <p class="text-sm text-gray-600 mb-4">
            Masukkan email yang terdaftar untuk menerima kode OTP reset password
          </p>
          <div>
            <label class="block text-gray-700 mb-2 text-sm font-medium">
              Email
            </label>
            <input
              v-model="forgotPasswordEmail"
              type="email"
              class="w-full px-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm focus:outline-none focus:bg-white focus:border-[#91C4C3] focus:ring-4 focus:ring-[#91C4C3]/10 transition-all"
              placeholder="nama@email.com"
              required
            />
          </div>
          <button
            @click="handleForgotPasswordSendOTP"
            :disabled="forgotPasswordLoading"
            class="w-full py-3 px-6 text-white rounded-xl shadow-lg shadow-[#64CCC5]/30 hover:shadow-xl hover:shadow-[#64CCC5]/40 transition-all bg-gradient-to-r from-[#64CCC5] to-[#4FB8B0] disabled:opacity-70 disabled:cursor-not-allowed font-semibold"
          >
            <span v-if="!forgotPasswordLoading">Kirim Kode OTP</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Mengirim...
            </span>
          </button>
        </div>

        <!-- Step 2: OTP -->
        <div v-if="forgotPasswordStep === 2" class="space-y-4">
          <p class="text-sm text-gray-600 mb-4">
            Kode OTP telah dikirim ke <strong>{{ forgotPasswordEmail }}</strong>
          </p>
          <div>
            <label class="block text-gray-700 mb-2 text-sm font-medium">
              Kode OTP (6 digit)
            </label>
            <input
              v-model="forgotPasswordOTP"
              type="text"
              maxlength="6"
              class="w-full px-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm focus:outline-none focus:bg-white focus:border-[#91C4C3] focus:ring-4 focus:ring-[#91C4C3]/10 transition-all text-center text-2xl tracking-widest font-mono"
              placeholder="000000"
              required
            />
          </div>

          <!-- Countdown Timer -->
          <div class="text-center">
            <p class="text-sm text-gray-500">
              Kode berlaku: <span class="font-semibold text-[#64CCC5]">{{ formatCountdown }}</span>
            </p>
            <button
              v-if="forgotPasswordCountdown === 0"
              @click="handleForgotPasswordSendOTP"
              class="text-sm text-[#64CCC5] hover:text-[#4FB8B0] hover:underline mt-2 transition-colors"
            >
              Kirim ulang OTP
            </button>
          </div>

          <button
            @click="handleForgotPasswordVerifyOTP"
            :disabled="forgotPasswordLoading || forgotPasswordOTP.length !== 6"
            class="w-full py-3 px-6 text-white rounded-xl shadow-lg shadow-[#64CCC5]/30 hover:shadow-xl hover:shadow-[#64CCC5]/40 transition-all bg-gradient-to-r from-[#64CCC5] to-[#4FB8B0] disabled:opacity-70 disabled:cursor-not-allowed font-semibold"
          >
            <span v-if="!forgotPasswordLoading">Verifikasi OTP</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Memverifikasi...
            </span>
          </button>
        </div>

        <!-- Step 3: New Password -->
        <div v-if="forgotPasswordStep === 3" class="space-y-4">
          <p class="text-sm text-gray-600 mb-4">
            Masukkan password baru untuk akun Anda
          </p>
          <div>
            <label class="block text-gray-700 mb-2 text-sm font-medium">
              Password Baru
            </label>
            <input
              v-model="forgotPasswordNewPassword"
              type="password"
              class="w-full px-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm focus:outline-none focus:bg-white focus:border-[#91C4C3] focus:ring-4 focus:ring-[#91C4C3]/10 transition-all"
              placeholder="Minimal 6 karakter"
              required
            />
          </div>
          <div>
            <label class="block text-gray-700 mb-2 text-sm font-medium">
              Konfirmasi Password Baru
            </label>
            <input
              v-model="forgotPasswordConfirmPassword"
              type="password"
              class="w-full px-4 py-3 border-2 border-gray-100 bg-gray-50 rounded-xl text-gray-800 placeholder-gray-400 text-sm focus:outline-none focus:bg-white focus:border-[#91C4C3] focus:ring-4 focus:ring-[#91C4C3]/10 transition-all"
              placeholder="Ulangi password baru"
              required
            />
          </div>
          <button
            @click="handleForgotPasswordReset"
            :disabled="forgotPasswordLoading || forgotPasswordNewPassword.length < 6 || forgotPasswordNewPassword !== forgotPasswordConfirmPassword"
            class="w-full py-3 px-6 text-white rounded-xl shadow-lg shadow-[#64CCC5]/30 hover:shadow-xl hover:shadow-[#64CCC5]/40 transition-all bg-gradient-to-r from-[#64CCC5] to-[#4FB8B0] disabled:opacity-70 disabled:cursor-not-allowed font-semibold"
          >
            <span v-if="!forgotPasswordLoading">Reset Password</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Mereset...
            </span>
          </button>
          <p v-if="forgotPasswordNewPassword !== forgotPasswordConfirmPassword && forgotPasswordConfirmPassword.length > 0" class="text-sm text-red-600 text-center">
            Password tidak cocok
          </p>
        </div>
      </div>
    </div>

    <!-- Modal Sukses Reset Password -->
    <div
      v-if="showResetSuccess"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center px-4 z-50 animate-fadeIn"
      @click.self="closeResetSuccessModal"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-6 sm:p-8 w-full max-w-md animate-slideUp text-center">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-4">
          <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 class="text-xl sm:text-2xl font-bold text-gray-800 mb-3">
          Password Berhasil Direset!
        </h3>
        <p class="text-gray-600 mb-6">
          Password Anda telah berhasil diubah. Silakan login dengan password baru Anda.
        </p>
        <button
          @click="closeResetSuccessModal"
          class="w-full py-3 px-6 text-white rounded-xl shadow-lg shadow-[#64CCC5]/30 hover:shadow-xl hover:shadow-[#64CCC5]/40 transition-all bg-gradient-to-r from-[#64CCC5] to-[#4FB8B0] font-semibold"
        >
          OK, Mengerti
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { LogIn, Mail, Lock, Shield } from "lucide-vue-next";

const router = useRouter();

const formData = ref({
  email: "",
  password: "",
});

const loading = ref(false);
const errorMessage = ref("");

// Forgot Password
const showForgotPassword = ref(false);
const forgotPasswordStep = ref(1);
const forgotPasswordEmail = ref("");
const forgotPasswordOTP = ref("");
const forgotPasswordNewPassword = ref("");
const forgotPasswordConfirmPassword = ref("");
const forgotPasswordLoading = ref(false);
const forgotPasswordError = ref("");
const forgotPasswordCountdown = ref(0);
let forgotPasswordTimer = null;

// Success Modal
const showResetSuccess = ref(false);

const API_BASE = "http://127.0.0.1:8001";

async function handleLogin() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: formData.value.email,
        password: formData.value.password,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Login gagal");
    }

    // simpan token
    localStorage.setItem("access_token", data.access_token);

    // pindah ke home
    router.push("/");
  } catch (err) {
    errorMessage.value = err.message || "Terjadi kesalahan.";
  } finally {
    loading.value = false;
  }
}

// Forgot Password Functions
function closeForgotPasswordModal() {
  showForgotPassword.value = false;
  forgotPasswordStep.value = 1;
  forgotPasswordEmail.value = "";
  forgotPasswordOTP.value = "";
  forgotPasswordNewPassword.value = "";
  forgotPasswordConfirmPassword.value = "";
  forgotPasswordError.value = "";
  forgotPasswordCountdown.value = 0;
  if (forgotPasswordTimer) {
    clearInterval(forgotPasswordTimer);
    forgotPasswordTimer = null;
  }
}

function startForgotPasswordCountdown() {
  forgotPasswordCountdown.value = 300; // 5 menit
  if (forgotPasswordTimer) {
    clearInterval(forgotPasswordTimer);
  }
  forgotPasswordTimer = setInterval(() => {
    forgotPasswordCountdown.value--;
    if (forgotPasswordCountdown.value <= 0) {
      clearInterval(forgotPasswordTimer);
      forgotPasswordTimer = null;
    }
  }, 1000);
}

const formatCountdown = computed(() => {
  const minutes = Math.floor(forgotPasswordCountdown.value / 60);
  const seconds = forgotPasswordCountdown.value % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
});

async function handleForgotPasswordSendOTP() {
  if (!forgotPasswordEmail.value) {
    forgotPasswordError.value = "Masukkan email Anda";
    return;
  }

  forgotPasswordLoading.value = true;
  forgotPasswordError.value = "";

  try {
    console.log("🔐 Sending forgot password OTP to:", forgotPasswordEmail.value);
    
    const res = await fetch(`${API_BASE}/auth/forgot-password/send-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: forgotPasswordEmail.value }),
    });

    const data = await res.json();
    console.log("📧 OTP Response:", data);

    if (!res.ok) {
      throw new Error(data.detail || "Gagal mengirim OTP");
    }

    // Pindah ke step 2 (OTP)
    forgotPasswordStep.value = 2;
    startForgotPasswordCountdown();
    console.log("✅ OTP sent, moved to step 2");
  } catch (err) {
    console.error("❌ Error sending OTP:", err);
    forgotPasswordError.value = err.message || "Gagal mengirim OTP";
  } finally {
    forgotPasswordLoading.value = false;
  }
}

async function handleForgotPasswordVerifyOTP() {
  if (forgotPasswordOTP.value.length !== 6) {
    forgotPasswordError.value = "Masukkan kode OTP 6 digit";
    return;
  }

  forgotPasswordLoading.value = true;
  forgotPasswordError.value = "";

  try {
    console.log("🔐 Verifying OTP:", forgotPasswordOTP.value);
    
    // Langsung ke step 3 tanpa verifikasi dulu (verifikasi di step reset)
    forgotPasswordStep.value = 3;
    console.log("✅ Moved to step 3 (new password)");
  } catch (err) {
    console.error("❌ Error:", err);
    forgotPasswordError.value = err.message || "Terjadi kesalahan";
  } finally {
    forgotPasswordLoading.value = false;
  }
}

async function handleForgotPasswordReset() {
  if (forgotPasswordNewPassword.value.length < 6) {
    forgotPasswordError.value = "Password minimal 6 karakter";
    return;
  }

  if (forgotPasswordNewPassword.value !== forgotPasswordConfirmPassword.value) {
    forgotPasswordError.value = "Password tidak cocok";
    return;
  }

  forgotPasswordLoading.value = true;
  forgotPasswordError.value = "";

  try {
    console.log("🔐 Resetting password for:", forgotPasswordEmail.value);
    
    const res = await fetch(`${API_BASE}/auth/forgot-password/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: forgotPasswordEmail.value,
        otp: forgotPasswordOTP.value,
        new_password: forgotPasswordNewPassword.value,
      }),
    });

    const data = await res.json();
    console.log("✅ Reset Response:", data);

    if (!res.ok) {
      throw new Error(data.detail || "Gagal reset password");
    }

    // Sukses reset password
    closeForgotPasswordModal();
    showResetSuccess.value = true;
    console.log("✅ Password reset successful");
  } catch (err) {
    console.error("❌ Error resetting password:", err);
    forgotPasswordError.value = err.message || "Gagal reset password";
  } finally {
    forgotPasswordLoading.value = false;
  }
}

function closeResetSuccessModal() {
  showResetSuccess.value = false;
}

// Cleanup on unmount
onUnmounted(() => {
  if (forgotPasswordTimer) {
    clearInterval(forgotPasswordTimer);
  }
});
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.2s ease-out;
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}
</style>