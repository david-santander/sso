# SSO POC Build and Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- Ports available: 3000, 3001, 4000, 4001, 8080
- At least 4GB RAM available for containers

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd sso

# Build and start all services
docker-compose up -d --build

# Wait for Keycloak to be ready (about 30 seconds)
# Check Keycloak logs
docker logs sso-keycloak -f

# Verify all services are running
docker-compose ps
```

## Service URLs

### Applications
- **SAML App Frontend**: http://localhost:3001
- **SAML App Backend**: http://localhost:3000
- **OIDC App Frontend**: http://localhost:4001
- **OIDC App Backend**: http://localhost:4000
- **Keycloak Admin Console**: http://localhost:8080

### Test Credentials
- **Keycloak Admin**: admin / admin
- **Test Users**:
  - admin_user / password123 (roles: admin, editor, viewer)
  - editor_user / password123 (roles: editor, viewer)
  - viewer_user / password123 (role: viewer)

## Configuration Details

### SAML Application (App1)
- **Entity ID**: http://localhost:3000
- **ACS URL**: http://localhost:3000/saml/callback
- **SLS URL**: http://localhost:3000/saml/sls
- **Frontend redirects to backend**: http://localhost:3000/saml/logout

### OIDC Application (App2)
- **Client ID**: app2-oidc
- **Client Secret**: secret
- **Redirect URI**: http://localhost:4000/oidc/callback
- **Post-Logout Redirect**: http://localhost:4001
- **Frontend redirects to backend**: http://localhost:4000/oidc/logout

## Important Configuration Files

### 1. docker-compose.yml
- Defines all services, ports, networks, and volumes
- Environment variables for all services
- Service dependencies and health checks

### 2. keycloak/realms/sso-poc-realm.json
- Realm configuration
- User definitions and roles
- SAML and OIDC client configurations
- **Note**: Post-logout redirect URIs for OIDC must be configured after first startup

### 3. app1-saml/backend/saml/settings.json
- SAML SP configuration
- IdP metadata (URLs and certificate)
- Binding configurations

### 4. Frontend auth.js files
- Authentication logic
- Backend API endpoints
- Login/logout URLs

## Post-Deployment Configuration

### OIDC Post-Logout Configuration
The OIDC client needs post-logout redirect URIs configured:

```bash
# Get Keycloak admin CLI ready
docker exec sso-keycloak /opt/keycloak/bin/kcadm.sh config credentials \
  --server http://localhost:8080 --realm master --user admin --password admin

# Get OIDC client ID
CLIENT_ID=$(docker exec sso-keycloak /opt/keycloak/bin/kcadm.sh get clients \
  -r sso-poc --fields id,clientId | jq -r '.[] | select(.clientId=="app2-oidc") | .id')

# Update post-logout redirect URIs
echo '{"attributes":{"post.logout.redirect.uris":"http://localhost:4001/*"}}' | \
  docker exec -i sso-keycloak /opt/keycloak/bin/kcadm.sh update clients/$CLIENT_ID \
  -r sso-poc -f -
```

## Troubleshooting

### Common Issues

1. **Keycloak not starting**: Check PostgreSQL is running and accessible
2. **Login redirects fail**: Verify all URLs use localhost, not internal hostnames
3. **SAML logout fails**: Ensure session attributes are properly stored
4. **OIDC logout fails**: Check post-logout redirect URIs are configured
5. **CORS errors**: Verify frontend URLs in backend CORS configuration

### Debugging Commands

```bash
# View logs
docker-compose logs -f [service-name]

# Check service health
docker-compose ps

# Restart a specific service
docker-compose restart [service-name]

# Rebuild a specific service
docker-compose up -d --build [service-name]

# Access container shell
docker exec -it [container-name] /bin/bash
```

### Clean Rebuild

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: Deletes all data)
docker-compose down -v

# Rebuild everything
docker-compose up -d --build
```

## Network Architecture

```
User Browser
    |
    ├─> localhost:3001 (SAML Frontend) ──> localhost:3000 (SAML Backend)
    |                                             |
    ├─> localhost:4001 (OIDC Frontend) ──> localhost:4000 (OIDC Backend)
    |                                             |
    └─> localhost:8080 (Keycloak) <─────────────┘
              |
              └─> postgres:5432 (Database)
```

## Security Considerations

1. **Change all default passwords** before production use
2. **Update SECRET_KEY** in all applications
3. **Enable HTTPS** for production deployments
4. **Review CORS policies** for production domains
5. **Secure PostgreSQL** with strong credentials
6. **Update Keycloak admin** credentials

## Maintenance

### Backup Keycloak Data
```bash
# Export realm configuration
docker exec sso-keycloak /opt/keycloak/bin/kc.sh export \
  --dir /tmp --realm sso-poc

# Copy to host
docker cp sso-keycloak:/tmp/sso-poc-realm.json ./backup/
```

### Update Keycloak Realm
1. Modify `keycloak/realms/sso-poc-realm.json`
2. Restart Keycloak: `docker-compose restart keycloak`
3. Or import manually through admin console

## Testing

### Test SAML Flow
1. Navigate to http://localhost:3001
2. Click "Login with SAML"
3. Authenticate with test credentials
4. Verify roles are displayed correctly
5. Test logout functionality

### Test OIDC Flow
1. Navigate to http://localhost:4001
2. Click "Login with OIDC"
3. Authenticate with test credentials
4. Verify roles are displayed correctly
5. Test logout functionality

### Test Role-Based Access
- Admin pages require admin role
- Editor pages require editor role (admin users also have access)
- Protected pages require any authenticated user