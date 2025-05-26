<template>
  <div class="protected">
    <h2>Protected Resource</h2>
    <p>This page is only accessible to authenticated users.</p>
    
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="data" class="content">
      <div class="info-card">
        <h3>Protected Content</h3>
        <p>{{ data.message }}</p>
        <p><strong>Accessed by:</strong> {{ data.user }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Protected',
  setup() {
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    onMounted(async () => {
      try {
        const response = await axios.get('/api/protected')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          error.value = 'You must be authenticated to view this resource.'
          setTimeout(() => {
            window.location.href = '/oidc/login'
          }, 2000)
        } else {
          error.value = 'Error loading protected resource.'
        }
      } finally {
        loading.value = false
      }
    })

    return {
      data,
      loading,
      error
    }
  }
}
</script>