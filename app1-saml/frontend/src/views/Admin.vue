<template>
  <div class="admin">
    <h2>Admin Dashboard</h2>
    <p>This page is only accessible to users with the 'admin' role.</p>
    
    <!-- RoleGuard provides additional client-side protection -->
    <RoleGuard role="admin" :show-fallback="true">
      <!-- Loading state while fetching admin data -->
      <div v-if="loading" class="loading">Loading...</div>
      
      <!-- Error state for failed requests or unauthorized access -->
      <div v-else-if="error" class="error">{{ error }}</div>
      
      <!-- Admin content displayed when data is successfully loaded -->
      <div v-else-if="data" class="content">
        <div class="info-card">
          <h3>Admin Content</h3>
          <p>{{ data.message }}</p>
          <p><strong>Admin User:</strong> {{ data.user }}</p>
        </div>
        
        <!-- Admin-specific actions (placeholder buttons for demo) -->
        <div class="admin-actions">
          <h3>Admin Actions</h3>
          <button class="btn-primary">Manage Users</button>
          <button class="btn-primary">View Logs</button>
          <button class="btn-primary">System Settings</button>
        </div>
      </div>
      
      <!-- Fallback content shown if user somehow bypasses route guard -->
      <template #fallback>
        <div class="error">
          You need admin role to access this content. The route guard should have prevented you from reaching this page.
        </div>
      </template>
    </RoleGuard>
  </div>
</template>

<script>
/**
 * @component Admin
 * @description Admin dashboard component with role-restricted access
 * 
 * This component demonstrates:
 * - Role-based access control (RBAC) for admin users
 * - Protected API endpoint consumption
 * - Error handling for authentication and authorization failures
 * - Multi-layer security with both route guards and component-level checks
 * 
 * Security layers:
 * 1. Route guard checks authentication and admin role
 * 2. RoleGuard component provides client-side role verification
 * 3. Backend API validates session and role before returning data
 */
import { ref, onMounted } from 'vue'
import axios from 'axios'
import RoleGuard from '../components/RoleGuard.vue'

export default {
  name: 'Admin',
  components: {
    RoleGuard
  },
  setup() {
    // Reactive state for component data
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    /**
     * Fetches admin-specific data on component mount
     * 
     * Error handling:
     * - 401: User not authenticated - redirects to login
     * - 403: User lacks admin role - shows error message
     * - Other: Generic error message
     */
    onMounted(async () => {
      try {
        // Call admin-protected endpoint
        const response = await axios.get('/api/admin')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          // User not authenticated - redirect to SAML login after delay
          error.value = 'You must be authenticated to view this resource.'
          setTimeout(() => {
            window.location.href = '/saml/login'
          }, 2000)
        } else if (err.response && err.response.status === 403) {
          // User authenticated but lacks admin role
          error.value = 'You need admin role to access this resource.'
        } else {
          // Other errors (network, server, etc.)
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