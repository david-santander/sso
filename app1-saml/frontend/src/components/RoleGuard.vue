<template>
  <!-- Renders children only if user has required role -->
  <div v-if="hasRole">
    <slot></slot>
  </div>
  <!-- Optionally shows fallback content for unauthorized users -->
  <div v-else-if="showFallback">
    <slot name="fallback">
      <!-- Default fallback message if no custom fallback provided -->
      <div class="alert alert-warning">
        You don't have permission to view this content.
      </div>
    </slot>
  </div>
</template>

<script>
/**
 * @component RoleGuard
 * @description Conditional rendering component based on user roles
 * 
 * This component provides client-side role-based content protection:
 * - Renders content only if user has required role(s)
 * - Supports single role or array of roles
 * - Includes role hierarchy checking (admin > editor > viewer)
 * - Optionally displays fallback content for unauthorized users
 * 
 * Security note: This is CLIENT-SIDE protection only and should
 * always be paired with server-side authorization checks. Never
 * rely solely on client-side guards for sensitive operations.
 * 
 * Usage examples:
 * <RoleGuard role="admin">
 *   <AdminContent />
 * </RoleGuard>
 * 
 * <RoleGuard :role="['admin', 'editor']" :show-fallback="true">
 *   <EditorContent />
 *   <template #fallback>
 *     <CustomUnauthorizedMessage />
 *   </template>
 * </RoleGuard>
 */
import { auth } from '../auth'

export default {
  name: 'RoleGuard',
  props: {
    /**
     * Required role(s) to display content
     * Can be a single string or array of strings
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
     * Checks if current user has any of the required roles
     * Uses auth service which includes hierarchical role checking
     * 
     * @returns {boolean} True if user has required role(s)
     */
    hasRole() {
      const requiredRoles = Array.isArray(this.role) ? this.role : [this.role]
      // Using auth.hasRole which includes hierarchy check
      // This means admin users can see content requiring editor/viewer roles
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