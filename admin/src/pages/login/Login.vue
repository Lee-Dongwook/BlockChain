<template>
  <div>
    <h1>Login</h1>
    <button @click="handleLogin">로그인</button>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "../../store";
import { useRouter } from "vue-router";

const router = useRouter();
const auth = useAuthStore();

function handleLogin() {
  auth.login("FAKE_TOKEN", "admin");
  router.push("/");
}
</script>
