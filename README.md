# SSO PoC: SAML & OIDC with RBAC

## Overview

This project demonstrates Single Sign-On (SSO) functionality using SAML 2.0 and OpenID Connect (OIDC) protocols, including Role-Based Access Control (RBAC). It's designed as an educational tool for architects, developers, and stakeholders to understand these authentication mechanisms.

## Components

- **Keycloak**: Identity Provider supporting both SAML and OIDC
- **App1-SAML**: Python Flask + Vue.js application acting as a SAML Service Provider
- **App2-OIDC**: Python Flask + Vue.js application acting as an OIDC Relying Party
- **PostgreSQL**: Database for Keycloak

## Quick Start

### Prerequisites

- Docker Desktop for Windows
- Git
- Basic understanding of web technologies

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sso-poc
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Wait for Keycloak to start** (takes about 30-60 seconds)
   ```bash
   # Check if Keycloak is ready
   curl http://localhost:8080/health/ready
   ```

4. **Import the realm configuration**
   ```bash
   cd keycloak/scripts
   ./import-realm.sh
   cd ../..
   ```

## Access Points

- **Keycloak Admin Console**: http://localhost:8080
  - Username: `admin`
  - Password: `admin`

- **App1 (SAML SP)**:
  - Frontend: http://localhost:3001
  - Backend API: http://localhost:3000
  
- **App2 (OIDC RP)**:
  - Frontend: http://localhost:4001
  - Backend API: http://localhost:4000

## Test Users

| Username | Password | Email |
|----------|----------|-------|
| admin_user | password | admin@example.com |
| user1 | password | user1@example.com |

**Note**: Role-based access control has been disabled in this POC to avoid SAML attribute conflicts.

## Testing SSO Flows

### SAML Flow (App1)

1. Navigate to http://localhost:3001
2. Click "Login with SAML"
3. Login with one of the test users
4. You'll be redirected back to App1 with user information displayed

### OIDC Flow (App2)

1. Navigate to http://localhost:4001
2. Click "Login with OIDC"
3. Login with one of the test users (if not already logged in)
4. You'll be redirected back to App2 with user information displayed
5. Access role-based resources based on your user's roles

### SSO Experience

1. Login to App1 (SAML)
2. Navigate to App2 (OIDC) - you should be automatically authenticated
3. This demonstrates SSO across different protocols

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Browser   │────▶│  App1-SAML   │────▶│   Keycloak   │
│             │◀────│  (Port 5001) │◀────│  (Port 8080) │
└─────────────┘     └──────────────┘     └──────────────┘
       │                                          ▲
       │            ┌──────────────┐              │
       └───────────▶│  App2-OIDC   │──────────────┘
                    │  (Port 5002) │
                    └──────────────┘
```

## Role-Based Access Control

Each application has the following protected endpoints:

- `/protected` - Requires authentication
- `/admin` - Requires 'admin' role
- `/editor` - Requires 'editor' role

## Key Differences: SAML vs OIDC

| Aspect | SAML | OIDC |
|--------|------|------|
| Protocol | XML-based | JSON/REST-based |
| Token Format | XML Assertions | JWT (JSON Web Tokens) |
| Complexity | More complex | Simpler |
| Use Cases | Enterprise, Legacy | Modern web, Mobile |
| Flow | POST/Redirect bindings | Authorization Code flow |

## Troubleshooting

1. **Keycloak not starting**: Ensure Docker has enough memory (at least 4GB)
2. **Realm import fails**: Wait longer for Keycloak to fully start
3. **Login redirects fail**: Check that all URLs use `localhost` consistently
4. **Vue.js build errors**: Ensure Node.js is installed and up to date

## Critical Configuration

⚠️ **IMPORTANT**: Please read [CRITICAL_CONFIGURATION.md](documentation/CRITICAL_CONFIGURATION.md) for essential configuration requirements, especially regarding:
- SAML client ID matching
- Port configurations
- Session management changes

## Project Structure

```
sso-poc/
├── docker-compose.yml
├── app1-saml/
│   ├── backend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── saml/
│   └── frontend/
│       └── (Vue.js app)
├── app2-oidc/
│   ├── backend/
│   │   ├── app.py
│   │   └── requirements.txt
│   └── frontend/
│       └── (Vue.js app)
├── keycloak/
│   ├── realms/
│   │   └── sso-poc-realm.json
│   └── scripts/
└── documentation/
```

## Next Steps

- Explore the Keycloak admin console to understand IdP configuration
- Modify user roles and test access control
- Review the application code to understand SAML/OIDC integration
- Check the browser developer tools to see the authentication flows

## Additional Resources

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [SAML 2.0 Specification](https://docs.oasis-open.org/security/saml/v2.0/)
- [OpenID Connect Specification](https://openid.net/connect/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vue.js Documentation](https://vuejs.org/)