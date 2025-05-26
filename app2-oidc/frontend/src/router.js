import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Protected from './views/Protected.vue'
import Admin from './views/Admin.vue'
import Editor from './views/Editor.vue'
import { auth } from './auth'

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

router.beforeEach(async (to, from, next) => {
  // Check auth status if not already loaded
  if (auth.state.isLoading) {
    await auth.checkAuth()
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!auth.state.isAuthenticated) {
      // Redirect to login
      auth.login()
      return
    }
    
    // Check if route requires specific role
    if (to.meta.requiresRole) {
      if (!auth.hasRole(to.meta.requiresRole)) {
        // User doesn't have required role
        alert(`Access denied. Role '${to.meta.requiresRole}' required.`)
        next('/')
        return
      }
    }
  }
  
  next()
})

export default router