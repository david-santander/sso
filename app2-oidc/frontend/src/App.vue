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

export default {
  name: 'App',
  setup() {
    const user = computed(() => auth.state.user)
    const isAuthenticated = computed(() => auth.state.isAuthenticated)

    const hasRole = (role) => {
      return auth.hasRole(role)
    }

    const login = () => {
      auth.login()
    }

    const logout = () => {
      auth.logout()
    }

    onMounted(() => {
      // Auth check is already done in main.js, but refresh here in case
      auth.checkAuth()
    })

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