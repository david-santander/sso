<template>
  <div class="editor">
    <h2>Editor Dashboard</h2>
    <p>This page is only accessible to users with the 'editor' role.</p>
    
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="data" class="content">
      <div class="info-card">
        <h3>Editor Content</h3>
        <p>{{ data.message }}</p>
        <p><strong>Editor User:</strong> {{ data.user }}</p>
        <p><strong>Content:</strong> {{ data.data }}</p>
      </div>
      
      <div class="editor-actions">
        <h3>Editor Actions</h3>
        <button class="btn-primary">Create Content</button>
        <button class="btn-primary">Edit Content</button>
        <button class="btn-primary">Publish Content</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Editor',
  setup() {
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    onMounted(async () => {
      try {
        const response = await axios.get('/api/editor')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          error.value = 'You must be authenticated to view this resource.'
          setTimeout(() => {
            window.location.href = '/oidc/login'
          }, 2000)
        } else if (err.response && err.response.status === 403) {
          error.value = 'You need editor role to access this resource.'
        } else {
          error.value = 'Error loading editor resource.'
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