import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { useAuthStore } from "./store";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    component: () => import("./pages/dashboard/Dashboard.vue"),
    meta: { auth: true },
  },
  {
    path: "/login",
    component: () => import("./pages/login/Login.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.auth && !auth.isLoggedIn) {
    return { path: "/login", query: { redirect: to.fullPath } };
  }
});

export default router;
