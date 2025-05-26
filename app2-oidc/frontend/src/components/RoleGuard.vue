<!--
  RoleGuard Component - Conditional rendering based on user roles
  
  This component provides declarative role-based content control:
  - Wraps content that should only be visible to certain roles
  - Supports single role or array of roles
  - Uses hierarchical role checking from auth service
  - Optionally shows fallback content for unauthorized users
  
  Usage examples:
  <RoleGuard role="admin">
    <AdminOnlyContent />
  </RoleGuard>
  
  <RoleGuard :role="['admin', 'editor']" :show-fallback="true">
    <EditorContent />
    <template #fallback>
      <CustomUnauthorizedMessage />
    </template>
  </RoleGuard>
-->
<template>
  <div v-if="hasRole">
    <!-- Render wrapped content if user has required role -->
    <slot></slot>
  </div>
  <div v-else-if="showFallback">
    <!-- Show fallback content if configured and user lacks role -->
    <slot name="fallback">
      <div class="alert alert-warning">
        You don't have permission to view this content.
      </div>
    </slot>
  </div>
</template>

<script>
import { auth } from '../auth'

/**
 * RoleGuard component for declarative role-based rendering
 * 
 * Features:
 * - Integrates with auth service for role checking
 * - Supports hierarchical roles (admin > editor > viewer)
 * - Can check for single role or any of multiple roles
 * - Optional fallback content for better UX
 * 
 * Security note:
 * - This is UI-only protection for better UX
 * - Always enforce authorization on backend APIs
 * - Frontend role checks can be bypassed by users
 */
export default {
  name: 'RoleGuard',
  props: {
    /**
     * Required role(s) to view content
     * Can be a single role string or array of roles
     * If array, user needs at least one of the roles
     */
    role: {
      type: [String, Array],
      required: true
    },
    /**
     * Whether to show fallback content for unauthorized users
     * If false, nothing is rendered for unauthorized users
     */
    showFallback: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    /**
     * Check if current user has required role(s)
     * Uses auth service which implements role hierarchy
     * @returns {boolean}
     */
    hasRole() {
      const requiredRoles = Array.isArray(this.role) ? this.role : [this.role]
      // Check if user has at least one of the required roles
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