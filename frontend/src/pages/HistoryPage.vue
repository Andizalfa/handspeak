<template>
  <div class="min-h-screen bg-slate-50 font-sans">
    
    <!-- Navbar Component -->
    <Navbar 
      mode="history"
      @back="goHome"
    />

    <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 sm:py-8">
      
      <div class="bg-white rounded-2xl shadow-xl shadow-slate-200/60 p-5 sm:p-8 min-h-[500px]">
        
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-[#80A1BA]/10 rounded-lg">
                <HistoryIcon class="w-6 h-6 text-[#80A1BA]" />
            </div>
            <div>
                <h2 class="text-gray-800 text-xl font-bold">Riwayat Penerjemahan</h2>
                <p class="text-gray-500 text-xs sm:text-sm">Daftar aktivitas terjemahan Anda</p>
            </div>
          </div>

          <div v-if="histories.length > 0" class="w-full sm:w-auto">
            <button
              @click="showDeleteDialog = true"
              class="w-full sm:w-auto flex items-center justify-center gap-2 px-4 py-2.5 text-white rounded-xl shadow-lg shadow-red-500/20 hover:shadow-red-500/30 transition-all duration-200 hover:-translate-y-0.5 text-sm font-medium bg-gradient-to-r from-red-500 to-red-600"
            >
              <Trash2 class="w-4 h-4" />
              Hapus Semua Riwayat
            </button>
          </div>
        </div>

        <!-- Delete Confirmation Dialog -->
        <div
          v-if="showDeleteDialog"
          class="fixed inset-0 flex items-center justify-center z-[999] px-4"
        >
          <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity" @click="showDeleteDialog = false"></div>
          
          <div class="bg-white rounded-2xl shadow-2xl p-6 sm:p-8 max-w-sm w-full mx-auto relative z-10 transform transition-all scale-100">
            <div class="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-4">
              <Trash2 class="w-6 h-6 text-red-500" />
            </div>
            <h3 class="text-gray-800 text-center text-xl font-bold mb-2">
              Hapus Semua Riwayat?
            </h3>
            <p class="text-gray-500 text-center text-sm mb-8 leading-relaxed">
              Semua data riwayat penerjemahan akan dihapus permanen dari database. Tindakan ini tidak dapat dibatalkan.
            </p>
            <div class="flex gap-3">
              <button
                @click="showDeleteDialog = false"
                class="flex-1 py-2.5 px-4 border border-gray-300 rounded-xl text-gray-700 font-medium hover:bg-gray-50 transition-colors"
              >
                Batal
              </button>
              <button
                @click="confirmDelete"
                class="flex-1 py-2.5 px-4 text-white rounded-xl shadow-lg shadow-red-500/30 hover:shadow-red-500/40 transition-all font-medium bg-gradient-to-r from-red-500 to-red-600"
              >
                Ya, Hapus
              </button>
            </div>
          </div>
        </div>

        <!-- Success Notification -->
        <div
          v-if="showSuccessNotification"
          class="fixed inset-0 flex items-center justify-center z-[999] px-4"
        >
          <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity" @click="showSuccessNotification = false"></div>
          
          <div class="bg-white rounded-2xl shadow-2xl p-6 sm:p-8 max-w-sm w-full mx-auto relative z-10 transform transition-all scale-100">
            <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
              <CheckCircle class="w-6 h-6 text-green-500" />
            </div>
            <h3 class="text-gray-800 text-center text-xl font-bold mb-2">
              Berhasil!
            </h3>
            <p class="text-gray-500 text-center text-sm mb-6 leading-relaxed">
              {{ successMessage }}
            </p>
            <button
              @click="showSuccessNotification = false"
              class="w-full py-2.5 px-4 text-white rounded-xl shadow-lg shadow-green-500/30 hover:shadow-green-500/40 transition-all font-medium bg-gradient-to-r from-green-500 to-green-600"
            >
              OK
            </button>
          </div>
        </div>

        <div v-if="loading" class="flex flex-col items-center justify-center py-20">
            <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-[#80A1BA] mb-4"></div>
            <p class="text-sm text-slate-500 animate-pulse">Sedang memuat data...</p>
        </div>

        <div
          v-else-if="histories.length === 0"
          class="flex flex-col items-center justify-center py-16 text-center"
        >
          <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4">
              <FileText class="w-10 h-10 text-slate-300" />
          </div>
          <p class="text-gray-600 font-medium mb-1">Belum ada riwayat</p>
          <p class="text-gray-400 text-sm mb-6 max-w-xs mx-auto">
            Riwayat penerjemahan bahasa isyarat Anda akan muncul di sini secara otomatis.
          </p>
          <button
            @click="goHome"
            class="px-6 py-2.5 text-white rounded-xl shadow-lg shadow-[#80A1BA]/30 hover:shadow-[#80A1BA]/40 transition-all duration-200 hover:-translate-y-0.5 text-sm bg-[#80A1BA]"
          >
            Mulai Deteksi Sekarang
          </button>
        </div>

        <div v-else>
            
            <div class="block sm:hidden space-y-4">
                <div 
                    v-for="(item, index) in formattedHistories" 
                    :key="item.id_history"
                    class="border border-gray-100 rounded-xl p-4 bg-gray-50/50 hover:bg-white hover:shadow-md transition-all duration-200"
                >
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs font-bold text-[#80A1BA] bg-[#80A1BA]/10 px-2 py-1 rounded">
                            #{{ index + 1 }}
                        </span>
                        <div class="text-right">
                            <div class="text-xs font-semibold text-gray-700">{{ item.date }}</div>
                            <div class="text-[10px] text-gray-400">{{ item.time }}</div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <p class="text-xs text-gray-500 mb-1">Terjemahan:</p>
                        <p class="text-gray-800 font-medium leading-relaxed">
                            {{ item.kata_terdeteksi || '-' }}
                        </p>
                    </div>

                    <div class="flex items-center justify-between pt-3 border-t border-gray-100">
                        <span class="text-xs text-gray-500">Akurasi:</span>
                        <span class="text-xs font-bold" :class="getConfidenceColor(item.confidence)">
                            {{ item.confidence ? (item.confidence * 100).toFixed(1) + '%' : '-' }}
                        </span>
                    </div>
                </div>
            </div>

            <div class="hidden sm:block overflow-hidden rounded-xl border border-gray-200">
                <table class="w-full text-sm text-left">
                    <thead class="bg-gray-50 text-gray-600 font-semibold uppercase text-xs tracking-wider">
                    <tr>
                        <th class="py-4 px-6 w-16">No.</th>
                        <th class="py-4 px-6 w-32">Waktu</th>
                        <th class="py-4 px-6">Hasil Terjemahan</th>
                        <th class="py-4 px-6 w-32 text-center">Confidence</th>
                    </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                    <tr
                        v-for="(item, index) in formattedHistories"
                        :key="item.id_history"
                        class="bg-white hover:bg-slate-50 transition-colors"
                    >
                        <td class="py-4 px-6 text-gray-500 font-medium">
                        {{ index + 1 }}
                        </td>
                        <td class="py-4 px-6">
                            <div class="flex flex-col">
                                <span class="text-gray-800 font-medium">{{ item.date }}</span>
                                <span class="text-gray-400 text-xs">{{ item.time }}</span>
                            </div>
                        </td>
                        <td class="py-4 px-6">
                        <div class="max-w-lg text-gray-700 leading-relaxed">
                            {{ item.kata_terdeteksi || '-' }}
                        </div>
                        </td>
                        <td class="py-4 px-6 text-center">
                            <span 
                                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                                :class="item.confidence > 0.8 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
                            >
                                {{ item.confidence ? (item.confidence * 100).toFixed(1) + '%' : '-' }}
                            </span>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div class="mt-6 flex items-center justify-between text-sm text-gray-500 px-1">
                <p>Menampilkan {{ histories.length }} data</p>
            </div>
        </div>

        <div v-if="errorMessage" class="mt-6 p-4 rounded-xl bg-red-50 border border-red-100 flex items-center gap-3">
             <div class="bg-red-100 p-1.5 rounded-full">
                <Trash2 class="w-4 h-4 text-red-600" /> 
             </div>
             <p class="text-sm text-red-600">{{ errorMessage }}</p>
        </div>

      </div>
    </main>

    <footer class="mt-auto py-6">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <p class="text-slate-400 text-xs">
          © 2025 HandSpeak. Memudahkan komunikasi untuk semua.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import {
  History as HistoryIcon,
  Trash2,
  FileText,
  CheckCircle,
} from "lucide-vue-next";
import Navbar from "@/components/Navbar.vue";

const router = useRouter();
const API_BASE = "http://127.0.0.1:8001";

const histories = ref([]);
const loading = ref(false);
const errorMessage = ref("");
const showDeleteDialog = ref(false);
const showSuccessNotification = ref(false);
const successMessage = ref("");

// Helper untuk warna confidence score
const getConfidenceColor = (score) => {
    if (!score) return 'text-gray-400';
    return score > 0.8 ? 'text-green-600' : 'text-yellow-600';
};

// format ke tanggal & jam terpisah
const formattedHistories = computed(() =>
  histories.value.map((item) => {
    const d = new Date(item.created_at);
    const date = d.toLocaleDateString("id-ID", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
    const time = d.toLocaleTimeString("id-ID", {
      hour: "2-digit",
      minute: "2-digit",
    });
    return {
      ...item,
      date,
      time,
    };
  })
);

function goHome() {
  router.push("/");
}

async function fetchHistory() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    successMessage.value = "Anda harus login terlebih dahulu untuk melihat riwayat!";
    showSuccessNotification.value = true;
    setTimeout(() => {
      router.push("/login");
    }, 1500);
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  try {
    const res = await fetch(`${API_BASE}/history`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      if (res.status === 401) {
        successMessage.value = "Sesi Anda telah berakhir. Silakan login kembali.";
        showSuccessNotification.value = true;
        localStorage.removeItem("access_token");
        setTimeout(() => {
          router.push("/login");
        }, 1500);
        return;
      }
      throw new Error(data.detail || "Gagal memuat riwayat.");
    }

    histories.value = data;
  } catch (err) {
    console.error(err);
    errorMessage.value = err.message || "Terjadi kesalahan.";
  } finally {
    loading.value = false;
  }
}

async function confirmDelete() {
  showDeleteDialog.value = false;
  
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      successMessage.value = "Anda harus login terlebih dahulu!";
      showSuccessNotification.value = true;
      setTimeout(() => {
        router.push("/login");
      }, 1500);
      return;
    }

    loading.value = true;

    const res = await fetch(`${API_BASE}/history`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      if (res.status === 401) {
        successMessage.value = "Sesi Anda telah berakhir. Silakan login kembali.";
        showSuccessNotification.value = true;
        localStorage.removeItem("access_token");
        setTimeout(() => {
          router.push("/login");
        }, 1500);
        return;
      }
      throw new Error("Gagal menghapus riwayat");
    }

    const data = await res.json();
    
    // Clear data dan tampilkan notifikasi sukses
    histories.value = [];
    errorMessage.value = "";
    
    // Tampilkan modal sukses
    successMessage.value = data.message || "Semua riwayat berhasil dihapus!";
    showSuccessNotification.value = true;
    
  } catch (err) {
    console.error(err);
    errorMessage.value = err.message || "Terjadi kesalahan saat menghapus riwayat";
  } finally {
    loading.value = false;
  }
}

async function handleClearLocal() {
  // Fungsi ini sudah tidak digunakan, diganti dengan showDeleteDialog
  showDeleteDialog.value = true;
}

onMounted(() => {
  fetchHistory();
});
</script>