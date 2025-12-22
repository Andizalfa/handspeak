<template>
  <div>
    <!-- Hero Section -->
    <section class="py-12 sm:py-16 lg:py-20 px-4 sm:px-6">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16 items-center">
          
          <div class="text-center lg:text-left order-2 lg:order-1">
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-gray-800 mb-4 sm:mb-6 leading-tight">
              Jembatan Komunikasi <br class="hidden lg:block"/> untuk Semua
            </h1>
            <p class="text-base sm:text-lg text-gray-600 mb-6 sm:mb-8 leading-relaxed max-w-lg mx-auto lg:mx-0">
              HandSpeak menggunakan kecerdasan buatan untuk menerjemahkan bahasa isyarat BISINDO ke teks secara real-time, membuka komunikasi tanpa batas.
            </p>
            
            <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center lg:justify-start">
              <button
                @click="$emit('scroll-to-camera')"
                class="px-6 py-3.5 text-white rounded-xl shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-300 hover:-translate-y-1 text-sm sm:text-base font-bold bg-gradient-to-r from-[#5B8FB9] to-[#4A7BA7]"
              >
                Mulai Sekarang
              </button>
              <button
                v-if="!isLoggedIn"
                @click="$router.push('/register')"
                class="px-6 py-3.5 bg-white text-[#5B8FB9] border-2 border-[#5B8FB9]/30 rounded-xl hover:border-[#5B8FB9] hover:bg-blue-50 transition-all duration-300 text-sm sm:text-base font-bold"
              >
                Buat Akun Gratis
              </button>
            </div>
          </div>

            <div class="hidden lg:block relative w-full max-w-md mx-auto lg:max-w-full order-1 lg:order-2">
                <div class="flex justify-center transform hover:scale-[1.02] transition-transform duration-500">
                    <img 
                    :src="gambarHero" 
                    alt="Sign Language Communication"
                    class="w-full h-auto object-contain max-h-[400px] lg:max-h-[500px] drop-shadow-2xl"
                    />
                </div>
            </div>
        </div>
      </div>
    </section>

    <!-- Statistics Section -->
    <section class="py-10 px-4 sm:px-6">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
          <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 text-center hover:shadow-xl transition-shadow">
            <div class="text-4xl sm:text-5xl font-bold mb-2 text-[#5B8FB9]">80%</div>
            <div class="text-gray-500 text-sm sm:text-base font-medium">Tingkat Akurasi</div>
          </div>
          <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 text-center hover:shadow-xl transition-shadow">
            <div class="text-4xl sm:text-5xl font-bold mb-2 text-[#64CCC5]">1000+</div>
            <div class="text-gray-500 text-sm sm:text-base font-medium">Pengguna Aktif</div>
          </div>
          <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 text-center hover:shadow-xl transition-shadow">
            <div class="text-4xl sm:text-5xl font-bold mb-2 text-[#FFD95A]">50</div>
            <div class="text-gray-500 text-sm sm:text-base font-medium">Kata BISINDO</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import gambarHero from "@/assets/gambar.png";

defineProps({
  isLoggedIn: Boolean
});

defineEmits(['scroll-to-camera']);
</script>