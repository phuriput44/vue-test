<template>
  <div>
    <input type="file" @change="handleFileUpload" accept=".csv" />
    <button @click="uploadCSV">Upload CSV</button>
    <h1>รายการสรุปรวมของผู้สมัครงาน</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>ชื่อ</th>
          <th>นามสกุล</th>
          <th>ที่อยู่</th>
          <th>คาดหวังเงินเดือน</th>
          <th>ประสบการณ์</th>
          <th><button @click="downloadCSV">Export to CSV</button></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(applicant, index) in applicants" :key="index">
          <td>{{ applicant.applicantID }}</td>
          <td>{{ applicant.firstName }}</td>
          <td>{{ applicant.lastName }}</td>
          <td>{{ applicant.address }}</td>
          <td>{{ applicant.salaryExpectation }}</td>
          <td>{{ applicant.experience }}</td>
          <td><button @click="deleteApplicant(applicant.applicantID)">ลบ</button></td>
        </tr>
      </tbody>
    </table>
    <button @click="logout">ออกจากระบบ</button>
  </div>
</template>

<script>
import apiClient from '../axios.js'
import axios from 'axios'
export default {
  data() {
    return {
      applicants: [],
      isLogin: false
    }
  },
  created() {
    // Load all applicants when the component is created
    this.getAllApplicants()
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
    },
    async getAllApplicants() {
      try {
        const response = await apiClient.get('/applicants/')
        this.applicants = response.data
      } catch (error) {
        console.error('Error fetching applicants:', error)
      }
    },
    async deleteApplicant(applicantID) {
      try {
        await apiClient.delete(`/applicants/${applicantID}`)
        // Reload the list of applicants after deleting one
        this.getAllApplicants()
      } catch (error) {
        console.error('Error deleting applicant:', error)
      }
    },
    logout() {
      localStorage.removeItem('token') // ลบ token ออกจาก local storage
      this.$router.push('/login')
    },
    async downloadCSV() {
      try {
        const response = await apiClient.get(`/export`)
        const blob = new Blob([response.data], { type: 'text/csv' })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = 'data.csv'
        link.click()
      } catch (error) {
        console.error('Error downloading CSV:', error)
      }
    },
    handleFileUpload(event) {
      this.file = event.target.files[0]
    },
    async uploadCSV() {
      const formData = new FormData()
      formData.append('file', this.file)
      try {
        await axios.post('http://127.0.0.1:8000/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        alert('File uploaded successfully')
      } catch (error) {
        console.error('Error uploading file:', error)
        alert('Error uploading file. Please try again.')
      }
    }
  }
}
</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
button {
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}
</style>
