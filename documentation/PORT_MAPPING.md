# Port Mapping Guide

## Overview

This document details the port mapping strategy for the SSO POC applications. The ports are organized to be intuitive and easy to remember.

## Port Assignments

### Identity Provider
- **Keycloak**: `8080`
  - Admin Console: http://localhost:8080
  - SAML Endpoint: http://localhost:8080/realms/sso-poc/protocol/saml
  - OIDC Endpoint: http://localhost:8080/realms/sso-poc

### Application 1 - SAML
- **Backend API**: `3000`
  - SAML SSO endpoint: http://localhost:3000/saml/login
  - SAML callback: http://localhost:3000/saml/callback
  - API endpoints: http://localhost:3000/api/*
  
- **Frontend**: `3001`
  - Main application: http://localhost:3001
  - Proxies `/saml/*` requests to backend port 3000
  - Proxies `/api/*` requests to backend port 3000

### Application 2 - OIDC
- **Backend API**: `4000`
  - OIDC login endpoint: http://localhost:4000/oidc/login
  - OIDC callback: http://localhost:4000/oidc/callback
  - API endpoints: http://localhost:4000/api/*
  
- **Frontend**: `4001`
  - Main application: http://localhost:4001
  - Proxies `/oidc/*` requests to backend port 4000
  - Proxies `/api/*` requests to backend port 4000

## Port Mapping Logic

The port assignment follows a logical pattern:

1. **Keycloak** uses the standard port `8080`
2. **SAML Application** uses the `3xxx` range:
   - Backend: `3000`
   - Frontend: `3001`
3. **OIDC Application** uses the `4xxx` range:
   - Backend: `4000`
   - Frontend: `4001`

This makes it easy to identify which application you're working with based on the port number.

## Docker Network

All containers communicate internally through the `sso-network` Docker network using container names:
- `sso-keycloak`
- `sso-postgres`
- `sso-app1-saml-backend`
- `sso-app1-saml-frontend`
- `sso-app2-oidc-backend`
- `sso-app2-oidc-frontend`

## Development Access

When developing locally:
1. Access frontends through their public ports (3001, 4001)
2. Backend APIs are accessible directly for testing (3000, 4000)
3. All authentication flows go through the frontend nginx proxy

### Default Credentials
- **Keycloak Admin**: Username: `admin`, Password: `admin`
- **Test User 1**: Username: `user1`, Password: `password` (has viewer role)
- **Test Admin**: Username: `admin`, Password: `password` (has admin and editor roles)

## Important Configuration Notes

### SAML Configuration
- **CRITICAL**: The SAML client ID in Keycloak must be `http://localhost:3000` (matching the SP entity ID)
- SAML signatures are disabled for this POC
- The Flask backend handles X-Forwarded-Host headers from nginx to generate correct SAML URLs
- AssertionConsumerService URL: `http://localhost:3000/saml/callback`

### OIDC Configuration
- Client ID: `app2-oidc`
- Client Secret: `secret`
- Redirect URI: `http://localhost:4000/oidc/callback`
- Standard authorization code flow is used

### Nginx Proxy Headers
Both frontend nginx configurations include:
- `X-Forwarded-Host`: Includes the port number (e.g., `$host:3000`)
- `X-Forwarded-Proto`: Protocol scheme
- `X-Forwarded-For`: Client IP chain
- `X-Real-IP`: Original client IP

## Troubleshooting

### Port Conflicts
If you encounter port conflicts:
1. Check if the ports are already in use: `netstat -an | grep -E '(3000|3001|4000|4001|8080)'`
2. Stop conflicting services or modify the port mappings in `docker-compose.yml`
3. Remember to update corresponding configurations in:
   - Keycloak client settings
   - Application configuration files
   - Nginx proxy headers

### SAML Authentication Issues
If SAML authentication fails with "Invalid Request" or "Client not found":
1. Verify the SAML client ID in Keycloak matches exactly: `http://localhost:3000`
2. Check that the SP entity ID in `settings.json` matches the client ID
3. Ensure the AssertionConsumerService URL is correct
4. Check Keycloak logs: `docker-compose logs keycloak | grep -E "(ERROR|WARN)"`

### OIDC Authentication Issues
If OIDC authentication fails:
1. Verify the client secret matches between Keycloak and the application
2. Check redirect URI configuration
3. Ensure the client is enabled in Keycloak