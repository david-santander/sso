import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Protected from './views/Protected.vue'
import Admin from './views/Admin.vue'
import Editor from './views/Editor.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/protected',
    name: 'Protected',
    component: Protected
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/editor',
    name: 'Editor',
    component: Editor
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router