# Detailed Setup Guide

## Quick Start

If you have Docker and Docker Compose already installed:

```bash
# Clone or download the project
cd sso-poc

# Start all services
docker-compose up -d

# Wait for services to start (about 1-2 minutes)
# Then access:
# - Keycloak: http://localhost:8080 (admin/admin)
# - SAML App: http://localhost:3001
# - OIDC App: http://localhost:4001
```

## Prerequisites Installation

### 1. Docker Desktop for Windows

1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Restart your computer when prompted
4. Start Docker Desktop
5. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

### 2. Node.js

1. Download Node.js from [https://nodejs.org/](https://nodejs.org/)
2. Choose the LTS version
3. Run the installer
4. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### 3. Git (Optional but recommended)

1. Download Git from [https://git-scm.com/](https://git-scm.com/)
2. Run the installer
3. Verify installation:
   ```bash
   git --version
   ```

## Docker Architecture

The project uses a multi-container architecture with the following services:

1. **Keycloak** (sso-keycloak)
   - Identity Provider supporting SAML and OIDC
   - Uses PostgreSQL for persistence
   - Automatically imports realm configuration on startup

2. **PostgreSQL** (sso-postgres)
   - Database for Keycloak
   - Data persisted in Docker volume

3. **App1-SAML** 
   - Backend (sso-app1-saml-backend): Python Flask with python3-saml (port 3000)
   - Frontend (sso-app1-saml-frontend): Vue.js served by Nginx (port 3001)
   - Frontend is built during Docker image creation

4. **App2-OIDC**
   - Backend (sso-app2-oidc-backend): Python Flask with OIDC support (port 4000)
   - Frontend (sso-app2-oidc-frontend): Vue.js served by Nginx (port 4001)
   - Frontend is built during Docker image creation

All services communicate through a Docker network called `sso-network`.

## Step-by-Step Setup

### Step 1: Prepare the Environment

1. Open a terminal (Command Prompt or PowerShell)
2. Navigate to your desired directory
3. Create and enter the project directory:
   ```bash
   mkdir sso-poc
   cd sso-poc
   ```

### Step 2: Set Up the Project Files

Copy all project files to your `sso-poc` directory. The structure should look like:
```
sso-poc/
├── docker-compose.yml
├── app1-saml/
├── app2-oidc/
├── keycloak/
└── documentation/
```

### Step 3: Frontend Applications

The frontend applications are built automatically during the Docker build process. No manual build steps are required.

### Step 4: Configure SAML Certificate (Optional)

For production use, you should generate proper certificates. For this PoC, we'll use Keycloak's default certificates.

### Step 5: Start Docker Services

```bash
docker-compose up -d
```

This command will:
- Download required Docker images
- Build the application images (including frontend builds)
- Create a network for the services
- Start PostgreSQL, Keycloak, App1-SAML, and App2-OIDC
- Automatically import the SSO realm configuration

Note: The first run may take several minutes as it builds all images and installs dependencies.

### Step 6: Verify Services are Running

```bash
docker-compose ps
```

All services should show as "Up".

### Step 7: Wait for Keycloak Initialization

Keycloak takes 30-60 seconds to start. Check its status:

```bash
curl http://localhost:8080/health/ready
```

When ready, you'll see a JSON response with `"status": "UP"`.

### Step 8: Verify Realm Import

The Keycloak realm is automatically imported during startup. To verify:

1. Open Keycloak Admin Console: http://localhost:8080
2. Login with admin/admin
3. Click on the realm dropdown (top-left)
4. You should see "sso-poc" realm listed

If the realm is missing, you can import it manually:
```bash
docker cp keycloak/realms/sso-poc-realm.json sso-keycloak:/tmp/
docker exec sso-keycloak /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin
docker exec sso-keycloak /opt/keycloak/bin/kcadm.sh create realms -f /tmp/sso-poc-realm.json
```

### Step 9: Update SAML Configuration

After Keycloak starts, we need to get its SAML certificate:

1. Access Keycloak Admin Console
2. Select the "sso-poc" realm
3. Go to Realm Settings → Keys
4. Click on the RSA certificate
5. Copy the certificate
6. Update `app1-saml/backend/saml/settings.json` with the certificate in the `idp.x509cert` field

### Step 10: Restart Applications (if needed)

If you updated the SAML certificate:
```bash
docker-compose restart app1-saml
```

## Verification Steps

### 1. Check Keycloak
- Navigate to http://localhost:8080
- Login with admin/admin
- Switch to "sso-poc" realm
- Verify users and clients exist

### 2. Test SAML Application
- Navigate to http://localhost:3001
- Click "Login with SAML"
- Login with a test user
- Verify user information is displayed

### 3. Test OIDC Application
- Navigate to http://localhost:4001
- Click "Login with OIDC"
- Should be already logged in (SSO)
- Verify user information is displayed

### 4. Test Role-Based Access
- Try accessing /admin, /editor pages
- Verify access based on user roles

## Common Issues and Solutions

### Issue: Port conflicts
**Solution**: Change ports in docker-compose.yml if needed

### Issue: Keycloak won't start
**Solution**: Increase Docker memory to at least 4GB

### Issue: docker-compose.yml version warning
**Solution**: This warning can be ignored. The `version` field is obsolete in newer Docker Compose versions.

### Issue: xmlsec library version mismatch in app1-saml-backend
**Error**: `xmlsec.InternalError: (-1, 'lxml & xmlsec libxml2 library version mismatch')`
**Solution**: This is already fixed in the Dockerfile, but if it occurs:
1. Rebuild the container: `docker-compose build --no-cache app1-saml-backend`
2. Restart: `docker-compose up -d app1-saml-backend`

### Issue: npm ci fails in frontend builds
**Error**: `The npm ci command can only install with an existing package-lock.json`
**Solution**: The Dockerfiles now use `npm install` instead of `npm ci`

### Issue: Frontend dist folder not found
**Error**: `failed to compute cache key: "/frontend/dist": not found`
**Solution**: Frontend builds are now handled in the frontend Dockerfiles automatically

### Issue: SAML login fails
**Solution**: Check SAML certificate configuration in `app1-saml/backend/saml/settings.json`

### Issue: OIDC redirect fails
**Solution**: Verify redirect URIs match exactly in Keycloak client configuration

## Development Mode

For development with hot-reload:

### SAML App:
```bash
# Terminal 1 - Backend
cd app1-saml/backend
python app.py

# Terminal 2 - Frontend
cd app1-saml/frontend
npm run dev
```

### OIDC App:
```bash
# Terminal 1 - Backend
cd app2-oidc/backend
python app.py

# Terminal 2 - Frontend
cd app2-oidc/frontend
npm run dev
```

## Cleanup

To stop and remove all services:
```bash
docker-compose down -v
```

This removes containers, networks, and volumes.