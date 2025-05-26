<!--
  Editor View Component - Role-protected editor dashboard
  
  This component:
  - Requires 'editor' role for access (admin users also have access)
  - Fetches editor-specific data from protected API endpoint
  - Demonstrates hierarchical role access (admins can view)
  - Provides editor-specific actions and content
  
  Role hierarchy:
  - Admin users automatically have editor permissions
  - Pure editor users can only access editor functions
  - Viewer users are denied access
-->
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

/**
 * Editor dashboard component
 * 
 * Protected component demonstrating:
 * - Role-based access with hierarchy
 * - API integration for role-specific resources
 * - Proper error handling for auth failures
 * 
 * Access control:
 * - Router guard checks for editor role (or higher)
 * - Backend API also validates role permissions
 * - Admin users can access due to role hierarchy
 */
export default {
  name: 'Editor',
  setup() {
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    /**
     * Fetch editor data on component mount
     * 
     * Security flow:
     * 1. Frontend router already checked role access
     * 2. API call includes httpOnly session cookie
     * 3. Backend validates both authentication and authorization
     * 4. Returns data only if user has editor or admin role
     * 
     * Error scenarios:
     * - 401: No valid session -> redirect to OIDC login
     * - 403: Valid session but insufficient role
     * - Other: Network/server errors
     */
    onMounted(async () => {
      try {
        // Session cookie automatically included
        const response = await axios.get('/api/editor')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          // Not authenticated or session expired
          error.value = 'You must be authenticated to view this resource.'
          // Redirect to OIDC provider for re-authentication
          setTimeout(() => {
            window.location.href = '/oidc/login'
          }, 2000)
        } else if (err.response && err.response.status === 403) {
          // Authenticated but lacks editor (or higher) role
          error.value = 'You need editor role to access this resource.'
        } else {
          // Generic error fallback
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