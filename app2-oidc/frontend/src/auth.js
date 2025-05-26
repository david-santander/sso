/**
 * Authentication module for OIDC (OpenID Connect) implementation
 * 
 * This module manages the authentication state and provides methods for:
 * - Checking authentication status via session cookies
 * - Managing user roles and hierarchical permissions
 * - Handling login/logout flows through OIDC provider
 * 
 * Key differences from SAML implementation:
 * - Uses session-based authentication with httpOnly cookies
 * - Backend handles OIDC token exchange and validation
 * - Frontend only needs to check session status, not handle tokens directly
 * 
 * Security considerations:
 * - No tokens stored in frontend (prevents XSS attacks)
 * - All authentication state managed via secure httpOnly cookies
 * - CORS credentials included for cross-origin requests
 */

import { reactive } from 'vue'

// Backend API endpoint for authentication operations
const API_BASE_URL = 'http://localhost:4000/api'

/**
 * Reactive authentication state
 * @property {Object|null} user - Current authenticated user data
 * @property {boolean} isAuthenticated - Whether user is authenticated
 * @property {boolean} isLoading - Loading state for async operations
 * @property {Array<string>} roles - User's assigned roles
 */
const authState = reactive({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  roles: []
})

/**
 * Authentication service object
 * Provides methods for authentication operations and role checks
 */
export const auth = {
  state: authState,
  
  /**
   * Checks current authentication status by calling backend API
   * 
   * This method:
   * 1. Sends request to backend with session cookie
   * 2. Backend validates OIDC session and returns user data
   * 3. Updates frontend auth state based on response
   * 
   * @async
   * @returns {Promise<void>}
   */
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
  
  /**
   * Checks if user has a specific role, including hierarchical permissions
   * 
   * Role hierarchy:
   * - admin: Has all permissions (admin, editor, viewer)
   * - editor: Has editor and viewer permissions
   * - viewer: Has only viewer permissions
   * 
   * @param {string} role - Role to check
   * @returns {boolean} - True if user has the role or a higher role
   */
  hasRole(role) {
    // Define role hierarchy - higher roles inherit lower role permissions
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
  
  /**
   * Checks if user has any of the specified roles
   * 
   * @param {Array<string>} roles - Array of roles to check
   * @returns {boolean} - True if user has at least one of the roles
   */
  hasAnyRole(roles) {
    return roles.some(role => this.hasRole(role))
  },
  
  /**
   * Initiates OIDC logout flow
   * 
   * Redirects to backend logout endpoint which:
   * 1. Clears server-side session
   * 2. Redirects to Keycloak for OIDC logout
   * 3. Keycloak clears its session and redirects back
   * 
   * Note: Full URL used to ensure proper CORS handling
   */
  logout() {
    window.location.href = 'http://localhost:4000/oidc/logout'
  },
  
  /**
   * Initiates OIDC login flow
   * 
   * Redirects to backend login endpoint which:
   * 1. Generates OIDC authorization request
   * 2. Redirects to Keycloak login page
   * 3. After auth, Keycloak redirects back with authorization code
   * 4. Backend exchanges code for tokens and creates session
   */
  login() {
    window.location.href = '/oidc/login'
  }
}

export default auth