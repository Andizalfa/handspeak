// src/api/apiClient.js

const API_BASE = "http://localhost:8001"; // sesuaikan kalau port/backend beda

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;

  const res = await fetch(url, {
    // default
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = null;
  try {
    data = await res.json();
  } catch (e) {
    // kalau bukan JSON, biarkan null
  }

  if (!res.ok) {
    const detail = data?.detail || res.statusText || "Request failed";
    const err = new Error(detail);
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return data;
}

// =====================
// AUTH
// =====================

export async function login(email, password) {
  const data = await request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  // backend-mu mengembalikan: { access_token, token_type }
  if (data?.access_token) {
    localStorage.setItem("access_token", data.access_token);
  }

  return data;
}

export async function registerUser(name, email, password) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password }),
  });
}

export async function getMe() {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("Belum login");

  return request("/auth/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

// =====================
// PREDICT SEQUENCE
// =====================

export async function predictSequence(sequence) {
  // Gunakan endpoint public tanpa auth untuk testing
  return request("/predict_sequence_public", {
    method: "POST",
    body: JSON.stringify({ sequence }),
  });
}

export async function predictSequenceWithAuth(sequence) {
  // Endpoint dengan auth untuk save ke history
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("Belum login");

  return request("/predict_sequence", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ sequence }),
  });
}

// =====================
// HISTORY
// =====================

export async function getHistory() {
  const token = localStorage.getItem("access_token");
  if (!token) throw new Error("Belum login");

  return request("/history", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function isLoggedIn() {
  return !!localStorage.getItem("access_token");
}
