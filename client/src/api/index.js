import axios from 'axios';

// Vite exposes env vars via import.meta.env
const DEFAULT_BASE = 'http://localhost:8000';
const base = (import.meta && import.meta.env && import.meta.env.VITE_API_BASE) || DEFAULT_BASE;

const instance = axios.create({
  baseURL: base,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30_000,
});

function handleResponse(promise) {
  return promise.then((res) => res.data).catch((err) => {
    // Normalize error to throw the response data when available
    if (err.response && err.response.data) throw err.response.data;
    throw err;
  });
}

const api = {
  get: (endpoint) => handleResponse(instance.get(endpoint)),
  post: (endpoint, body) => handleResponse(instance.post(endpoint, body)),
};

export default api;
