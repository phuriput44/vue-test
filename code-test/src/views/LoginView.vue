<template>
  <div>
    <h1>เข้าสู่ระบบ</h1>
    <form @submit.prevent="login">
      <label for="username">ชื่อผู้ใช้:</label>
      <input type="text" id="username" v-model="username" />
      <label for="password">รหัสผ่าน:</label>
      <input type="password" id="password" v-model="password" />
      <button type="submit">เข้าสู่ระบบ</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const formData = new FormData()
        formData.append('username', this.username)
        formData.append('password', this.password)

        const response = await axios.post('http://127.0.0.1:8000/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        localStorage.setItem('token', response.data.access_token)
        window.location.reload()
        this.$router.push('/show')
      } catch (error) {
        console.error('Error logging in:', error)
      }
    }
  }
}
</script>
