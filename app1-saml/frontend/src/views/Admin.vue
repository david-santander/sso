<template>
  <div class="admin">
    <h2>Admin Dashboard</h2>
    <p>This page is only accessible to users with the 'admin' role.</p>
    
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="data" class="content">
      <div class="info-card">
        <h3>Admin Content</h3>
        <p>{{ data.message }}</p>
        <p><strong>Admin User:</strong> {{ data.user }}</p>
      </div>
      
      <div class="admin-actions">
        <h3>Admin Actions</h3>
        <button class="btn-primary">Manage Users</button>
        <button class="btn-primary">View Logs</button>
        <button class="btn-primary">System Settings</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Admin',
  setup() {
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    onMounted(async () => {
      try {
        const response = await axios.get('/api/admin')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          error.value = 'You must be authenticated to view this resource.'
          setTimeout(() => {
            window.location.href = '/saml/login'
          }, 2000)
        } else if (err.response && err.response.status === 403) {
          error.value = 'You need admin role to access this resource.'
        } else {
          error.value = 'Error loading admin resource.'
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