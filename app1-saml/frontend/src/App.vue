<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <h1>App1 - SAML Service Provider</h1>
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <router-link to="/protected" v-if="isAuthenticated">Protected</router-link>
          <router-link to="/admin" v-if="hasRole('admin')">Admin</router-link>
          <router-link to="/editor" v-if="hasRole('editor')">Editor</router-link>
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
import { ref, onMounted, provide } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    const user = ref(null)
    const isAuthenticated = ref(false)

    const checkAuth = async () => {
      try {
        const response = await axios.get('/api/user')
        if (response.data.authenticated) {
          user.value = response.data
          isAuthenticated.value = true
        } else {
          user.value = null
          isAuthenticated.value = false
        }
      } catch (error) {
        console.error('Error checking auth:', error)
        user.value = null
        isAuthenticated.value = false
      }
    }

    const hasRole = (role) => {
      return user.value && user.value.roles && user.value.roles.includes(role)
    }

    const login = () => {
      window.location.href = '/saml/login'
    }

    const logout = () => {
      window.location.href = '/saml/logout'
    }

    onMounted(() => {
      checkAuth()
    })

    provide('checkAuth', checkAuth)

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