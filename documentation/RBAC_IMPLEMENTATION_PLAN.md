# Comprehensive Role-Based Access Control (RBAC) Implementation Plan

## Executive Summary
This document outlines a comprehensive plan to implement Role-Based Access Control (RBAC) across both SAML and OIDC applications in the SSO POC system. The plan addresses authentication, authorization, role management, and enforcement at both backend and frontend levels.

## Current State Analysis

### What's Working
1. **OIDC Application**: Full RBAC implementation with role extraction from JWT tokens
2. **Keycloak Configuration**: Three users with predefined roles (admin, editor, viewer)
3. **Backend Decorators**: `require_auth` and `require_role` decorators exist in both apps
4. **Session Management**: Both apps maintain user sessions with authentication state

### Gaps to Address
1. **SAML Application**: No role extraction or enforcement (returns 403 for all role checks)
2. **Frontend Protection**: No client-side route guards or role-based UI rendering
3. **Role Mapping**: SAML attributes don't include role information
4. **Consistency**: Different role handling between SAML and OIDC apps

## Implementation Plan

### Phase 1: SAML Role Integration (Priority: High)

#### 1.1 Configure Keycloak SAML Client
- Add role list mapper to SAML client configuration
- Map realm roles to SAML attributes
- Configure attribute name as "roles" or "Role"

**Implementation Steps:**
1. Update Keycloak realm configuration
2. Add SAML protocol mapper for roles
3. Configure role attribute format (single vs multi-valued)

#### 1.2 Update SAML Backend
- Modify `app1-saml/backend/app.py` to extract roles from SAML response
- Store roles in session during authentication
- Enable the `require_role` decorator functionality

**Code Changes Required:**
```python
# In saml_callback function
roles = attributes.get('roles', []) or attributes.get('Role', [])
session['roles'] = roles if isinstance(roles, list) else [roles]

# Update require_role decorator to check session['roles']
```

#### 1.3 Update SAML Settings
- Modify `saml/settings.json` to include role attribute mapping
- Ensure attribute consumption service includes role attribute

### Phase 2: Frontend Route Protection (Priority: High)

#### 2.1 Implement Vue Router Guards
- Create authentication middleware for route protection
- Add role-based access control to routes
- Implement redirect logic for unauthorized access

**Components to Create:**
1. `auth.js` - Authentication state management
2. `router-guards.js` - Navigation guards
3. `roleCheck.js` - Role validation utilities

#### 2.2 Add Role-Based UI Rendering
- Create `v-if` directives for role-based content
- Hide/show navigation items based on user roles
- Display user roles in the UI

#### 2.3 Centralize Auth State
- Create Vuex store or Pinia store for auth state
- Persist user info and roles
- Handle token/session expiration

### Phase 3: Enhanced Authorization Features (Priority: Medium)

#### 3.1 Hierarchical Roles
- Implement role hierarchy (admin > editor > viewer)
- Create role inheritance logic
- Update authorization checks to support hierarchy

#### 3.2 Resource-Level Permissions
- Add resource-specific permissions
- Implement permission checking beyond roles
- Create permission management interface

#### 3.3 Dynamic Role Assignment
- API endpoints for role management
- Admin interface for user role assignment
- Audit logging for role changes

### Phase 4: Security Enhancements (Priority: Medium)

#### 4.1 Token Management
- Implement token refresh for OIDC
- Add token validation middleware
- Handle token expiration gracefully

#### 4.2 Session Security
- Add CSRF protection
- Implement session timeout
- Secure session cookies (httpOnly, secure flags)

#### 4.3 API Security
- Add rate limiting
- Implement API key authentication for service-to-service
- Add request validation and sanitization

### Phase 5: Monitoring and Compliance (Priority: Low)

#### 5.1 Audit Logging
- Log all authentication attempts
- Track authorization decisions
- Record role changes and access patterns

#### 5.2 Compliance Features
- Add consent management
- Implement data access policies
- Create compliance reports

#### 5.3 Monitoring Dashboard
- Real-time authentication metrics
- Failed access attempt alerts
- Role usage analytics

## Technical Implementation Details

### Backend Changes

#### SAML Application Updates
```python
# Extract roles from SAML response
def extract_roles_from_saml(attributes):
    roles = []
    role_attrs = ['roles', 'Role', 'memberOf', 'groups']
    
    for attr in role_attrs:
        if attr in attributes:
            attr_value = attributes[attr]
            if isinstance(attr_value, list):
                roles.extend(attr_value)
            else:
                roles.append(attr_value)
    
    return list(set(roles))  # Remove duplicates

# Update session with roles
session['roles'] = extract_roles_from_saml(attributes)
```

#### Unified Role Checking
```python
def check_user_role(required_role):
    user_roles = session.get('roles', [])
    
    # Check direct role
    if required_role in user_roles:
        return True
    
    # Check hierarchical roles
    role_hierarchy = {
        'admin': ['editor', 'viewer'],
        'editor': ['viewer']
    }
    
    for user_role in user_roles:
        if required_role in role_hierarchy.get(user_role, []):
            return True
    
    return False
```

### Frontend Implementation

#### Vue Router Guards
```javascript
// router-guards.js
export function requireAuth(to, from, next) {
    const isAuthenticated = store.getters['auth/isAuthenticated'];
    
    if (!isAuthenticated) {
        next({ name: 'login', query: { redirect: to.fullPath } });
    } else {
        next();
    }
}

export function requireRole(role) {
    return (to, from, next) => {
        const userRoles = store.getters['auth/userRoles'];
        
        if (userRoles.includes(role)) {
            next();
        } else {
            next({ name: 'forbidden' });
        }
    };
}
```

#### Role-Based Components
```vue
<!-- RoleGuard.vue -->
<template>
  <div v-if="hasRole">
    <slot></slot>
  </div>
  <div v-else-if="showFallback">
    <slot name="fallback">
      <p>You don't have permission to view this content.</p>
    </slot>
  </div>
</template>

<script>
export default {
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
      const userRoles = this.$store.getters['auth/userRoles'];
      const requiredRoles = Array.isArray(this.role) ? this.role : [this.role];
      return requiredRoles.some(role => userRoles.includes(role));
    }
  }
}
</script>
```

### Keycloak Configuration

#### SAML Role Mapper Configuration
```json
{
  "name": "role-list",
  "protocol": "saml",
  "protocolMapper": "saml-role-list-mapper",
  "config": {
    "single": "false",
    "attribute.nameformat": "Basic",
    "attribute.name": "roles"
  }
}
```

## Testing Strategy

### Unit Tests
1. Test role extraction logic
2. Test authorization decorators
3. Test frontend route guards

### Integration Tests
1. Test SAML login with role assignment
2. Test OIDC login with role assignment
3. Test cross-application role consistency

### End-to-End Tests
1. Test complete authentication flows
2. Test role-based access scenarios
3. Test unauthorized access handling

## Deployment Considerations

### Environment Variables
```bash
# Add to .env files
RBAC_ENABLED=true
ROLE_HIERARCHY_ENABLED=true
AUDIT_LOGGING_ENABLED=true
SESSION_TIMEOUT=1800
```

### Database Schema
- User roles table
- Role permissions table
- Audit log table
- Session storage

### Performance Considerations
- Cache role checks
- Optimize session storage
- Implement lazy loading for permissions

## Security Best Practices

1. **Principle of Least Privilege**: Users get minimum required roles
2. **Defense in Depth**: Check roles at multiple layers
3. **Audit Everything**: Log all security-relevant events
4. **Regular Reviews**: Periodic role and permission audits
5. **Secure by Default**: Deny access unless explicitly granted

## Timeline and Milestones

### Week 1-2: Phase 1 - SAML Role Integration
- Configure Keycloak SAML mappers
- Update SAML backend code
- Test role extraction

### Week 3-4: Phase 2 - Frontend Protection
- Implement Vue Router guards
- Add role-based UI components
- Create auth state management

### Week 5-6: Phase 3 - Enhanced Authorization
- Implement role hierarchy
- Add resource permissions
- Create management interfaces

### Week 7-8: Phase 4 - Security Enhancements
- Add token management
- Implement session security
- Enhance API security

### Week 9-10: Phase 5 - Monitoring and Compliance
- Set up audit logging
- Create monitoring dashboard
- Add compliance features

## Success Metrics

1. **Functional Metrics**
   - 100% role enforcement on protected endpoints
   - Zero unauthorized access incidents
   - < 100ms authorization check latency

2. **Security Metrics**
   - All authentication attempts logged
   - Role changes audited
   - Session security implemented

3. **User Experience Metrics**
   - Seamless role-based navigation
   - Clear unauthorized access messaging
   - Fast page load times with auth checks

## Conclusion

This comprehensive RBAC implementation plan provides a structured approach to adding robust authentication and authorization to the SSO POC system. By following this plan, both SAML and OIDC applications will have consistent, secure, and user-friendly role-based access control.

The phased approach allows for incremental implementation while maintaining system stability. Each phase builds upon the previous one, ultimately creating a production-ready RBAC system that meets enterprise security requirements.