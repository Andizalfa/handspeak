// 🔍 Test Environment Variables
// Jalankan script ini di browser console saat buka https://handspeak-one.vercel.app

console.log('=== Environment Variables Check ===');
console.log('VITE_API_BASE:', import.meta.env.VITE_API_BASE);
console.log('VITE_ML_API_BASE:', import.meta.env.VITE_ML_API_BASE);
console.log('===================================');

// Expected output:
// VITE_API_BASE: https://handspeak-production.up.railway.app
// VITE_ML_API_BASE: https://backendml-production-326a.up.railway.app

// Jika output adalah 'undefined', berarti env vars belum apply
// Solusi: Redeploy frontend di Vercel
