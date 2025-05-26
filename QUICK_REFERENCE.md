# SSO POC Quick Reference

## Service Ports
| Service | Internal Port | External Port | URL |
|---------|--------------|---------------|-----|
| Keycloak | 8080 | 8080 | http://localhost:8080 |
| SAML Backend | 5000 | 3000 | http://localhost:3000 |
| SAML Frontend | 80 | 3001 | http://localhost:3001 |
| OIDC Backend | 5000 | 4000 | http://localhost:4000 |
| OIDC Frontend | 80 | 4001 | http://localhost:4001 |
| PostgreSQL | 5432 | - | Internal only |

## Critical URLs

### SAML Application
- Login: http://localhost:3001 → /saml/login → Keycloak → /saml/callback → http://localhost:3001
- Logout: http://localhost:3001 → http://localhost:3000/saml/logout → Keycloak → /saml/sls → http://localhost:3001

### OIDC Application
- Login: http://localhost:4001 → /oidc/login → Keycloak → /oidc/callback → http://localhost:4001
- Logout: http://localhost:4001 → http://localhost:4000/oidc/logout → Keycloak → http://localhost:4001

## Docker Commands
```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f [service-name]

# Restart service
docker-compose restart [service-name]

# Stop everything
docker-compose down

# Full rebuild
docker-compose down -v && docker-compose up -d --build
```

## Test Users
| Username | Password | Roles |
|----------|----------|-------|
| admin_user | password123 | admin, editor, viewer |
| editor_user | password123 | editor, viewer |
| viewer_user | password123 | viewer |

## Key Configuration Files
- `docker-compose.yml` - Service definitions
- `keycloak/realms/sso-poc-realm.json` - Realm config
- `app1-saml/backend/saml/settings.json` - SAML config
- `*/frontend/src/auth.js` - Frontend auth config

## Environment Variables
```bash
# Keycloak
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=admin

# SAML App
SAML_SP_ENTITY_ID=http://localhost:3000
SAML_IDP_ENTITY_ID=http://localhost:8080/realms/sso-poc

# OIDC App
OIDC_CLIENT_ID=app2-oidc
OIDC_CLIENT_SECRET=secret
OIDC_ISSUER=http://keycloak:8080/realms/sso-poc
OIDC_ISSUER_PUBLIC=http://localhost:8080/realms/sso-poc
```

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| SAML logout error | Check session attributes are stored |
| OIDC invalid redirect | Configure post-logout URIs (see BUILD_AND_DEPLOY.md) |
| CORS errors | Check backend CORS origins match frontend ports |
| Keycloak not starting | Wait 30s, check postgres is running |
| Login loop | Clear browser cookies, check URLs consistency |