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
          <div class="flex items-start gap-4 mb-4">
            <div class="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center bg-gradient-to-br from-[#64CCC5] to-[#4FB8B0] shadow-lg shadow-teal-500/20 flex-shrink-0">
              <Camera class="w-6 h-6 sm:w-7 sm:h-7 text-white" />
            </div>
            <h3 class="text-lg sm:text-xl font-bold text-gray-800 pt-2">Real-Time Translation</h3>
          </div>
          <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
            Deteksi gerakan bahasa isyarat BISINDO secara langsung menggunakan kamera dengan akurasi tinggi.
          </p>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100 h-full">
          <div class="flex items-start gap-4 mb-4">
            <div class="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center bg-gradient-to-br from-[#FFD95A] to-[#FFC830] shadow-lg shadow-yellow-500/20 flex-shrink-0">
              <Zap class="w-6 h-6 sm:w-7 sm:h-7 text-gray-800" />
            </div>
            <h3 class="text-lg sm:text-xl font-bold text-gray-800 pt-2">Cepat & Akurat</h3>
          </div>
          <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
            Teknologi machine learning terkini memberikan hasil terjemahan dalam hitungan milidetik.
          </p>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-6 sm:p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100 h-full">
          <div class="flex items-start gap-4 mb-4">
            <div class="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center bg-gradient-to-br from-[#5B8FB9] to-[#4A7BA7] shadow-lg shadow-blue-500/20 flex-shrink-0">
              <History class="w-6 h-6 sm:w-7 sm:h-7 text-white" />
            </div>
            <h3 class="text-lg sm:text-xl font-bold text-gray-800 pt-2">Riwayat Lengkap</h3>
          </div>
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