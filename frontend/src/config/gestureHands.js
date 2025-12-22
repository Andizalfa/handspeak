// gestureHands.js
// Konfigurasi tangan yang digunakan untuk setiap gesture saat training
// Format: "L" = Left only, "R" = Right only, "LR" = Both hands

export const GESTURE_HANDS = {
  "Apa": "LR",
  "Apa Kabar": "R",
  "Bagaimana": "LR",
  "Baik": "LR",
  "Belajar": "R",
  "Berapa": "R",
  "Berasal": "L",
  "Berdiri": "LR",
  "Bertemu": "LR",
  "Bingung": "LR",
  "Boleh": "LR",
  "Dari": "L",
  "Dia": "R",
  "Dimana": "R",
  "Duduk": "LR",
  "Halo": "R",
  "Hati-hati": "LR",
  "Kalian": "R",
  "Kami": "R",
  "Kamu": "R",
  "Kapan": "R",
  "Kemana": "R",
  "Kita": "R",
  "Lagi": "L",
  "Makan": "R",
  "Mandi": "R",
  "Marah": "R",
  "Masalah": "LR",
  "Melihat": "R",
  "Membaca": "LR",
  "Menulis": "LR",
  "Mereka": "LR",
  "Minum": "L",  // Tangan kiri fisik
  "Nama": "LR",
  "Pendek": "R",
  "Ramah": "LR",
  "Sabar": "R",
  "Sampai": "L",
  "Saya": "R",
  "Sedih": "R",
  "Sehat": "LR",
  "Selamat Malam": "R",
  "Selamat Pagi": "R",
  "Selamat Siang": "R",
  "Selamat Sore": "R",
  "Senang": "LR",
  "Siapa": "R",
  "Terimakasih": "L",
  "Tidur": "L",
  "Tinggi": "R"
}

// Fungsi untuk cek apakah hand pattern sesuai dengan gesture
export function validateHandPattern(gestureName, handPattern) {
  const expectedPattern = GESTURE_HANDS[gestureName];
  
  if (!expectedPattern) {
    // Gesture tidak dikenal, terima saja
    return true;
  }
  
  // Normalisasi pattern - sort untuk handle "RL" vs "LR"
  const normalizedPattern = handPattern.replace(/[^LR]/g, '').split('').sort().join('');
  const normalizedExpected = expectedPattern.split('').sort().join('');
  
  const isValid = normalizedPattern === normalizedExpected;
  
  // Debug log
  console.log(`🔍 Validasi tangan: "${gestureName}" - Expected: "${expectedPattern}", Got: "${handPattern}" (normalized: "${normalizedPattern}") - ${isValid ? '✅ VALID' : '❌ INVALID'}`);
  
  return isValid;
}
