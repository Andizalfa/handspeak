<template>
  <section class="py-16 sm:py-20 px-4 sm:px-6 bg-white/50">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-10 sm:mb-16">
        <h2 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-800 mb-3 sm:mb-4">
          Kenapa Memilih HandSpeak?
        </h2>
        <p class="text-base sm:text-lg text-gray-500 max-w-2xl mx-auto">
          Platform terdepan dalam teknologi penerjemahan bahasa isyarat dengan berbagai keunggulan
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
        <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100 h-full">
          <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center mb-6 bg-gradient-to-br from-[#64CCC5] to-[#4FB8B0] shadow-lg shadow-teal-500/20">
            <Camera class="w-7 h-7 sm:w-8 sm:h-8 text-white" />
          </div>
          <h3 class="text-lg sm:text-xl font-bold text-gray-800 mb-3">Real-Time Translation</h3>
          <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
            Deteksi gerakan bahasa isyarat BISINDO secara langsung menggunakan kamera dengan akurasi tinggi.
          </p>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100 h-full">
          <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center mb-6 bg-gradient-to-br from-[#FFD95A] to-[#FFC830] shadow-lg shadow-yellow-500/20">
            <Zap class="w-7 h-7 sm:w-8 sm:h-8 text-gray-800" />
          </div>
          <h3 class="text-lg sm:text-xl font-bold text-gray-800 mb-3">Cepat & Akurat</h3>
          <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
            Teknologi machine learning terkini memberikan hasil terjemahan dalam hitungan milidetik.
          </p>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100 h-full">
          <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center mb-6 bg-gradient-to-br from-[#5B8FB9] to-[#4A7BA7] shadow-lg shadow-blue-500/20">
            <History class="w-7 h-7 sm:w-8 sm:h-8 text-white" />
          </div>
          <h3 class="text-lg sm:text-xl font-bold text-gray-800 mb-3">Riwayat Lengkap</h3>
          <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
            Simpan dan akses kembali semua kata yang pernah diterjemahkan kapan saja.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { Camera, Zap, History } from "lucide-vue-next";
</script>