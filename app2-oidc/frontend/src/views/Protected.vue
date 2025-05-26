<!--
  Protected View Component - Basic authenticated-only resource
  
  This component:
  - Requires authentication but no specific role
  - Demonstrates basic protected resource pattern
  - Any authenticated user can access (viewer, editor, admin)
  - Shows how to handle authentication-only protection
  
  Use case:
  - General authenticated user content
  - User dashboards, profiles, etc.
  - Resources that don't require specific permissions
-->
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

/**
 * Protected resource component
 * 
 * Demonstrates:
 * - Basic authentication requirement (no role needed)
 * - Session-based API calls
 * - Proper error handling for unauthenticated access
 * 
 * This is the simplest form of protection:
 * - User must be logged in
 * - Any valid session is accepted
 * - No role-based restrictions
 */
export default {
  name: 'Protected',
  setup() {
    const data = ref(null)
    const loading = ref(true)
    const error = ref(null)

    /**
     * Fetch protected data on component mount
     * 
     * Authentication flow:
     * 1. Request includes session cookie automatically
     * 2. Backend validates OIDC session exists
     * 3. No role check performed - any authenticated user allowed
     * 4. Returns data or 401 if not authenticated
     * 
     * Note: Unlike Admin/Editor views, no 403 errors possible
     * since this endpoint only checks authentication, not authorization
     */
    onMounted(async () => {
      try {
        // Make authenticated request to protected endpoint
        const response = await axios.get('/api/protected')
        data.value = response.data
      } catch (err) {
        if (err.response && err.response.status === 401) {
          // No valid session - need to authenticate via OIDC
          error.value = 'You must be authenticated to view this resource.'
          // Auto-redirect to initiate OIDC flow
          setTimeout(() => {
            window.location.href = '/oidc/login'
          }, 2000)
        } else {
          // Network or unexpected error
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