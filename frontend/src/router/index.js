import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/game/:gameCode",
      name: "game",
      component: () => import("../views/GameView.vue"),
      props: (route) => ({
        gameCode: Number(route.params.gameCode),
      }),
    },
    {
      path: "/commands",
      name: "commands",
      component: () => import("../views/CommandsView.vue"),
    }
  ],
});

export default router;
