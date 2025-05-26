/**
 * @fileoverview Authentication service for SAML-based SSO implementation
 * 
 * This module manages authentication state and provides methods for:
 * - Checking user authentication status
 * - Managing user sessions
 * - Role-based access control with hierarchical permissions
 * - SAML login/logout flows
 * 
 * @module auth
 */

import { reactive } from 'vue'

/** Base URL for backend API endpoints */
const API_BASE_URL = 'http://localhost:3000/api'

/**
 * Reactive authentication state object
 * @typedef {Object} AuthState
 * @property {Object|null} user - Current authenticated user object
 * @property {boolean} isAuthenticated - Whether user is authenticated
 * @property {boolean} isLoading - Loading state for auth operations
 * @property {Array<string>} roles - User's assigned roles
 */
const authState = reactive({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  roles: []
})

/**
 * Authentication service object providing methods for auth management
 */
export const auth = {
  /** Exposed authentication state for reactivity */
  state: authState,
  
  /**
   * Checks current authentication status by calling backend API
   * 
   * Security considerations:
   * - Uses 'include' credentials to send session cookies
   * - Validates response status before processing
   * - Resets state on any failure for security
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
   * - admin: Full access (includes editor and viewer permissions)
   * - editor: Content management (includes viewer permissions)
   * - viewer: Read-only access
   * 
   * @param {string} role - Role to check
   * @returns {boolean} True if user has the role or a higher-level role
   */
  hasRole(role) {
    // Define role hierarchy - higher roles inherit permissions of lower roles
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
   * @returns {boolean} True if user has at least one of the roles
   */
  hasAnyRole(roles) {
    return roles.some(role => this.hasRole(role))
  },
  
  /**
   * Initiates SAML logout flow
   * 
   * Redirects to backend SAML logout endpoint which:
   * 1. Destroys local session
   * 2. Generates SAML logout request
   * 3. Redirects to IdP for logout
   * 4. Handles logout response
   */
  logout() {
    window.location.href = 'http://localhost:3000/saml/logout'
  },
  
  /**
   * Initiates SAML login flow
   * 
   * Redirects to backend SAML login endpoint which:
   * 1. Generates SAML authentication request
   * 2. Redirects to IdP (Keycloak) for authentication
   * 3. Handles SAML response and creates session
   */
  login() {
    window.location.href = '/saml/login'
  }
}

export default auth