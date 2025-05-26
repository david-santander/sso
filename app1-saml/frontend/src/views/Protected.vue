<template>
  <div class="protected">
    <h2>Protected Resource</h2>
    <p>This page is only accessible to authenticated users.</p>
    
    <!-- Loading state while fetching protected data -->
    <div v-if="loading" class="loading">Loading...</div>
    
    <!-- Error state for failed requests or authentication issues -->
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <!-- Protected content displayed when data is successfully loaded -->
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
/**
 * @component Protected
 * @description Protected page component requiring authentication
 * 
 * This component demonstrates:
 * - Basic authentication requirement (no specific role needed)
 * - Session-based access control via SAML
 * - Generic protected resource pattern
 * 
 * Access requirements:
 * - User must be authenticated via SAML
 * - Any authenticated user can access (no role restrictions)
 * - Useful for general member-only content
 */
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Protected',
  setup() {
    // Reactive state for component data
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    /**
     * Fetches protected data on component mount
     * 
     * The backend /api/protected endpoint:
     * - Requires valid session (authentication)
     * - No role requirements - any authenticated user can access
     * - Returns generic protected content
     */
    onMounted(async () => {
      try {
        // Call protected endpoint - session cookie sent automatically
        const response = await axios.get('/api/protected')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          // User not authenticated - redirect to SAML login
          // This should rarely happen due to route guard
          error.value = 'You must be authenticated to view this resource.'
          setTimeout(() => {
            window.location.href = '/saml/login'
          }, 2000)
        } else {
          // Other errors (network, server, etc.)
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