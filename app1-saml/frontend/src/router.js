/**
 * @fileoverview Vue Router configuration with SAML authentication and RBAC
 * 
 * This router configuration implements:
 * - Public and protected routes
 * - Authentication checks via navigation guards
 * - Role-based access control for admin and editor pages
 * - Automatic redirection to SAML login when authentication is required
 * 
 * Security Features:
 * - Pre-route authentication verification
 * - Role validation before accessing restricted pages
 * - Session state checking to prevent unauthorized access
 */

import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Protected from './views/Protected.vue'
import Admin from './views/Admin.vue'
import Editor from './views/Editor.vue'
import { auth } from './auth'

/**
 * Route definitions with metadata for access control
 * 
 * Route metadata properties:
 * - requiresAuth: Route requires authenticated user
 * - requiresRole: Specific role required for access
 */
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/protected',
    name: 'Protected',
    component: Protected,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresRole: 'admin' }
  },
  {
    path: '/editor',
    name: 'Editor',
    component: Editor,
    meta: { requiresAuth: true, requiresRole: 'editor' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/**
 * Global navigation guard for authentication and authorization
 * 
 * This guard runs before every route navigation and:
 * 1. Ensures authentication state is loaded
 * 2. Validates authentication for protected routes
 * 3. Checks role-based permissions
 * 4. Redirects to login or home page as needed
 * 
 * @param {Object} to - Target route
 * @param {Object} from - Current route
 * @param {Function} next - Navigation callback
 */
router.beforeEach(async (to, from, next) => {
  // Check auth status if not already loaded
  if (auth.state.isLoading) {
    await auth.checkAuth()
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!auth.state.isAuthenticated) {
      // Redirect to SAML login - this will trigger the full SAML flow
      auth.login()
      return
    }
    
    // Check if route requires specific role
    if (to.meta.requiresRole) {
      if (!auth.hasRole(to.meta.requiresRole)) {
        // User doesn't have required role - show alert and redirect to home
        // In production, consider using a proper notification system
        alert(`Access denied. Role '${to.meta.requiresRole}' required.`)
        next('/')
        return
      }
    }
  }
  
  // Allow navigation to proceed
  next()
})

export default router