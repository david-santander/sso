<template>
  <div v-if="hasRole">
    <slot></slot>
  </div>
  <div v-else-if="showFallback">
    <slot name="fallback">
      <div class="alert alert-warning">
        You don't have permission to view this content.
      </div>
    </slot>
  </div>
</template>

<script>
import { auth } from '../auth'

export default {
  name: 'RoleGuard',
  props: {
    role: {
      type: [String, Array],
      required: true
    },
    showFallback: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    hasRole() {
      const requiredRoles = Array.isArray(this.role) ? this.role : [this.role]
      return requiredRoles.some(role => auth.hasRole(role))
    }
  }
}
</script>

<style scoped>
.alert {
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 0.25rem;
}

.alert-warning {
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  color: #856404;
}
</style>