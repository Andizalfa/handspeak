// src/composables/useAuth.js
import { ref } from "vue";

// simpan token
const token = ref(localStorage.getItem("token") || null);

// ==== LOGIN ====
function setToken(newToken) {
  token.value = newToken;
  localStorage.setItem("token", newToken);
}

// ==== LOGOUT ====
function logout() {
  token.value = null;
  localStorage.removeItem("token");
}

// ==== GET TOKEN ====
function getToken() {
  return token.value;
}

export function useAuth() {
  return {
    token,
    setToken,
    logout,
    getToken,
  };
}
