import axios from "axios";
import { useAuthStore } from "../../store";

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:3000",
});

http.interceptors.request.use((config) => {
  const auth = useAuthStore();
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`;
  }
  return config;
});

http.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      useAuthStore().logout();
    }
    return Promise.reject(err);
  }
);
