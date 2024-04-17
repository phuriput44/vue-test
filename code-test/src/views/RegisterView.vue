<template>
  <div>
    <RegisterForm @formSubmitted="handleFormSubmission" v-if="!isFormSubmitted" />
    <div v-if="isFormSubmitted">
      <h3>ข้อมูลการสมัครงานที่ส่ง</h3>
      <p>ชื่อ: {{ submittedFormData.firstName }}</p>
      <p>นามสกุล: {{ submittedFormData.lastName }}</p>
      <p>ที่อยู่: {{ submittedFormData.address }}</p>
      <p>คาดหวังเงินเดือน: {{ submittedFormData.salaryExpectation }}</p>
      <p>ประสบการณ์: {{ submittedFormData.experience }}</p>
      <button @click="submitForm">ยืนยัน</button>
    </div>
  </div>
</template>

<script>
import apiClient from '../axios'
import RegisterForm from '../components/RegisterForm.vue'

export default {
  components: {
    RegisterForm
  },
  data() {
    return {
      isFormSubmitted: false,
      submittedFormData: {}
    }
  },
  onFormSubmitted(formData) {
    console.log('Form submitted:', formData)
  },
  methods: {
    handleFormSubmission(formData) {
      apiClient
        .post('/applicants/', formData)
        .then((response) => {
          console.log('Applicant added successfully:', response.data)
          this.isFormSubmitted = true
          this.submittedFormData = formData
        })
        .catch((error) => {
          console.error('Error adding applicant:', error)
        })
    },
    submitForm() {
      this.isFormSubmitted = false
    }
  }
}
</script>
