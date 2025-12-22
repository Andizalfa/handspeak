<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-200">
    
    <!-- Navbar Component -->
    <Navbar 
      :isLoggedIn="isLoggedIn" 
      @logout="showLogoutDialog = true"
    />

    <!-- Hero Section Component -->
    <Herosection 
      :isLoggedIn="isLoggedIn"
      @scroll-to-camera="scrollToCamera"
    />

    <!-- Keunggulan Component -->
    <Keunggulan />

    <!-- Mulai Coba Component -->
    <Mulaicoba ref="mulaicobaRef" />

    <!-- Logout Dialog -->
    <div
      v-if="showLogoutDialog"
      class="fixed inset-0 flex items-center justify-center z-[999] px-4"
    >
      <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity" @click="showLogoutDialog = false"></div>
      
      <div
        class="bg-white rounded-2xl shadow-2xl p-6 sm:p-8 max-w-sm w-full mx-auto relative z-10 transform transition-all scale-100"
      >
        <div class="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-4">
            <LogOut class="w-6 h-6 text-red-500" />
        </div>
        <h3 class="text-gray-800 text-center text-xl font-bold mb-2">
          Keluar dari Akun?
        </h3>
        <p class="text-gray-500 text-center text-sm mb-8 leading-relaxed">
          Sesi Anda akan berakhir. Anda perlu login kembali untuk mengakses riwayat.
        </p>
        <div class="flex gap-3">
          <button
            @click="showLogoutDialog = false"
            class="flex-1 py-2.5 px-4 border border-gray-300 rounded-xl text-gray-700 font-medium hover:bg-gray-50 transition-colors"
          >
            Batal
          </button>
          <button
            @click="handleLogoutConfirm"
            class="flex-1 py-2.5 px-4 text-white rounded-xl shadow-lg shadow-red-500/30 hover:shadow-red-500/40 transition-all font-medium bg-gradient-to-r from-red-500 to-red-600"
          >
            Ya, Keluar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { LogOut } from "lucide-vue-next";
import { isLoggedIn as checkLoggedIn } from "@/api/apiClient";

// Import Components
import Navbar from "@/components/Navbar.vue";
import Herosection from "@/components/Herosection.vue";
import Keunggulan from "@/components/Keunggulan.vue";
import Mulaicoba from "@/components/Mulaicoba.vue";

const router = useRouter();
const mulaicobaRef = ref(null);

// Check login status
const isLoggedIn = ref(checkLoggedIn());

// UI state
const showLogoutDialog = ref(false);

// --------- Scroll functions -----------
function scrollToCamera() {
  const section = document.getElementById('camera-section');
  if (section) {
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// --------- Logout & cleanup -----------
function handleLogoutConfirm() {
  showLogoutDialog.value = false;
  localStorage.removeItem("access_token");
  isLoggedIn.value = false;
  
  // Stop detection di Mulaicoba component
  if (mulaicobaRef.value) {
    mulaicobaRef.value.stopDetection();
  }
  
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Lifecycle hooks
onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'instant' });
  isLoggedIn.value = checkLoggedIn();
});
</script>