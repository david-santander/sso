<template>
  <div id="app">
    <!-- Navigation bar with role-based menu items -->
    <nav class="navbar">
      <div class="nav-container">
        <h1>App1 - SAML Service Provider</h1>
        <div class="nav-links">
          <!-- Public route - always visible -->
          <router-link to="/">Home</router-link>
          
          <!-- Protected routes - visible only when authenticated -->
          <router-link to="/protected" v-if="isAuthenticated">Protected</router-link>
          
          <!-- Role-specific routes - visible based on user roles -->
          <!-- Admin users can see admin page (and editor page due to hierarchy) -->
          <router-link to="/admin" v-if="hasRole('admin')">Admin</router-link>
          
          <!-- Editor users can see editor page -->
          <router-link to="/editor" v-if="hasRole('editor')">Editor</router-link>
          
          <!-- User info display - shows username and roles -->
          <span v-if="isAuthenticated" class="user-info">
            {{ user.username }} ({{ user.roles.join(', ') }})
          </span>
          
          <!-- Authentication buttons -->
          <button v-if="!isAuthenticated" @click="login" class="btn-primary">Login</button>
          <button v-else @click="logout" class="btn-secondary">Logout</button>
        </div>
      </div>
    </nav>
    
    <!-- Main content area - passes user prop to all child routes -->
    <main class="main-content">
      <router-view :user="user" />
    </main>
  </div>
</template>

<script>
/**
 * @component App
 * @description Main application component that provides the layout structure and navigation
 * 
 * This component:
 * - Manages the global navigation bar with role-based menu visibility
 * - Displays user authentication status and role information
 * - Provides authentication methods to child components via Vue's provide/inject
 * - Handles login/logout actions through SAML flow
 */
import { computed, onMounted, provide } from 'vue'
import { auth } from './auth'

export default {
  name: 'App',
  setup() {
    // Reactive computed properties for authentication state
    const user = computed(() => auth.state.user)
    const isAuthenticated = computed(() => auth.state.isAuthenticated)

    /**
     * Checks if the current user has a specific role
     * Uses the auth service's hasRole method which includes hierarchy checking
     * 
     * @param {string} role - Role to check
     * @returns {boolean} True if user has the role
     */
    const hasRole = (role) => {
      return auth.hasRole(role)
    }

    /**
     * Initiates SAML login flow by redirecting to backend login endpoint
     */
    const login = () => {
      auth.login()
    }

    /**
     * Initiates SAML logout flow by redirecting to backend logout endpoint
     * This will destroy the session and redirect to IdP for logout
     */
    const logout = () => {
      auth.logout()
    }

    onMounted(() => {
      // Auth check is already done in main.js, but refresh here in case
      // This ensures the UI is in sync with the authentication state
      auth.checkAuth()
    })

    // Provide auth utilities to child components
    // This allows any descendant component to inject and use these functions
    provide('checkAuth', auth.checkAuth)
    provide('auth', auth)

    return {
      user,
      isAuthenticated,
      hasRole,
      login,
      logout
    }
  }
}
</script>