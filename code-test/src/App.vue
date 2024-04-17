<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/login" v-if="!isLogin">Login</RouterLink>
      <RouterLink to="/register">Register</RouterLink>
      <RouterLink to="/show" v-if="isLogin">Show</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<script>
export default {
  data() {
    return {
      applicants: [],
      isLogin: false
    }
  },
  created() {
    this.checkLogin()
  },
  methods: {
    checkLogin() {
      const token = localStorage.getItem('token')
      if (token) {
        this.isLogin = true
      } else {
        this.isLogin = false
      }
      console.log(this.isLogin)
    }
  }
}
</script>
