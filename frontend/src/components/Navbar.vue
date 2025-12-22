<template>
  <header class="sticky top-0 z-50 shadow-lg" :class="headerClass">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3">
      <div class="flex items-center justify-between">
        
        <div 
          class="flex items-center gap-2 sm:gap-3 cursor-pointer group" 
          @click="scrollToTop"
        >
          <div
            class="flex items-center justify-center w-8 h-8 sm:w-10 sm:h-10 rounded-lg shadow-lg group-hover:scale-105 transition-transform"
            :class="logoClass"
          >
            <Hand class="w-4 h-4 sm:w-5 sm:h-5" :class="logoIconClass" />
          </div>
          <div>
            <h1 class="text-white text-base sm:text-lg font-bold tracking-wide leading-tight">HandSpeak</h1>
            <p class="text-white/90 text-[10px] sm:text-xs font-light hidden sm:block">
              Penerjemah BISINDO Real-time
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2 sm:gap-3">
          <!-- Mode History Page: Tombol Kembali -->
          <template v-if="mode === 'history'">
            <button
              @click="$emit('back')"
              class="group flex items-center gap-2 px-3 py-2 sm:px-4 sm:py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all duration-200 border border-white/20 backdrop-blur-sm"
            >
              <ArrowLeft class="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
              <span class="text-xs sm:text-sm font-medium hidden sm:inline">Kembali</span>
            </button>
          </template>

          <!-- Mode Home Page: Tombol Login/Register/History/Logout -->
          <template v-else>
            <template v-if="isLoggedIn">
              <button
                @click="$router.push('/history')"
                class="flex items-center gap-2 px-3 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all duration-200 backdrop-blur-sm"
              >
                <History class="w-4 h-4" />
                <span class="text-sm font-medium hidden sm:inline">Riwayat</span>
              </button>
              
              <button
                @click="$emit('logout')"
                class="flex items-center gap-2 px-3 py-2 bg-white text-[#4A7BA7] hover:bg-slate-100 rounded-lg shadow-md transition-all duration-200"
              >
                <LogOut class="w-4 h-4" />
                <span class="text-sm font-medium hidden sm:inline">Keluar</span>
              </button>
            </template>

            <template v-else>
              <button
                @click="$router.push('/register')"
                class="px-3 py-2 text-white hover:bg-white/10 rounded-lg transition-all duration-200 text-xs sm:text-sm font-medium"
              >
                Daftar
              </button>
              <button
                @click="$router.push('/login')"
                class="px-4 py-2 bg-white text-[#5B8FB9] hover:bg-slate-50 rounded-lg shadow-md transition-all duration-200 text-xs sm:text-sm font-bold"
              >
                Masuk
              </button>
            </template>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from "vue";
import { Hand, History, LogOut, ArrowLeft } from "lucide-vue-next";

const props = defineProps({
  isLoggedIn: Boolean,
  mode: {
    type: String,
    default: 'home', // 'home' atau 'history'
    validator: (value) => ['home', 'history'].includes(value)
  }
});

defineEmits(['logout', 'back']);

const headerClass = computed(() => {
  if (props.mode === 'history') {
    return 'bg-[#80A1BA]';
  }
  return 'bg-gradient-to-r from-[#5B8FB9] to-[#4A7BA7]';
});

const logoClass = computed(() => {
  if (props.mode === 'history') {
    return 'bg-white';
  }
  return 'bg-gradient-to-br from-[#FFD95A] to-[#FFC830]';
});

const logoIconClass = computed(() => {
  if (props.mode === 'history') {
    return 'text-[#80A1BA]';
  }
  return 'text-gray-800';
});

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
</script>