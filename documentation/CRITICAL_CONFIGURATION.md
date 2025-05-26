# Critical Configuration Notes

This document contains critical configuration requirements that must be followed for the SSO POC to work correctly.

**LAST VERIFIED**: 2025-05-26 - Both SAML and OIDC apps working with all roles properly transmitted

## SAML Configuration

### 1. Client ID Matching
**CRITICAL**: The SAML client ID in Keycloak MUST match the SP entity ID exactly.

- Keycloak SAML Client ID: `http://localhost:3000`
- SP Entity ID (in settings.json): `http://localhost:3000`

These must be EXACTLY the same, including protocol and port.

### 2. SAML URLs
The following URLs must be correctly configured:
- Assertion Consumer Service URL: `http://localhost:3000/saml/callback`
- Single Logout Service URL: `http://localhost:3000/saml/sls`

### 3. SAML Signatures
- Assertion signatures are enabled for security
- Client signatures are disabled (SP doesn't sign requests)
- Server signatures are enabled

### 4. Role Mapping
**IMPORTANT**: Role mapping is enabled for SAML authentication.
- The SAML client includes a role-list mapper that sends roles as a 'userRoles' attribute
- Users have been assigned realm roles (admin, editor, viewer) in Keycloak
- The backend processes these roles for RBAC enforcement

**CRITICAL FIX**: The SAML backend must handle multiple attributes with the same name. Keycloak sends each role as a separate `<saml:Attribute>` element with name="userRoles". The backend code in `app.py` (lines 170-184) must aggregate these properly.

### 5. X509 Certificate Updates
**CRITICAL**: When Keycloak is recreated, its X509 certificate changes. You must:
1. Get the new certificate: 
   ```bash
   curl -s http://localhost:8080/realms/sso-poc/protocol/saml/descriptor | grep -o '<ds:X509Certificate>.*</ds:X509Certificate>' | sed 's/<ds:X509Certificate>//g' | sed 's/<\/ds:X509Certificate>//g'
   ```
2. Update `app1-saml/backend/saml/settings.json` with the new certificate
3. Restart the SAML backend: `docker-compose restart app1-saml-backend`

## OIDC Configuration

### 1. Client Configuration
- Client ID: `app2-oidc`
- Client Secret: `secret`
- Redirect URI: `http://localhost:4000/oidc/callback`

### 2. OIDC Endpoints
The OIDC endpoints are automatically discovered via:
`http://localhost:8080/realms/sso-poc/.well-known/openid-configuration`

## Port Mapping

### Critical Port Assignments
- Keycloak: 8080
- SAML Backend: 3000
- SAML Frontend: 3001  
- OIDC Backend: 4000
- OIDC Frontend: 4001

### Nginx Proxy Headers
Both frontend applications use nginx to proxy requests to backends.
Critical headers that must be set:
- `X-Forwarded-Host`: Must include the port (e.g., `localhost:3000`)
- `X-Forwarded-Proto`: Protocol scheme
- `X-Forwarded-For`: Client IP chain

## Session Management

### Flask Sessions
Both applications use Flask's built-in cookie-based sessions:
- No external session storage required
- Session cookies are HTTP-only for security
- Different cookie names: `saml_session` vs `oidc_session`

### Removed Dependencies
Flask-Session and Redis have been removed to avoid compatibility issues.

## Known Limitations

1. **HTTPS**: Not configured (use only for POC/development)
2. **Session Timeout**: Fixed at 1 hour
3. **Single Logout**: Not fully implemented

## Troubleshooting Checklist

If authentication fails:
1. ✓ Check SAML client ID matches exactly
2. ✓ Verify all URLs use correct ports
3. ✓ Ensure Keycloak realm is imported
4. ✓ Check nginx proxy headers are set
5. ✓ Verify backend containers can reach Keycloak
6. ✓ Check browser console for CORS errors

## Docker Build Requirements

When building from scratch:
```bash
# Clean everything
docker-compose down -v

# Build and start
docker-compose up -d --build

# Wait for Keycloak to be ready (1-2 minutes)
# Then test applications
```

The realm will be automatically imported on first startup.

## Critical Code Changes Made

### 1. SAML Backend Role Parsing (`app1-saml/backend/app.py`)
Added code to handle multiple SAML attributes with the same name (lines 179-184):
```python
else:
    # Handle multiple attributes with same name (e.g., roles)
    if isinstance(attributes[name], list):
        attributes[name].extend(values)
    else:
        attributes[name] = [attributes[name]] + values
```

### 2. Keycloak Realm Configuration (`keycloak/realms/sso-poc-realm.json`)
Updated SAML role mapper configuration (lines 192-198):
```json
"config": {
    "single": "false",
    "attribute.nameformat": "Basic",
    "attribute.name": "userRoles",
    "full.path": "false",
    "friendly.name": "userRoles"
}
```

## Testing Verification

1. **SAML App (http://localhost:3001)**:
   - Login with admin_user/password123
   - Should see roles: admin, editor, viewer
   
2. **OIDC App (http://localhost:4001)**:
   - Login with admin_user/password123
   - Should see roles: admin, editor, viewer

3. **Role-based Access**:
   - Admin page: Only accessible by admin_user
   - Editor page: Accessible by admin_user and editor_user
   - Protected page: Accessible by all authenticated users