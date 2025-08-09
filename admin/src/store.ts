import { defineStore } from "pinia";

interface State {
  token: string | null;
  role: "admin" | "viewer";
}

export const useAuthStore = defineStore("auth", {
  state: (): State => ({ token: null, role: "viewer" }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    login(token: string, role: State["role"]) {
      this.token = token;
      this.role = role;
    },
    logout() {
      this.token = null;
      this.role = "viewer";
    },
  },
});
