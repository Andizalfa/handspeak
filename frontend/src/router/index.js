import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import HomePage from "../pages/HomePage.vue";
import HistoryPage from "../pages/HistoryPage.vue";
import { isLoggedIn } from "../api/apiClient";

const routes = [
  { path: "/login", name: "login", component: LoginPage },
  { path: "/register", name: "register", component: RegisterPage },
  { path: "/", name: "home", component: HomePage }, // Tidak perlu auth - halaman publik
  { path: "/history", name: "history", component: HistoryPage, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const loggedIn = isLoggedIn();

  if (to.meta.requiresAuth && !loggedIn) {
    next({ name: "login" });
  } else if ((to.name === "login" || to.name === "register") && loggedIn) {
    next({ name: "home" });
  } else {
    next();
  }
});

export default router;
