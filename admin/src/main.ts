import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import router from "./router";
import { VueQueryPlugin, QueryClient } from "@tanstack/vue-query";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(VueQueryPlugin, { queryClient: new QueryClient() });

app.mount("#app");
