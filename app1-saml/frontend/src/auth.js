import { reactive } from 'vue'

const API_BASE_URL = 'http://localhost:3000/api'

const authState = reactive({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  roles: []
})

export const auth = {
  state: authState,
  
  async checkAuth() {
    try {
      const response = await fetch(`${API_BASE_URL}/user`, {
        credentials: 'include'
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.authenticated) {
          authState.user = data
          authState.isAuthenticated = true
          authState.roles = data.roles || []
        } else {
          authState.user = null
          authState.isAuthenticated = false
          authState.roles = []
        }
      } else {
        authState.user = null
        authState.isAuthenticated = false
        authState.roles = []
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      authState.user = null
      authState.isAuthenticated = false
      authState.roles = []
    } finally {
      authState.isLoading = false
    }
  },
  
  hasRole(role) {
    // Define role hierarchy
    const roleHierarchy = {
      'admin': ['editor', 'viewer'],
      'editor': ['viewer'],
      'viewer': []
    }
    
    // Direct role check
    if (authState.roles.includes(role)) {
      return true
    }
    
    // Check hierarchical roles
    for (const userRole of authState.roles) {
      if (roleHierarchy[userRole] && roleHierarchy[userRole].includes(role)) {
        return true
      }
    }
    
    return false
  },
  
  hasAnyRole(roles) {
    return roles.some(role => this.hasRole(role))
  },
  
  logout() {
    window.location.href = 'http://localhost:3000/saml/logout'
  },
  
  login() {
    window.location.href = '/saml/login'
  }
}

export default auth