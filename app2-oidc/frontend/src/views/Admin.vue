<!--
  Admin View Component - Role-protected admin dashboard
  
  This component:
  - Requires 'admin' role for access (enforced by router guard)
  - Fetches admin-specific data from protected API endpoint
  - Demonstrates role-based content and actions
  - Handles authentication/authorization errors gracefully
  
  Security notes:
  - Double protection: router guard + API endpoint authorization
  - Automatic redirect to login on 401 (session expired)
  - Clear error messaging for authorization failures
-->
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

/**
 * Admin dashboard component
 * 
 * Protected component that:
 * - Fetches admin-only resources from backend
 * - Handles authorization errors appropriately
 * - Displays admin-specific functionality
 * 
 * Authentication flow:
 * 1. Router guard checks admin role (frontend)
 * 2. API call includes session cookie
 * 3. Backend validates session and role
 * 4. Returns admin data or appropriate error
 */
export default {
  name: 'Admin',
  setup() {
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    /**
     * Fetch admin data on component mount
     * 
     * Error handling:
     * - 401: Session expired or not authenticated -> redirect to login
     * - 403: Authenticated but lacks admin role -> show error
     * - Other: Generic error message
     * 
     * Note: Even though router guard checks role, API also validates
     * This provides defense-in-depth security
     */
    onMounted(async () => {
      try {
        // API call automatically includes session cookie
        const response = await axios.get('/api/admin')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          // Session expired or not authenticated
          error.value = 'You must be authenticated to view this resource.'
          // Auto-redirect to OIDC login after brief delay
          setTimeout(() => {
            window.location.href = '/oidc/login'
          }, 2000)
        } else if (err.response && err.response.status === 403) {
          // Authenticated but lacks required role
          error.value = 'You need admin role to access this resource.'
        } else {
          // Network or server error
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