/**
 * Vue Router configuration for OIDC application
 * 
 * This router handles:
 * - Route definitions with authentication and role requirements
 * - Navigation guards for protected routes
 * - Automatic redirection to OIDC login when authentication required
 * - Role-based access control (RBAC) enforcement
 * 
 * Security features:
 * - Authentication check before accessing protected routes
 * - Role verification using hierarchical permissions
 * - Automatic session validation on navigation
 * - Proper error handling and user feedback
 */

import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Protected from './views/Protected.vue'
import Admin from './views/Admin.vue'
import Editor from './views/Editor.vue'
import { auth } from './auth'

/**
 * Route definitions with access control metadata
 * 
 * Route metadata:
 * - requiresAuth: Route requires authenticated user
 * - requiresRole: Specific role required for access
 * 
 * Note: Role hierarchy is enforced - admins can access editor routes
 */
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
    // Public route - no authentication required
  },
  {
    path: '/protected',
    name: 'Protected',
    component: Protected,
    meta: { requiresAuth: true }
    // Requires authentication but no specific role
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresRole: 'admin' }
    // Requires admin role
  },
  {
    path: '/editor',
    name: 'Editor',
    component: Editor,
    meta: { requiresAuth: true, requiresRole: 'editor' }
    // Requires editor role (admin users also have access)
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/**
 * Global navigation guard for authentication and authorization
 * 
 * This guard:
 * 1. Ensures authentication state is loaded before route access
 * 2. Redirects to OIDC login if authentication required but user not authenticated
 * 3. Checks role-based permissions for protected routes
 * 4. Provides user feedback for authorization failures
 * 
 * OIDC flow difference from SAML:
 * - No need to handle tokens in frontend
 * - Session validation done via API call with httpOnly cookie
 * - Simpler redirect flow without complex SAML assertions
 */
router.beforeEach(async (to, from, next) => {
  // Check auth status if not already loaded
  // This ensures we have current session state from backend
  if (auth.state.isLoading) {
    await auth.checkAuth()
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!auth.state.isAuthenticated) {
      // User not authenticated - redirect to OIDC login
      // Backend will handle OIDC authorization flow
      auth.login()
      return
    }
    
    // Check if route requires specific role
    if (to.meta.requiresRole) {
      if (!auth.hasRole(to.meta.requiresRole)) {
        // User authenticated but lacks required role
        // Note: hasRole() checks hierarchical permissions
        alert(`Access denied. Role '${to.meta.requiresRole}' required.`)
        next('/')
        return
      }
    }
  }
  
  next()
})

export default router