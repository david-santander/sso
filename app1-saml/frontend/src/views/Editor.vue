<template>
  <div class="editor">
    <h2>Editor Dashboard</h2>
    <p>This page is only accessible to users with the 'editor' role.</p>
    
    <!-- Loading state while fetching editor data -->
    <div v-if="loading" class="loading">Loading...</div>
    
    <!-- Error state for failed requests or unauthorized access -->
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <!-- Editor content displayed when data is successfully loaded -->
    <div v-else-if="data" class="content">
      <div class="info-card">
        <h3>Editor Content</h3>
        <p>{{ data.message }}</p>
        <p><strong>Editor User:</strong> {{ data.user }}</p>
        <p><strong>Content:</strong> {{ data.data }}</p>
      </div>
      
      <!-- Editor-specific actions (placeholder buttons for demo) -->
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
/**
 * @component Editor
 * @description Editor dashboard component with role-restricted access
 * 
 * This component demonstrates:
 * - Role-based access control for editor users
 * - Hierarchical role permissions (admin users can also access)
 * - Protected API endpoint consumption
 * - Error handling for authentication and authorization
 * 
 * Note: Admin users can access this page due to role hierarchy
 * where admin role includes editor permissions
 */
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Editor',
  setup() {
    // Reactive state for component data
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    /**
     * Fetches editor-specific data on component mount
     * 
     * The backend /api/editor endpoint:
     * - Requires authentication (session cookie)
     * - Requires editor role (or admin role via hierarchy)
     * - Returns editor-specific content and actions
     */
    onMounted(async () => {
      try {
        // Call editor-protected endpoint
        const response = await axios.get('/api/editor')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          // User not authenticated - redirect to SAML login
          error.value = 'You must be authenticated to view this resource.'
          setTimeout(() => {
            window.location.href = '/saml/login'
          }, 2000)
        } else if (err.response && err.response.status === 403) {
          // User authenticated but lacks editor role
          error.value = 'You need editor role to access this resource.'
        } else {
          // Other errors (network, server, etc.)
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