<!--
  Main Application Component for OIDC Demo
  
  This component serves as the root component and provides:
  - Navigation bar with role-based menu items
  - Authentication state display
  - Login/Logout functionality
  - Router outlet for child views
  
  Key OIDC features demonstrated:
  - Session-based authentication status
  - Role-based navigation visibility
  - Centralized auth state management
-->
<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <h1>App2 - OIDC Relying Party</h1>
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <router-link to="/protected" v-if="isAuthenticated">Protected</router-link>
          <router-link to="/admin" v-if="hasRole('admin')">Admin</router-link>
          <router-link to="/editor" v-if="hasRole('editor')">Editor</router-link>
          <span v-if="isAuthenticated" class="user-info">
            {{ user.username }} ({{ user.roles.join(', ') }})
          </span>
          <button v-if="!isAuthenticated" @click="login" class="btn-primary">Login</button>
          <button v-else @click="logout" class="btn-secondary">Logout</button>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view :user="user" />
    </main>
  </div>
</template>

<script>
import { computed, onMounted, provide } from 'vue'
import { auth } from './auth'

/**
 * Root application component
 * 
 * Responsibilities:
 * - Provide authentication service to child components
 * - Display user authentication status
 * - Handle login/logout actions
 * - Show/hide navigation based on roles
 */
export default {
  name: 'App',
  setup() {
    // Reactive computed properties for auth state
    const user = computed(() => auth.state.user)
    const isAuthenticated = computed(() => auth.state.isAuthenticated)

    /**
     * Check if current user has specified role
     * Uses auth service's hierarchical role checking
     * @param {string} role - Role to check
     * @returns {boolean}
     */
    const hasRole = (role) => {
      return auth.hasRole(role)
    }

    /**
     * Initiate OIDC login flow
     * Redirects to backend which handles OIDC authorization
     */
    const login = () => {
      auth.login()
    }

    /**
     * Initiate OIDC logout flow
     * Clears session and redirects to Keycloak logout
     */
    const logout = () => {
      auth.logout()
    }

    onMounted(() => {
      // Auth check is already done in main.js, but refresh here in case
      // This ensures UI reflects current auth state
      auth.checkAuth()
    })

    // Provide auth service to child components via Vue's provide/inject
    // This allows any descendant component to access auth functionality
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