<template>
  <div>
    <h2>ฟอร์มสมัครงาน</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="firstName">ชื่อ:</label>
        <input type="text" id="firstName" v-model="formData.firstName" required />
      </div>
      <div>
        <label for="lastName">นามสกุล:</label>
        <input type="text" id="lastName" v-model="formData.lastName" required />
      </div>
      <div>
        <label for="address">ที่อยู่:</label>
        <textarea id="address" v-model="formData.address" required></textarea>
      </div>
      <div>
        <label for="salaryExpectation">คาดหวังเงินเดือน (บาท):</label>
        <input
          type="number"
          id="salaryExpectation"
          v-model.number="formData.salaryExpectation"
          required
        />
      </div>
      <div>
        <label for="experience">ประสบการณ์:</label>
        <textarea id="experience" v-model="formData.experience"></textarea>
      </div>
      <button @click="submitForm">ยืนยัน</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      formData: {
        firstName: '',
        lastName: '',
        address: '',
        salaryExpectation: null,
        experience: ''
      }
    }
  },
  methods: {
    submitForm() {
      this.$emit('formSubmitted', this.formData)
      this.clearForm()
    },
    clearForm() {
      this.formData = {
        firstName: '',
        lastName: '',
        address: '',
        salaryExpectation: null,
        experience: ''
      }
    }
  }
}
</script>
