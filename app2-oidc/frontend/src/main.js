import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { auth } from './auth'

// Check authentication status on app startup
auth.checkAuth()

createApp(App).use(router).mount('#app')