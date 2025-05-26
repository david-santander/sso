"""OIDC Authentication Backend for SSO POC

This module implements OpenID Connect (OIDC) authentication using Authlib.
It provides secure authentication, role-based access control (RBAC), and session management
for the OIDC-based application in the SSO proof of concept.
"""

import os
import json
from flask import Flask, request, redirect, session, jsonify, url_for
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from functools import wraps
import jwt
from jwt import PyJWKClient

# Initialize Flask application
app = Flask(__name__)
# Secret key for session encryption - should be set via environment variable in production
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Configure secure session settings
# Session cookies are used to maintain authentication state
app.config['SESSION_COOKIE_NAME'] = 'oidc_session'  # Custom cookie name for OIDC sessions
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection while allowing IdP redirects
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session timeout: 1 hour

# Enable CORS for frontend application
# In production, origins should be restricted to actual frontend domains
CORS(app, supports_credentials=True, origins=['http://localhost:4001'])

# Initialize OAuth client
oauth = OAuth(app)

# OIDC configuration from environment variables
# OIDC_ISSUER: Internal URL for server-to-server communication
# OIDC_ISSUER_PUBLIC: Public URL for browser redirects
OIDC_CLIENT_ID = os.environ.get('OIDC_CLIENT_ID', 'app2-oidc')
OIDC_CLIENT_SECRET = os.environ.get('OIDC_CLIENT_SECRET', 'secret')
OIDC_ISSUER = os.environ.get('OIDC_ISSUER', 'http://keycloak:8080/realms/sso-poc')
OIDC_ISSUER_PUBLIC = os.environ.get('OIDC_ISSUER_PUBLIC', 'http://localhost:8080/realms/sso-poc')
OIDC_REDIRECT_URI = os.environ.get('OIDC_REDIRECT_URI', 'http://localhost:4000/oidc/callback')

# Configure OAuth with explicit endpoints to avoid metadata discovery issues
# Using explicit endpoints instead of metadata URL for better control and debugging
oidc = oauth.register(
    'oidc',
    client_id=OIDC_CLIENT_ID,
    client_secret=OIDC_CLIENT_SECRET,
    access_token_url=f'{OIDC_ISSUER}/protocol/openid-connect/token',  # Token endpoint (internal)
    authorize_url=f'{OIDC_ISSUER_PUBLIC}/protocol/openid-connect/auth',  # Auth endpoint (public)
    jwks_uri=f'{OIDC_ISSUER}/protocol/openid-connect/certs',  # JWKS endpoint for token validation
    client_kwargs={
        'scope': 'openid email profile roles'  # Request user info and role claims
    }
)

def require_auth(f):
    """
    Decorator to enforce authentication on protected endpoints.
    
    Returns 401 Unauthorized if user is not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def check_role_hierarchy(user_roles, required_role):
    """
    Check if user has required role considering role hierarchy.
    
    Implements hierarchical RBAC where higher roles inherit permissions
    of lower roles (admin > editor > viewer).
    
    Args:
        user_roles: List of roles assigned to the user
        required_role: The role required to access the resource
        
    Returns:
        bool: True if user has required role or a higher role
    """
    # Define role hierarchy - higher roles inherit permissions of lower roles
    role_hierarchy = {
        'admin': ['editor', 'viewer'],  # Admin can do everything editor and viewer can
        'editor': ['viewer'],            # Editor can do everything viewer can
        'viewer': []                     # Viewer has no inherited permissions
    }
    
    # Direct role check
    if required_role in user_roles:
        return True
    
    # Check hierarchical roles
    for user_role in user_roles:
        if user_role in role_hierarchy and required_role in role_hierarchy[user_role]:
            return True
    
    return False

def require_role(role):
    """
    Decorator factory to enforce role-based access control.
    
    Creates a decorator that checks if the authenticated user has the
    required role (or a higher role in the hierarchy) before allowing
    access to the endpoint.
    
    Args:
        role: The minimum role required to access the endpoint
        
    Returns:
        decorator: Function decorator that enforces the role requirement
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check authentication
            if 'user' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_roles = session.get('user', {}).get('roles', [])
            
            # Check if user has the required role (including hierarchy)
            if not check_role_hierarchy(user_roles, role):
                return jsonify({'error': f'Role {role} required. User has roles: {user_roles}'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def decode_token(token):
    """
    Decode and validate JWT token using JWKS from the OIDC provider.
    
    Fetches the public key from the JWKS endpoint and validates the token
    signature, expiration, audience, and issuer.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        dict: Decoded token claims if valid, None otherwise
    """
    try:
        # Fetch public keys from JWKS endpoint
        jwks_client = PyJWKClient(f'{OIDC_ISSUER}/protocol/openid-connect/certs')
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # Validate and decode token
        # Note: The token will have the public issuer URL, so we validate against that
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256'],
            audience=OIDC_CLIENT_ID,
            issuer=OIDC_ISSUER_PUBLIC,  # Use public issuer URL for validation
            options={"verify_exp": True}  # Verify token expiration
        )
        return data
    except Exception as e:
        print(f"Token decode error: {e}")
        return None


@app.route('/api/user')
def get_user():
    """
    Get current user information from session.
    
    Returns user details if authenticated, otherwise returns
    authenticated: false.
    
    Returns:
        JSON response with user information or authentication status
    """
    if 'user' in session:
        return jsonify({
            'authenticated': True,
            'username': session['user'].get('preferred_username', session['user'].get('email', '')),
            'email': session['user'].get('email', ''),
            'roles': session['user'].get('roles', []),
            'attributes': session['user']
        })
    return jsonify({'authenticated': False})

@app.route('/api/protected')
@require_auth
def protected_resource():
    """
    Example protected endpoint requiring authentication.
    
    Demonstrates basic authentication requirement without
    specific role requirements.
    """
    return jsonify({
        'message': 'This is a protected resource',
        'user': session['user'].get('preferred_username', session['user'].get('email', ''))
    })

@app.route('/api/admin')
@require_role('admin')
def admin_resource():
    """
    Admin-only endpoint demonstrating role-based access control.
    
    Only users with 'admin' role can access this endpoint.
    """
    return jsonify({
        'message': 'This is an admin-only resource',
        'user': session['user'].get('preferred_username', session['user'].get('email', ''))
    })

@app.route('/api/editor')
@require_role('editor')
def editor_resource():
    """
    Editor endpoint demonstrating hierarchical RBAC.
    
    Accessible by users with 'editor' role or higher (admin).
    """
    return jsonify({
        'message': 'This is an editor-only resource',
        'user': session['user'].get('preferred_username', session['user'].get('email', '')),
        'data': 'You can edit this content'
    })

@app.route('/oidc/login')
def oidc_login():
    """
    Initiate OIDC authentication flow.
    
    Redirects user to Identity Provider (IdP) for authentication
    using the Authorization Code flow.
    """
    # Use the configured redirect URI instead of generating it
    redirect_uri = OIDC_REDIRECT_URI
    return oidc.authorize_redirect(redirect_uri)

@app.route('/oidc/callback')
def oidc_callback():
    """
    Handle OIDC authentication callback from IdP.
    
    Exchanges authorization code for tokens, validates ID token,
    extracts user claims and roles, establishes user session,
    and redirects to frontend application.
    """
    try:
        # Exchange authorization code for tokens
        token = oidc.authorize_access_token()
        
        # Extract and validate ID token
        id_token = token.get('id_token')
        if id_token:
            # Decode and validate token claims
            claims = decode_token(id_token)
            if claims:
                # Extract user information from token claims
                user_info = {
                    'sub': claims.get('sub'),  # Subject identifier
                    'email': claims.get('email'),
                    'preferred_username': claims.get('preferred_username'),
                    'name': claims.get('name'),
                    'roles': claims.get('realm_access', {}).get('roles', [])  # Realm-level roles
                }
                
                # Also check for client-specific roles
                if 'resource_access' in claims and OIDC_CLIENT_ID in claims['resource_access']:
                    client_roles = claims['resource_access'][OIDC_CLIENT_ID].get('roles', [])
                    user_info['roles'].extend(client_roles)
                
                # Establish authenticated session
                session['user'] = user_info
                # Store tokens for logout and token refresh
                session['tokens'] = {
                    'access_token': token.get('access_token'),
                    'id_token': id_token,
                    'refresh_token': token.get('refresh_token')
                }
        
        return redirect('http://localhost:4001/')
    except Exception as e:
        print(f"OIDC callback error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/oidc/logout')
def oidc_logout():
    """
    Handle OIDC logout flow.
    
    Clears local session and redirects to IdP logout endpoint
    with ID token hint for proper SSO logout.
    """
    # Retrieve ID token before clearing session
    id_token = session.get('tokens', {}).get('id_token')
    # Clear local session
    session.clear()
    
    if id_token:
        # Redirect to IdP logout endpoint for SSO logout
        # Use public URL since the browser needs to access it
        logout_url = f"{OIDC_ISSUER_PUBLIC}/protocol/openid-connect/logout"
        params = {
            'id_token_hint': id_token,  # Helps IdP identify the session
            'post_logout_redirect_uri': 'http://localhost:4001'  # Where to redirect after logout
        }
        logout_url_with_params = logout_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        return redirect(logout_url_with_params)
    
    # Fallback: redirect to frontend if no ID token
    return redirect('http://localhost:4001/')


if __name__ == '__main__':
    # Run Flask development server
    # In production, use a proper WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)